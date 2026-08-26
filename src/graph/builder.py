"""StateGraph 조립 — 전체 그래프 노드/엣지 연결, 흐름제어만 담당(로직은 각 노드 파일에)

기본 흐름 : 라우팅(Tier0 내장) → context구성 → tool call(Tier1/2) → 가드레일 → answer

조건부 엣지
1. build_context 후 : policy_qa인데 confidence 필터 통과 청크 0개면 call_tool/run_guardrail 건너뛰고 고정문구로 조기종료
2. call_tool 후 : Tier1(fail→재시도 self-loop / delay·상한초과→고정문구) · Tier2(empty_result/param_invalid→재시도 self-loop / 상한초과→run_guardrail 생략하고 LLM이 실패사유 반영해 안내문 생성) · 정상성공→run_guardrail
"""
from langgraph.graph import END, START, StateGraph

from graph.answer import finalize_answer
from graph.context import answer_no_context, build_context, has_no_context
from graph.guardrail import run_guardrail
from graph.state import AgentState
from graph.tool_call import answer_tier2_exhausted, answer_tool_error, call_tool, route_after_tool_call
from graph.router import route_query


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("route_query", route_query)
    workflow.add_node("build_context", build_context)
    workflow.add_node("answer_no_context", answer_no_context)
    workflow.add_node("call_tool", call_tool)
    workflow.add_node("answer_tool_error", answer_tool_error)
    workflow.add_node("answer_tier2_exhausted", answer_tier2_exhausted)
    workflow.add_node("run_guardrail", run_guardrail)
    workflow.add_node("finalize_answer", finalize_answer)

    workflow.add_edge(START, "route_query")
    workflow.add_edge("route_query", "build_context")
    workflow.add_conditional_edges(
        "build_context",
        lambda state: "answer_no_context" if has_no_context(state) else "call_tool",
        {"answer_no_context": "answer_no_context", "call_tool": "call_tool"},
    )
    workflow.add_edge("answer_no_context", "finalize_answer")
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
