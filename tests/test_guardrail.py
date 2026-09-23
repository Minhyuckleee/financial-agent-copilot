"""노드 함수 경계 테스트 — 가드레일. 전량검사(여러 규칙 동시 적용) + 자동교정 검증."""
from dotenv import load_dotenv

from graph.guardrail import _check_product_rates, _extract_reported_number, run_guardrail
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


_SHINHAN_CREDIT_LOANS = [
    {"bank_name": "신한은행", "product_name": "개인신용대출(마이너스한도대출)", "loan_type": "마이너스한도대출",
     "credit_score_band": "701~800점", "interest_rate": 6.52},
    {"bank_name": "신한은행", "product_name": "개인신용대출(일반신용대출)", "loan_type": "일반신용대출",
     "credit_score_band": "701~800점", "interest_rate": 7.36},
]


def test_same_bank_products_correct_rates_not_overwritten():
    """e2e C012 재현. 같은 은행 상품이 둘이면 은행명 위치가 하나라, 예전엔 두 번째 항목이
    첫 상품 금리와 대조돼 LLM이 맞게 쓴 6.52%를 7.36%로 덮어썼다."""
    answer = "신한은행에서 신용점수 750점이면 마이너스한도대출(마통)은 6.52%, 일반신용대출은 7.36%입니다."
    text, corrections = _check_product_rates(answer, _SHINHAN_CREDIT_LOANS)

    assert corrections == []
    assert text == answer


def test_same_bank_products_still_catch_rate_not_in_source():
    """은행 단위로 묶어도, 그 은행 어느 상품에도 없는 금리는 여전히 잡아야 한다."""
    answer = "신한은행 마이너스한도대출 금리는 5.10%입니다."
    text, corrections = _check_product_rates(answer, _SHINHAN_CREDIT_LOANS)

    assert len(corrections) == 1
    assert "6.52%" in text  # 5.10과 가장 가까운 신한 금리


def test_non_rate_numeric_field_not_used_as_correction_target():
    """save_term_months(12) 같은 비금리 숫자는 교정 후보가 아니다. 예전엔 `_flatten_numbers`로
    항목 전체를 훑어 11.9%가 12로 '교정'될 수 있었다."""
    tool_result = [{"bank_name": "국민은행", "product_name": "정기예금", "save_term_months": 12,
                    "interest_rate": 3.5, "interest_rate_preferential": 3.8}]
    text, corrections = _check_product_rates("국민은행 정기예금 금리는 11.9%입니다.", tool_result)

    assert len(corrections) == 1
    assert "3.8%" in text
    assert "12%" not in text


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
