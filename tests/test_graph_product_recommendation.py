"""`StateGraph.invoke()` 경계 테스트 — 상품추천(예금+개인신용대출) 골든패스."""
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from graph.builder import build_graph
from graph.state import AgentState

load_dotenv()


def test_deposit_golden_path_end_to_end():
    graph = build_graph()
    result = graph.invoke(AgentState(query="정기예금 좋은 상품 추천해줘"))

    assert result["route"] == "product_recommendation"
    assert result["tool_name"] == "recommend_deposit_products"
    assert result["tool_result"]
    assert result["answer"]


def test_credit_loan_golden_path_end_to_end():
    graph = build_graph()
    result = graph.invoke(AgentState(query="신용점수 750인 고객 신용대출 알아봐줘"))

    assert result["route"] == "product_recommendation"
    assert result["tool_name"] == "recommend_credit_loan_products"
    assert result["tool_result"]
    assert result["answer"]


def test_jeonse_golden_path_end_to_end():
    graph = build_graph()
    result = graph.invoke(AgentState(query="전세자금대출 상품 알아봐줘"))

    assert result["route"] == "product_recommendation"
    assert result["tool_name"] == "recommend_jeonse_loan_products"
    assert result["tool_result"]
    assert result["answer"]


def test_mortgage_golden_path_end_to_end():
    graph = build_graph()
    result = graph.invoke(AgentState(query="주택담보대출 상품 추천해줘"))

    assert result["route"] == "product_recommendation"
    assert result["tool_name"] == "recommend_mortgage_loan_products"
    assert result["tool_result"]
    assert result["answer"]


def test_business_loan_golden_path_end_to_end():
    graph = build_graph()
    result = graph.invoke(AgentState(query="개인사업자 신용점수 700인데 사업자대출 알아봐줘"))

    assert result["route"] == "product_recommendation"
    assert result["tool_name"] == "recommend_business_loan_products"
    assert result["tool_result"]
    assert result["answer"]


def test_credit_loan_numeric_self_check_matches_actual_rate_type():
    """발견 버그 회귀 테스트 — recommend_credit_loan_products가
    crdt_lend_rate_type='A'(대출금리)만 걸러야 한다. 섞이면 가산금리(C) 같은
    엉뚱한 값이 뽑혀 규칙④가 오탐하거나(실제로는 tool 버그) 잘못된 금리를 추천하게 된다."""
    graph = build_graph()
    result = graph.invoke(AgentState(query="신용점수 750인 고객 신용대출 알아봐줘"))

    numeric_corrections = [c for c in result["guardrail_corrections"] if c.rule == "numeric_self_check"]
    assert numeric_corrections == []


def test_followup_reuses_history_for_tool_params_e2e():
    """CLI와 같은 방식(turn마다 history 누적)으로 두 번째
    발화가 생략한 조건(credit_score=750)을 이전 turn에서 재사용하는지 전체 그래프로
    확인."""
    graph = build_graph()
    turn1_query = "신용점수 750인 고객 신용대출 알아봐줘"
    turn1 = graph.invoke(AgentState(query=turn1_query))
    assert turn1["tool_params"]["credit_score"] == 750

    history = [HumanMessage(content=turn1_query), AIMessage(content=turn1["answer"])]
    turn2 = graph.invoke(AgentState(query="그 조건으로 농협만 좁혀줘", history=history))

    assert turn2["route"] == "product_recommendation"
    assert turn2["tool_params"]["credit_score"] == 750
    assert turn2["tool_params"]["bank_name_filter"] == "농협"
