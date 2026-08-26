"""노드 함수 경계 테스트 — answer. finalize_answer는 LLM 호출 없는 순수함수."""
from graph.answer import _LOW_CONFIDENCE_NOTICE, finalize_answer
from graph.state import AgentState


def test_finalize_answer_appends_notice_when_low_confidence():
    state = AgentState(query="x", answer="조건에 맞는 상품을 찾지 못했습니다.", low_confidence=True)
    result = finalize_answer(state)
    assert _LOW_CONFIDENCE_NOTICE in result["answer"]


def test_finalize_answer_no_notice_when_confident():
    state = AgentState(query="x", answer="정상 답변입니다.", low_confidence=False)
    result = finalize_answer(state)
    assert _LOW_CONFIDENCE_NOTICE not in result["answer"]
