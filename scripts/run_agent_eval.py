"""Agent 레벨 평가 하네스 — v1(탐색용, 53건, train/test 구분 없음).

`data/eval/agent_eval_v1.json`의 각 케이스를 실제로 실행하고(question 있으면
`StateGraph.invoke()` 전체 그래프, seed_state면 특정 노드/함수 직접 호출) `expected`와
대조한다. LLM judge 없음 — 전부 구조적 필드(route/tool_name/tool_params/
guardrail_rule_triggered/answer_type) 코드 비교. 이번 v1은 모든 카테고리에 걸쳐 통계적 정밀도 없이 최소표본만
채워 "어디가 약한지" 보는 탐색용. 여기서 약한 카테고리를 찾으면 그 카테고리만 train/test
정식 분리로 확장한다.

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/run_agent_eval.py
"""
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

load_dotenv()

from langchain_core.messages import AIMessage, HumanMessage  # noqa: E402

from graph.builder import build_graph  # noqa: E402
from graph.guardrail import run_guardrail  # noqa: E402
from graph.state import AgentState  # noqa: E402
from tools.ecos import inquire_exchange_rate  # noqa: E402
from tools.fault_injection import reset_fail_once_state  # noqa: E402
from tools.finlife import (  # noqa: E402
    recommend_business_loan_products,
    recommend_credit_loan_products,
    recommend_deposit_products,
    recommend_jeonse_loan_products,
    recommend_mortgage_loan_products,
)

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"

_TOOLS_BY_NAME = {
    t.name: t
    for t in [
        recommend_deposit_products,
        recommend_credit_loan_products,
        recommend_jeonse_loan_products,
        recommend_mortgage_loan_products,
        recommend_business_loan_products,
        inquire_exchange_rate,
    ]
}

_TOOL_ERROR_FAIL_MSG = "죄송합니다, 일시적인 시스템 오류로 조회에 실패했습니다. 잠시 후 다시 시도해주세요."
_TOOL_ERROR_DELAY_MSG = "죄송합니다, 응답 지연으로 조회를 완료하지 못했습니다. 잠시 후 다시 시도해주세요."
_NO_CONTEXT_MSG = "해당 질문은 사내규정질의DB 스코프 외입니다."
_OUT_OF_SCOPE_MSG = "죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다."


def _history_to_messages(history: list[dict]) -> list:
    out = []
    for m in history:
        if m["role"] == "human":
            out.append(HumanMessage(content=m["content"]))
        else:
            out.append(AIMessage(content=m["content"]))
    return out


def _classify_answer_type(answer: str, low_confidence: bool) -> str:
    """low_confidence는 이 코드베이스에서 answer_tier2_exhausted 경로만 세팅하는
    플래그라(state.py: "Tier2 캡 초과 등"), 텍스트 휴리스티 대신 이 필드로 직접
    판별한다 — v1 1차 실행에서 자유생성 문구가 매번 달라 텍스트매칭이 놓치는 걸
    실측으로 확인함(v1_022/023)."""
    if answer == _NO_CONTEXT_MSG:
        return "no_context"
    if answer == _OUT_OF_SCOPE_MSG:
        return "out_of_scope_rejection"
    if answer == _TOOL_ERROR_FAIL_MSG or answer == _TOOL_ERROR_DELAY_MSG:
        return "tool_error"
    if low_confidence:
        return "tier2_exhausted"
    return "normal"


def _run_question_case(case: dict) -> dict:
    reset_fail_once_state()  # 케이스 간 fail_once 상태 오염 방지
    if case.get("fault_injection"):
        fi = case["fault_injection"]
        os.environ["FAULT_INJECTION"] = json.dumps({fi["tool"]: fi["mode"]})
        os.environ["FAULT_INJECTION_DELAY_SECONDS"] = "0"
    else:
        os.environ.pop("FAULT_INJECTION", None)

    graph = build_graph()
    history = _history_to_messages(case.get("history") or [])
    result = graph.invoke(AgentState(query=case["question"], history=history))

    os.environ.pop("FAULT_INJECTION", None)

    triggered_rules = sorted({c.rule for c in result.get("guardrail_corrections", [])})
    return {
        "route": result.get("route"),
        "tool_name": result.get("tool_name"),
        "tool_params": result.get("tool_params"),
        "tool_call_attempt_count": result.get("tool_call_attempt_count"),
        "tier0_retry_count": result.get("tier0_retry_count"),
        "tier2_retry_count": result.get("tier2_retry_count"),
        "low_confidence": result.get("low_confidence"),
        "guardrail_rule_triggered": triggered_rules,
        "answer": result.get("answer"),
        "answer_type": _classify_answer_type(result.get("answer") or "", result.get("low_confidence", False)),
    }


def _run_guardrail_seed_case(case: dict) -> dict:
    seed = case["seed_state"]
    state = AgentState(
        query="(seed)",
        route=seed["route"],
        answer=seed["answer"],
        tool_result=seed.get("tool_result"),
        tool_name=seed.get("tool_name"),
        retrieved_chunks=seed.get("retrieved_chunks") or [],
    )
    result = run_guardrail(state)
    triggered_rules = sorted({c.rule for c in result.get("guardrail_corrections", [])})
    return {"guardrail_rule_triggered": triggered_rules, "answer": result.get("answer")}


def _run_param_invalid_seed_case(case: dict) -> dict:
    seed = case["seed_state"]
    tool = _TOOLS_BY_NAME[seed["tool_name"]]
    try:
        tool.invoke(seed["tool_params"])
        return {"error_type": None}
    except ValidationError:
        return {"error_type": "param_invalid"}


def _grade(case: dict, actual: dict) -> tuple[bool, list[str]]:
    expected = case["expected"]
    problems = []

    if "pass_if_any" in expected:
        # b4(RAG rewrite 충실도) 전용 — 방어가 (a)정직한 거절 텍스트 (b)가드레일 규칙⑤ 사후교정
        # 둘 중 어느 경로로 성공해도 동등하게 유효하다. 대안 하나라도 만족하면 통과.
        for alt_expected in expected["pass_if_any"]:
            alt_case = {**case, "expected": alt_expected}
            ok, _ = _grade(alt_case, actual)
            if ok:
                return (True, [])
        return (False, [f"pass_if_any: 대안 {len(expected['pass_if_any'])}개 전부 불만족"])

    if "error_type" in expected:
        if actual.get("error_type") != expected["error_type"]:
            problems.append(f"error_type: expected={expected['error_type']} actual={actual.get('error_type')}")
        return (len(problems) == 0, problems)

    if "route" in expected and actual.get("route") != expected["route"]:
        problems.append(f"route: expected={expected['route']} actual={actual.get('route')}")

    if "route_in" in expected and actual.get("route") not in expected["route_in"]:
        # b4 재설계 — 코퍼스 경계/거절문구를 정확히 맞히려는 시도가 반복적으로 제 가정
        # 오류로 판명나서, "route가 policy_qa든 out_of_scope든 정직한
        # 경로면 통과"로 단순화. product_recommendation/exchange_rate로 새는 진짜
        # 라우팅 혼동만 잡아낸다.
        problems.append(f"route_in: expected one of {expected['route_in']} actual={actual.get('route')}")

    if "tool_name" in expected and actual.get("tool_name") != expected["tool_name"]:
        problems.append(f"tool_name: expected={expected['tool_name']} actual={actual.get('tool_name')}")

    if "tool_params_contains" in expected:
        actual_params = actual.get("tool_params") or {}
        for k, v in expected["tool_params_contains"].items():
            if actual_params.get(k) != v:
                problems.append(f"tool_params.{k}: expected={v} actual={actual_params.get(k)}")

    if "tool_params_bank_matches" in expected:
        # 은행명 축약형("국민") vs 정식명("국민은행") 둘 다 finlife API 기준 기능적으로
        # 동일(substring 매칭이라 필터 결과 같음) — m4 1차실행에서 exact match가 과했던
        # 걸 확인해 양방향 substring 허용으로 완화.
        actual_params = actual.get("tool_params") or {}
        for k, v in expected["tool_params_bank_matches"].items():
            actual_v = actual_params.get(k) or ""
            # actual_v가 빈 문자열이면 "" in v가 항상 True라 아래 substring 비교만으론
            # "파라미터 자체가 소실됨"을 놓친다(빈 문자열은 통과시키면 안 됨) — 명시적으로 걸러낸다.
            if not actual_v or (v not in actual_v and actual_v not in v):
                problems.append(f"tool_params_bank_matches.{k}: expected~={v} actual={actual_v}")

    if "tier0_recovered" in expected:
        recovered = (actual.get("tier0_retry_count") or 0) > 0 and actual.get("route") != "out_of_scope"
        if recovered != expected["tier0_recovered"]:
            problems.append(f"tier0_recovered: expected={expected['tier0_recovered']} actual={recovered}")

    if "tier1_recovered" in expected:
        recovered = actual.get("answer_type") == "normal"
        if recovered != expected["tier1_recovered"]:
            problems.append(f"tier1_recovered: expected={expected['tier1_recovered']} actual={recovered}")

    if "tier2_recovered" in expected:
        recovered = actual.get("answer_type") == "normal"
        if recovered != expected["tier2_recovered"]:
            problems.append(f"tier2_recovered: expected={expected['tier2_recovered']} actual={recovered}")

    if "low_confidence" in expected and actual.get("low_confidence") != expected["low_confidence"]:
        problems.append(f"low_confidence: expected={expected['low_confidence']} actual={actual.get('low_confidence')}")

    if "answer_type" in expected and actual.get("answer_type") != expected["answer_type"]:
        problems.append(f"answer_type: expected={expected['answer_type']} actual={actual.get('answer_type')}")

    if "answer_contains" in expected:
        answer = actual.get("answer") or ""
        for phrase in expected["answer_contains"]:
            if phrase not in answer:
                problems.append(f"answer_contains 누락: '{phrase}' not in answer")

    if "answer_contains_none" in expected:
        # m7(PII 이력재인용 누출) 전용 — 이력에서 언급된 PII가 마스킹 없이 최종답변에
        # 그대로 새어나오는지 확인. run_guardrail의 정규식 마스킹은
        # 최종 답변 텍스트 전체를 스캔하므로 정상이라면 여기서 항상 통과해야 하고,
        # 걸리면 마스킹 정규식이 실제 LLM 출력 포맷을 놓쳤다는 뜻.
        answer = actual.get("answer") or ""
        leaked = [phrase for phrase in expected["answer_contains_none"] if phrase in answer]
        if leaked:
            problems.append(f"answer_contains_none 위반(PII 누출 의심): {leaked}")

    if "answer_contains_any" in expected:
        # DB-miss 케이스는 has_no_context 고정문구 경로든, 답변생성 정직성 프롬프트가
        # 자유생성으로 "확인할 수 없다"고 답하는 경로든 둘 다 정답(defense-in-depth
        # 2차 방어선) — v1 재실행 실측으로 확인된 정상 동작이라
        # 하나만 맞으면 통과로 완화.
        answer = actual.get("answer") or ""
        if not any(p in answer for p in expected["answer_contains_any"]):
            problems.append(f"answer_contains_any 전부 불일치: {expected['answer_contains_any']} (answer={answer[:80]}...)")

    if "guardrail_rule_triggered" in expected:
        expected_rules = sorted(expected["guardrail_rule_triggered"])
        actual_rules = actual.get("guardrail_rule_triggered") or []
        if expected_rules != actual_rules:
            problems.append(f"guardrail_rule_triggered: expected={expected_rules} actual={actual_rules}")

    if "guardrail_rule_triggered_contains" in expected:
        # exact match 대신 포함여부만 확인 — 같은 답변에서 여러 규칙이 동시에 정당하게
        # 걸릴 수 있음(v1_028 실측: ②③ 동시발생이 정상 동작이었음)
        actual_rules = set(actual.get("guardrail_rule_triggered") or [])
        missing = [r for r in expected["guardrail_rule_triggered_contains"] if r not in actual_rules]
        if missing:
            problems.append(f"guardrail_rule_triggered_contains 누락: {missing} (actual={sorted(actual_rules)})")

    return (len(problems) == 0, problems)


def main() -> None:
    import sys

    cases_filename = sys.argv[1] if len(sys.argv) > 1 else "agent_eval_v1.json"
    cases = json.loads((EVAL_DIR / cases_filename).read_text(encoding="utf-8"))

    results = []
    for i, case in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {case['id']} {case['category']} - {case['category_label']}")
        try:
            if case.get("seed_state") and "answer" in case["seed_state"]:
                actual = _run_guardrail_seed_case(case)
            elif case.get("seed_state") and "tool_params" in case["seed_state"]:
                actual = _run_param_invalid_seed_case(case)
            else:
                actual = _run_question_case(case)
            passed, problems = _grade(case, actual)
        except Exception as e:
            actual = {}
            passed, problems = False, [f"EXCEPTION: {type(e).__name__}: {e}"]

        results.append(
            {
                "id": case["id"],
                "category": case["category"],
                "category_label": case["category_label"],
                "metric_type": case["metric_type"],
                "passed": passed,
                "problems": problems,
                "actual": actual,
            }
        )
        print(f"  -> {'PASS' if passed else 'FAIL'}" + (f" | {problems}" if problems else ""))

    out_path = EVAL_DIR / cases_filename.replace(".json", "_results.json")
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    total = len(results)
    passed_n = sum(1 for r in results if r["passed"])
    print(f"\n=== TSR: {passed_n}/{total} = {passed_n/total:.1%} ===")

    by_cat: dict[str, list[bool]] = {}
    for r in results:
        by_cat.setdefault(r["category"], []).append(r["passed"])
    print("\n=== 카테고리별 ===")
    for cat, outcomes in sorted(by_cat.items()):
        p = sum(outcomes)
        print(f"  {cat}: {p}/{len(outcomes)}")

    print(f"\n저장: {out_path}")


if __name__ == "__main__":
    main()
