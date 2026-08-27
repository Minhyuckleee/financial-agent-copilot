"""StateGraph 조립 — 전체 그래프 노드/엣지 연결, 흐름제어만 담당(로직은 각 노드 파일에)

기본 흐름 : 라우팅(Tier0 내장) → route별 분기 → (context구성 | tool call(Tier1/2)) → 가드레일 → answer

route_query 직후 LangGraph 정석 라우터 패턴(add_conditional_edges)으로 route별로 필요한
노드로만 분기한다 — policy_qa는 build_context로, exchange_rate/product_recommendation은
call_tool로, out_of_scope는 고정문구 노드로 바로 감(해당 없는 노드는 아예 호출 자체를
안 함).

조건부 엣지
1. route_query 후 : route별로 build_context/call_tool/answer_out_of_scope 중 하나로 분기
2. build_context 후 : policy_qa인데 confidence 필터 통과 청크 0개면 고정문구로 조기종료, 아니면 run_guardrail
3. call_tool 후 : Tier1(fail→재시도 self-loop / delay·상한초과→고정문구) · Tier2(empty_result/param_invalid→재시도 self-loop / 상한초과→run_guardrail 생략하고 LLM이 실패사유 반영해 안내문 생성) · 정상성공→run_guardrail
"""
from langgraph.graph import END, START, StateGraph

from graph.answer import finalize_answer
from graph.context import answer_no_context, build_context, has_no_context
from graph.guardrail import run_guardrail
from graph.state import AgentState
from graph.tool_call import answer_tier2_exhausted, answer_tool_error, call_tool, route_after_tool_call
from graph.router import answer_out_of_scope, route_query


def _route_after_classification(state: AgentState) -> str:
    if state.route == "policy_qa":
        return "build_context"
    if state.route == "out_of_scope":
        return "answer_out_of_scope"
    return "call_tool"


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("route_query", route_query)
    workflow.add_node("build_context", build_context)
    workflow.add_node("answer_no_context", answer_no_context)
    workflow.add_node("answer_out_of_scope", answer_out_of_scope)
    workflow.add_node("call_tool", call_tool)
    workflow.add_node("answer_tool_error", answer_tool_error)
    workflow.add_node("answer_tier2_exhausted", answer_tier2_exhausted)
    workflow.add_node("run_guardrail", run_guardrail)
    workflow.add_node("finalize_answer", finalize_answer)

    workflow.add_edge(START, "route_query")
    workflow.add_conditional_edges(
        "route_query",
        _route_after_classification,
        {
            "build_context": "build_context",
            "call_tool": "call_tool",
            "answer_out_of_scope": "answer_out_of_scope",
        },
    )
    workflow.add_conditional_edges(
        "build_context",
        lambda state: "answer_no_context" if has_no_context(state) else "run_guardrail",
        {"answer_no_context": "answer_no_context", "run_guardrail": "run_guardrail"},
    )
    workflow.add_edge("answer_no_context", "finalize_answer")
    workflow.add_edge("answer_out_of_scope", "finalize_answer")
    workflow.add_conditional_edges(
        "call_tool",
        route_after_tool_call,
        {
            "call_tool": "call_tool",
            "answer_tool_error": "answer_tool_error",
            "answer_tier2_exhausted": "answer_tier2_exhausted",
            "run_guardrail": "run_guardrail",
        },
    )
    workflow.add_edge("answer_tool_error", "finalize_answer")
    workflow.add_edge("answer_tier2_exhausted", "finalize_answer")
    workflow.add_edge("run_guardrail", "finalize_answer")
    workflow.add_edge("finalize_answer", END)

    return workflow.compile()
