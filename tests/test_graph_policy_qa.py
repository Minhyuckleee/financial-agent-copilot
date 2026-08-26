"""`StateGraph.invoke()` 경계 테스트 — 사내규정질의 골든패스 end-to-end 스모크.

confidence 필터(threshold_low) 자체는 `_filter_confident`가 순수함수라 합성 데이터로
결정론적으로 검증한다 — 실제 오프토픽 질문으로 필터를 테스트하면 query rewrite(LLM,
비결정적)의 문구에 따라 confidence가 경계값 근처에서 흔들려 flaky해진다(rewrite가
오프토픽 질문도 격식체로 재포장해 golden set과 겹치는 구간이 실제로 있음)."""
from dotenv import load_dotenv

from graph.builder import build_graph
from graph.context import NO_CONTEXT_ANSWER, _filter_confident, answer_no_context, has_no_context
from graph.state import AgentState

load_dotenv()


def test_policy_qa_golden_path_end_to_end():
    graph = build_graph()
    result = graph.invoke(AgentState(query="개인정보 유출 사고가 발생하면 며칠 이내에 통지해야 하나요?"))

    assert result["route"] == "policy_qa"
    assert result["rewritten_query"]
    assert result["retrieved_chunks"]
    assert result["answer"]


def test_filter_confident_drops_chunks_below_threshold():
    chunks = [
        {"id": "a", "confidence": 0.75},
        {"id": "b", "confidence": 0.59},
        {"id": "c", "confidence": 0.60},
    ]
    result = _filter_confident(chunks, threshold=0.60)
    assert [c["id"] for c in result] == ["a", "c"]


def test_filter_confident_returns_empty_when_all_below_threshold():
    chunks = [{"id": "a", "confidence": 0.4}, {"id": "b", "confidence": 0.5}]
    assert _filter_confident(chunks, threshold=0.60) == []


def test_has_no_context_true_when_policy_qa_and_no_chunks():
    state = AgentState(query="x", route="policy_qa", retrieved_chunks=[])
    assert has_no_context(state) is True


def test_has_no_context_false_when_chunks_present():
    chunk = {"id": "a", "source": "s", "content": "c", "confidence": 0.9}
    state = AgentState(query="x", route="policy_qa", retrieved_chunks=[chunk])
    assert has_no_context(state) is False


def test_has_no_context_false_for_other_routes_even_if_empty():
    """다른 route는 원래 retrieved_chunks가 비어있는 게 정상 동작이라 이 분기에 안 걸려야 함."""
    state = AgentState(query="x", route="exchange_rate", retrieved_chunks=[])
    assert has_no_context(state) is False


def test_answer_no_context_returns_fixed_message_without_llm_call():
    state = AgentState(query="x", route="policy_qa", retrieved_chunks=[])
    result = answer_no_context(state)
    assert result == {"answer": NO_CONTEXT_ANSWER}
