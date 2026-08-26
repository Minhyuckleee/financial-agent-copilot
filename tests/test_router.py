"""노드 함수 경계 테스트 — 라우팅. 실제 LLM 호출(mock 안 함)."""
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from graph.router import route_query
from graph.state import AgentState

load_dotenv()

_EXPLAIN_DUTY_HISTORY = [
    HumanMessage(content="금융소비자보호법상 설명의무는 어떤 내용인가요?"),
    AIMessage(content="금융상품 판매업자는 계약체결 전 상품의 주요 내용을 소비자가 이해할 수 있도록 설명해야 합니다."),
]


def test_exchange_rate_classified_correctly():
    state = AgentState(query="환율 알려줘")
    result = route_query(state)
    assert result["route"] == "exchange_rate"


def test_out_of_scope_classified_correctly():
    state = AgentState(query="제 계좌 잔액 조회해줘")
    result = route_query(state)
    assert result["route"] == "out_of_scope"


def test_follow_up_uses_history_to_stay_policy_qa():
    """"그거 더 있어?"처럼 지시대명사만 있는 후속질문도 history로 같은
    클래스(policy_qa) 유지되는지 확인."""
    state = AgentState(query="그거 더 있어?", history=_EXPLAIN_DUTY_HISTORY)
    result = route_query(state)
    assert result["route"] == "policy_qa"


def test_tier0_recovers_ambiguous_follow_up_via_rewrite():
    """history가 있어도 극단적으로 생략된 후속질문("왜 그래요?")은 1차
    분류가 out_of_scope로 실패하고, Tier0 재작성 후 재분류에서 policy_qa로 복구됨을
    실측 확인(조작한 예시 아님 — 실제 상담 현장에서 나올 법한 문장)."""
    state = AgentState(query="왜 그래요?", history=_EXPLAIN_DUTY_HISTORY)
    result = route_query(state)
    assert result["route"] == "policy_qa"
    assert result["tier0_retry_count"] == 1


def test_out_of_scope_final_rejection_account_inquiry_respects_retry_cap():
    """명백한 범위외(계좌조회)는 Tier0가 1회 재시도해도 out_of_scope로
    최종 확정되고, 추가 재시도 없이 종료됨(tier0_retry_count 상한 1)."""
    state = AgentState(query="제 계좌 잔액 조회해주세요")
    result = route_query(state)
    assert result["route"] == "out_of_scope"
    assert result["tier0_retry_count"] == 1


def test_out_of_scope_final_rejection_credit_screening_respects_retry_cap():
    """여신심사/신용평가 요청도 동일하게 최종 out_of_scope 확정(스코프아웃 대상)."""
    state = AgentState(query="여신심사 기준이 어떻게 되나요")
    result = route_query(state)
    assert result["route"] == "out_of_scope"
    assert result["tier0_retry_count"] == 1
