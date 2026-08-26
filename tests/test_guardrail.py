"""노드 함수 경계 테스트 — 가드레일. 전량검사(여러 규칙 동시 적용) + 자동교정 검증."""
from dotenv import load_dotenv

from graph.guardrail import _extract_reported_number, run_guardrail
from graph.state import AgentState

load_dotenv()


def test_extract_reported_number_exchange_rate_uses_regex_not_llm():
    """exchange_rate route는 LLM 호출 없이 정규식으로만 추출돼야 한다."""
    text = "현재 USD/KRW 환율은 1416.0원입니다. (기준일: 2026.08.11)"
    assert _extract_reported_number(text, route="exchange_rate") == 1416.0


def test_extract_reported_number_exchange_rate_returns_none_when_no_match():
    assert _extract_reported_number("환율 정보를 조회하지 못했습니다.", route="exchange_rate") is None


def test_multiple_rules_triggered_and_all_applied():
    """계좌번호+금지표현+숫자불일치+고지누락 4개가 동시에 걸리는 케이스 — 전량검사."""
    state = AgentState(
        query="예금 추천해줘",
        route="product_recommendation",
        tool_name="recommend_deposit_products",
        tool_result=[{"bank_name": "국민은행", "product_name": "정기예금", "interest_rate": 3.5, "interest_rate_preferential": 3.5}],
        answer="계좌번호 110-234-567890로 예금 가능합니다. 원금 보장되는 상품입니다. 국민은행 정기예금 금리는 5.0%입니다.",
    )
    result = run_guardrail(state)
    corrections = result["guardrail_corrections"]
    rules_triggered = {c.rule for c in corrections}

    assert rules_triggered == {"pii_masking", "disclosure_missing", "prohibited_terms", "numeric_self_check"}
    assert "110-234-567890" not in result["answer"]
    assert "원금 보장" not in result["answer"]
    assert "5.0" not in result["answer"]
    assert "상품설명서" in result["answer"]


def test_product_rate_misattribution_caught_by_bank_segmentation():
    """예전엔 `_flatten_numbers`로 route 전체 풀을 대조해서, A은행 절에
    B은행 금리를 잘못 적어도 그 숫자가 풀 안(B은행 것)에 있으니 통과해버리는 구멍이
    있었다. 은행명 위치로 답변을 분절해 그 구간 안의 금리만 그 은행 항목과 대조하도록
    바꿔서(LLM 미사용), 상품명(은행) 귀속까지 정확히 잡히는지 확인."""
    state = AgentState(
        query="예금 추천해줘",
        route="product_recommendation",
        tool_name="recommend_deposit_products",
        tool_result=[
            {"bank_name": "국민은행", "product_name": "정기예금A", "interest_rate": 3.5, "interest_rate_preferential": 3.8},
            {"bank_name": "우리은행", "product_name": "정기예금B", "interest_rate": 3.6, "interest_rate_preferential": 3.9},
        ],
        answer="국민은행 정기예금A 금리는 3.9%이고, 우리은행 정기예금B 금리는 3.9%입니다.",
    )
    result = run_guardrail(state)
    numeric_corrections = [c for c in result["guardrail_corrections"] if c.rule == "numeric_self_check"]

    assert len(numeric_corrections) == 1
    assert "국민은행" in numeric_corrections[0].reason
    assert "우리은행 정기예금B 금리는 3.9%입니다" in result["answer"]  # 원래 맞는 값은 안 건드림
    assert "국민은행 정기예금A 금리는 3.8%" in result["answer"]  # 오귀속된 값만 3.5/3.8 중 최근접(3.8)으로 교정


def test_clean_answer_produces_no_corrections():
    state = AgentState(
        query="환율 알려줘",
        route="exchange_rate",
        tool_name="inquire_exchange_rate",
        tool_result={"currency_pair": "USD/KRW", "rate": 1416.0, "base_date": "20260811"},
        answer="현재 원/달러 환율은 1416.0원입니다.",
    )
    result = run_guardrail(state)
    assert result["guardrail_corrections"] == []
