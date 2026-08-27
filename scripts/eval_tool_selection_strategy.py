"""tool 선택 프롬프트 전략(naive vs 목적재정의) 비교 실험.

같은 100건에 대해 1차 시도는 공통(프로덕션 `call_tool()` 그대로) — 대부분 no_selection이
나오도록 설계된 모호 발화라 여기서 실패를 유도한다. 재시도만 두 조건으로 갈라 비교한다.

조건A(naive) : "이전 대화 참고해서 반드시 tool을 호출하세요" 정도의 일반 지시 — history는
               조건B와 동일하게 이미 프롬프트에 들어가 있음. 차이는 오직 지시 문구(전략).
조건B(production) : tool_call.py의 실제 재시도 로직 그대로(no_selection 전용 목적재정의 지시).

tool_call.py는 무변경 — 조건A만 이 스크립트 안에 별도 함수로 재현한다.

측정:
- tool 호출 성공률 = 재시도 후 error is None AND tool_name == expected_tool_name
- 답변 정확도 = 성공 AND (조건 없으면 자동 통과, 있으면 tool_params_contains 전부 일치)

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/eval_tool_selection_strategy.py
"""
import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env")

from langchain_core.messages import AIMessage, HumanMessage  # noqa: E402

from graph.llm import get_llm  # noqa: E402
from graph.state import AgentState, ToolError  # noqa: E402
from graph.tool_call import _format_history, _TOOLS_BY_ROUTE, call_tool  # noqa: E402

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"

_NAIVE_RETRY_TEMPLATE = (
    "이전 대화:\n{history}\n\n"
    "다음 요청을 처리할 tool을 선택해 호출하세요: {query}\n\n"
    "참고: 이전 시도에서는 적절한 tool을 찾지 못해 조회 자체를 시도하지 않았습니다. "
    "이전 대화를 참고하여 반드시 tool을 호출하세요."
)


def _retry_naive(state: AgentState) -> dict:
    """조건A 재현 — call_tool()의 no_selection 재시도 분기를 일반 지시로만 대체."""
    tools = _TOOLS_BY_ROUTE.get(state.route, [])
    tool_by_name = {t.name: t for t in tools}
    prompt = _NAIVE_RETRY_TEMPLATE.format(history=_format_history(state.history), query=state.query)

    llm_with_tools = get_llm().bind_tools(tools)
    response = llm_with_tools.invoke(prompt)
    if not response.tool_calls:
        return {
            "tool_name": None,
            "tool_params": None,
            "error": ToolError(type="no_selection", message="tool을 선택하지 않음(naive 재시도도 실패)"),
        }

    call = response.tool_calls[0]
    tool = tool_by_name[call["name"]]
    call_args = call["args"]
    try:
        result = tool.invoke(call_args)
    except Exception as e:  # noqa: BLE001 — 비교 실험용, Tier1/2 세분류 불필요
        return {"tool_name": tool.name, "tool_params": call_args, "error": ToolError(type="fail", message=str(e))}
    if not result:
        return {"tool_name": tool.name, "tool_params": call_args, "error": ToolError(type="empty_result", message="조회 결과 없음")}
    return {"tool_name": tool.name, "tool_params": call_args, "tool_result": result, "error": None}


def _grade(case: dict, retried: dict) -> tuple[bool, bool]:
    tool_ok = retried.get("error") is None and retried.get("tool_name") == case["expected_tool_name"]
    params_ok = True
    if tool_ok and case.get("expected_tool_params_contains"):
        actual_params = retried.get("tool_params") or {}
        for k, v in case["expected_tool_params_contains"].items():
            if actual_params.get(k) != v:
                params_ok = False
    return tool_ok, tool_ok and params_ok


def _run_case(case: dict) -> list[dict]:
    """1차 시도는 케이스당 한 번만 실행(paired 설계 — A/B가 같은 1차 실패 상태에서
    출발해야 재시도 전략만의 차이를 보는 것이 됨, LLM 비결정성으로 1차 결과 자체가
    갈리면 비교가 오염됨)."""
    history = [HumanMessage(content=case["turn1_query"]), AIMessage(content=case["turn1_answer"])]
    state = AgentState(query=case["turn2_query"], route="product_recommendation", history=history)
    first = call_tool(state)  # 1차 시도 — A/B 공통(production 그대로), 한 번만

    results = []
    if first.get("error") is None:
        # 모호 발화가 1차에 바로 풀린 경우 — A/B 비교 대상 아님, 둘 다 같은 결과로 채점
        tool_ok, answer_ok = _grade(case, first)
        for condition in ["A", "B"]:
            results.append((condition, False, None, first, tool_ok, answer_ok))
    else:
        retried_state = AgentState(query=state.query, route="product_recommendation", history=history, **first)
        retry_b = call_tool(retried_state)
        retry_a = _retry_naive(retried_state)
        for condition, retried in [("A", retry_a), ("B", retry_b)]:
            tool_ok, answer_ok = _grade(case, retried)
            results.append((condition, True, first["error"].type, retried, tool_ok, answer_ok))

    return [
        {
            "id": case["id"],
            "condition": condition,
            "phrasing_type": case["phrasing_type"],
            "complexity": case["complexity"],
            "reached_retry": reached_retry,
            "first_attempt_error": first_error,
            "tool_success": tool_ok,
            "answer_accurate": answer_ok,
            "actual_tool_name": retried.get("tool_name"),
            "actual_tool_params": retried.get("tool_params"),
        }
        for condition, reached_retry, first_error, retried, tool_ok, answer_ok in results
    ]


def main() -> None:
    cases = json.loads((EVAL_DIR / "tool_selection_strategy_dataset.json").read_text(encoding="utf-8"))

    all_results = []
    for i, case in enumerate(cases, 1):
        case_results = _run_case(case)
        all_results.extend(case_results)
        a, b = case_results
        print(
            f"[{i}/{len(cases)}] {case['id']}: "
            f"A(tool={a['tool_success']},answer={a['answer_accurate']}) "
            f"B(tool={b['tool_success']},answer={b['answer_accurate']})"
        )

    summary = {}
    for condition in ["A", "B"]:
        subset = [r for r in all_results if r["condition"] == condition]
        n = len(subset)
        reached_retry_n = sum(r["reached_retry"] for r in subset)
        tool_success = sum(r["tool_success"] for r in subset)
        answer_accurate = sum(r["answer_accurate"] for r in subset)
        by_type = {}
        for t in ["procedural", "reconfirm", "reason", "vague"]:
            type_subset = [r for r in subset if r["phrasing_type"] == t]
            by_type[t] = {
                "n": len(type_subset),
                "tool_success": sum(r["tool_success"] for r in type_subset),
            }
        summary[condition] = {
            "n": n,
            "reached_retry_n": reached_retry_n,
            "tool_success_rate": tool_success / n,
            "answer_accuracy_rate": answer_accurate / n,
            "by_phrasing_type": by_type,
        }

    out = {"per_case": all_results, "summary": summary}
    out_path = EVAL_DIR / "tool_selection_strategy_results.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== 요약 ===")
    for condition in ["A", "B"]:
        s = summary[condition]
        print(
            f"조건{condition}: 1차부터 성공(재시도 안 감) {s['n'] - s['reached_retry_n']}건 / "
            f"tool 호출 성공률 {s['tool_success_rate']:.1%} / 답변 정확도 {s['answer_accuracy_rate']:.1%}"
        )
        for t, d in s["by_phrasing_type"].items():
            print(f"    {t}: {d['tool_success']}/{d['n']}")
    print(f"\n저장: {out_path}")


if __name__ == "__main__":
    main()
