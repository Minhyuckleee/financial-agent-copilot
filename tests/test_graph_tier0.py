"""`StateGraph.invoke()` 경계 테스트 — Tier0(라우팅 재작성) 후속질문/최종거절 e2e 스모크.

라우터의 Tier0 로직(router.py)과 history 참조는 이미 구현됐지만 실API로
검증된 적이 없었다 — 이 파일은 (1) 대화이력이 실제로 전체 그래프에서 후속질문 분류에
반영되는지, (2) 범위외 최종 확정시 조용히 오답하지 않고 정직한 거절 메시지가 answer로
나가는지를 CLI와 같은 방식(turn마다 history 누적)으로 확인한다.
"""
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from graph.builder import build_graph
from graph.state import AgentState

load_dotenv()


def test_follow_up_question_stays_policy_qa_with_history_e2e():
    graph = build_graph()
    turn1_query = "금융소비자보호법상 설명의무는 어떤 내용인가요?"
    turn1 = graph.invoke(AgentState(query=turn1_query))
    assert turn1["route"] == "policy_qa"

    history = [HumanMessage(content=turn1_query), AIMessage(content=turn1["answer"])]
    turn2 = graph.invoke(AgentState(query="그거 더 있어?", history=history))

    assert turn2["route"] == "policy_qa"
    assert turn2["answer"]


def test_out_of_scope_final_rejection_gives_honest_message_e2e():
    graph = build_graph()
    result = graph.invoke(AgentState(query="여신심사 기준이 어떻게 되나요"))

    assert result["route"] == "out_of_scope"
    assert result["answer"] == "죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다."
