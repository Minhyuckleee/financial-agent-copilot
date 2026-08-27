"""tool 선택 전략 A(naive)/B(현재 프로덕션) 비교 — 신규 50건(절차형 전용, 복합조건).

`eval_tool_selection_strategy.py`(100건)에서 확인한 발견을 다른 문구·조건값으로 재현되는지
확인하는 용도입니다. 100건과 안 겹치는 신규 절차형 문구 10개 × 5상품 × 복합조건(은행명/
신용점수/기간 전부 명시)으로 구성해, tool 재선택뿐 아니라 조건(파라미터) 보존까지 같이
확인합니다.

`tool_call.py`는 무변경 — A만 이 스크립트 안에서 별도로 재현합니다.

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/eval_tool_selection_strategy_testset.py
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



def _call_with_prompt(state: AgentState, prompt: str) -> dict:
    tools = _TOOLS_BY_ROUTE.get(state.route, [])
    tool_by_name = {t.name: t for t in tools}
    llm_with_tools = get_llm().bind_tools(tools)
    response = llm_with_tools.invoke(prompt)
    if not response.tool_calls:
        return {
            "tool_name": None,
            "tool_params": None,
            "error": ToolError(type="no_selection", message="재시도도 tool 미선택"),
        }
    call = response.tool_calls[0]
    tool = tool_by_name[call["name"]]
    call_args = call["args"]
    try:
        result = tool.invoke(call_args)
    except Exception as e:  # noqa: BLE001 — 비교 실험용
        return {"tool_name": tool.name, "tool_params": call_args, "error": ToolError(type="fail", message=str(e))}
    if not result:
        return {"tool_name": tool.name, "tool_params": call_args, "error": ToolError(type="empty_result", message="조회 결과 없음")}
    return {"tool_name": tool.name, "tool_params": call_args, "tool_result": result, "error": None}


def _retry_a(state: AgentState) -> dict:
    prompt = _NAIVE_RETRY_TEMPLATE.format(history=_format_history(state.history), query=state.query)
    return _call_with_prompt(state, prompt)


def _grade(case: dict, retried: dict) -> tuple[bool, bool]:
    tool_ok = retried.get("error") is None and retried.get("tool_name") == case["expected_tool_name"]
    params_ok = True
    if tool_ok and case.get("expected_tool_params_contains"):
        actual_params = retried.get("tool_params") or {}
        for k, v in case["expected_tool_params_contains"].items():
            av = actual_params.get(k)
            if k == "bank_name_filter":
                if not av or (v not in av and av not in v):
                    params_ok = False
            elif av != v:
                params_ok = False
    return tool_ok, tool_ok and params_ok


def _run_case(case: dict) -> list[dict]:
    history = [HumanMessage(content=case["turn1_query"]), AIMessage(content=case["turn1_answer"])]
    state = AgentState(query=case["turn2_query"], route="product_recommendation", history=history)
    first = call_tool(state)  # 1차 시도 — 전 조건 공통(production 그대로), 한 번만

    results = []
    if first.get("error") is None:
        tool_ok, answer_ok = _grade(case, first)
        for condition in ["A", "B"]:
            results.append((condition, False, None, first, tool_ok, answer_ok))
    else:
        retried_state = AgentState(query=state.query, route="product_recommendation", history=history, **first)
        retry_results = {
            "A": _retry_a(retried_state),
            "B": call_tool(retried_state),
        }
        for condition, retried in retry_results.items():
            tool_ok, answer_ok = _grade(case, retried)
            results.append((condition, True, first["error"].type, retried, tool_ok, answer_ok))

    return [
        {
            "id": case["id"],
            "condition": condition,
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
    cases = json.loads((EVAL_DIR / "tool_selection_strategy_testset.json").read_text(encoding="utf-8"))

    all_results = []
    for i, case in enumerate(cases, 1):
        case_results = _run_case(case)
        all_results.extend(case_results)
        a, b = case_results
        print(
            f"[{i}/{len(cases)}] {case['id']}: "
            f"A(tool={a['tool_success']},ans={a['answer_accurate']}) "
            f"B(tool={b['tool_success']},ans={b['answer_accurate']})"
        )

    summary = {}
    for condition in ["A", "B"]:
        subset = [r for r in all_results if r["condition"] == condition]
        n = len(subset)
        retried = [r for r in subset if r["reached_retry"]]
        summary[condition] = {
            "n": n,
            "reached_retry_n": len(retried),
            "tool_success_rate_overall": sum(r["tool_success"] for r in subset) / n,
            "answer_accuracy_rate_overall": sum(r["answer_accurate"] for r in subset) / n,
            "tool_success_rate_retry_only": (
                sum(r["tool_success"] for r in retried) / len(retried) if retried else None
            ),
            "answer_accuracy_rate_retry_only": (
                sum(r["answer_accurate"] for r in retried) / len(retried) if retried else None
            ),
        }

    out = {"per_case": all_results, "summary": summary}
    out_path = EVAL_DIR / "tool_selection_strategy_testset_results.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== 요약 (신규 50건) ===")
    for condition in ["A", "B"]:
        s = summary[condition]
        print(
            f"조건{condition}: 재시도대상 {s['reached_retry_n']}/{s['n']} | "
            f"전체 tool성공 {s['tool_success_rate_overall']:.1%} 답변정확 {s['answer_accuracy_rate_overall']:.1%} | "
            f"재시도만 tool성공 {s['tool_success_rate_retry_only']} 답변정확 {s['answer_accuracy_rate_retry_only']}"
        )
    print(f"\n저장: {out_path}")


if __name__ == "__main__":
    main()
