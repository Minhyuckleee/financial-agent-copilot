"""`StateGraph.invoke()` 경계 테스트 — Tier2(파라미터 재해석) e2e 스모크.

param_invalid는 자연 발화로 재현이 안 돼(노드테스트에서 직접 검증, tests/test_tool_call.py
참고) 여기선 empty_result 경로만 e2e로 확인한다 — 재해석으로 복구되는 경우와, 재해석해도
안 되는 경우(상한 초과, low_confidence 안내) 둘 다 실제로 나올 법한 발화로 실측됨.
"""
from dotenv import load_dotenv

from graph.answer import _LOW_CONFIDENCE_NOTICE
from graph.builder import build_graph
from graph.state import AgentState

load_dotenv()


def test_tier2_recovers_via_reinterpreted_params_e2e():
    graph = build_graph()
    result = graph.invoke(AgentState(query="신한은행 18개월 정기예금 추천해줘"))

    assert result["tier2_retry_count"] == 1
    assert result["error"] is None
    assert result["low_confidence"] is False
    assert result["answer"]
    assert _LOW_CONFIDENCE_NOTICE not in result["answer"]


def test_tier2_exhausts_retry_cap_and_gives_low_confidence_notice_e2e():
    graph = build_graph()
    result = graph.invoke(AgentState(query="새마을금고 정기예금 좋은 상품 추천해줘"))

    assert result["tier2_retry_count"] == 1
    assert result["low_confidence"] is True
    assert _LOW_CONFIDENCE_NOTICE in result["answer"]
    # 사후 재검토 — run_guardrail을 안 거치므로 교정이 하나도 안 쌓여야 함.
    # 재설계 전엔 규칙②가 상품정보 없는 답변에 필수고지문구를 붙이는 부작용이 있었음.
    assert result["guardrail_corrections"] == []
