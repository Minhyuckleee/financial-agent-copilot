"""`StateGraph.invoke()` 경계 테스트 — 환율조회 골든패스 end-to-end 스모크."""
from dotenv import load_dotenv

from graph.builder import build_graph
from graph.guardrail import _template_exchange_rate_answer
from graph.state import AgentState

load_dotenv()


def test_exchange_rate_golden_path_end_to_end():
    graph = build_graph()
    result = graph.invoke(AgentState(query="환율 알려줘"))

    assert result["route"] == "exchange_rate"
    assert result["tool_name"] == "inquire_exchange_rate"
    assert result["tool_result"]["currency_pair"] == "USD/KRW"
    assert result["answer"]
    assert str(result["tool_result"]["rate"]) in result["answer"] or "환율" in result["answer"]
    assert result["guardrail_corrections"] == []


def test_template_exchange_rate_answer_uses_dot_separated_date():
    """대시 구분자("2026-08-11")는 규칙①의 계좌번호 정규식(\\d{2,6}-\\d{2,6}-\\d{2,8})과
    우연히 매칭돼 날짜가 마스킹되는 버그가 실측으로 발견됐다 — 점 구분자로
    회피했는지 회귀 방지."""
    tool_result = {"currency_pair": "USD/KRW", "rate": 1416.0, "base_date": "20260811"}
    answer = _template_exchange_rate_answer(tool_result)
    assert answer == "현재 USD/KRW 환율은 1416.0원입니다. (기준일: 2026.08.11)"
