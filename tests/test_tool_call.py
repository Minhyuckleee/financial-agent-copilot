"""노드 함수 경계 테스트 — tool call. 실제 API 호출(mock 안 함)."""
import json

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from graph.state import AgentState, ToolError
from graph.tool_call import (
    MAX_TIER2_RETRIES,
    MAX_TOOL_CALL_ATTEMPTS,
    answer_tier2_exhausted,
    call_tool,
    route_after_tool_call,
)
from tools.fault_injection import _fail_once_used

load_dotenv()


def test_exchange_rate_route_calls_ecos_tool():
    state = AgentState(query="환율 알려줘", route="exchange_rate")
    result = call_tool(state)
    assert result["tool_name"] == "inquire_exchange_rate"
    assert result["tool_result"]["currency_pair"] == "USD/KRW"
    assert isinstance(result["tool_result"]["rate"], float)


def test_policy_qa_route_skips_tool_call():
    state = AgentState(query="사내규정 알려줘", route="policy_qa")
    result = call_tool(state)
    assert result == {}


def test_deposit_query_selects_deposit_tool():
    state = AgentState(query="정기예금 좋은 상품 추천해줘", route="product_recommendation")
    result = call_tool(state)
    assert result["tool_name"] == "recommend_deposit_products"
    assert isinstance(result["tool_result"], list)


def test_credit_loan_query_selects_credit_loan_tool():
    state = AgentState(query="신용점수 750인 고객 신용대출 알아봐줘", route="product_recommendation")
    result = call_tool(state)
    assert result["tool_name"] == "recommend_credit_loan_products"
    assert result["tool_params"]["credit_score"] == 750


def test_jeonse_query_selects_jeonse_tool():
    state = AgentState(query="전세자금대출 상품 알아봐줘", route="product_recommendation")
    result = call_tool(state)
    assert result["tool_name"] == "recommend_jeonse_loan_products"


def test_mortgage_query_selects_mortgage_tool():
    state = AgentState(query="주택담보대출 상품 추천해줘", route="product_recommendation")
    result = call_tool(state)
    assert result["tool_name"] == "recommend_mortgage_loan_products"


def test_business_loan_query_selects_business_loan_tool():
    state = AgentState(query="개인사업자 신용점수 700인데 사업자대출 알아봐줘", route="product_recommendation")
    result = call_tool(state)
    assert result["tool_name"] == "recommend_business_loan_products"
    assert result["tool_params"]["credit_score"] == 700


def test_fail_once_recovers_on_retry(monkeypatch):
    """1회차 RuntimeError(fail), 2회차 실제 호출 통과. call_tool 노드 자체는
    1회 시도만 하므로(재시도는 그래프 레벨 self-loop, tests/test_graph_tier1.py 참고),
    여기서는 노드를 두 번 호출해 재시도 이후 state로 이어지는지 직접 확인한다."""
    _fail_once_used["inquire_exchange_rate"] = False
    monkeypatch.setenv("FAULT_INJECTION", json.dumps({"inquire_exchange_rate": "fail_once"}))

    state = AgentState(query="환율 알려줘", route="exchange_rate")
    first = call_tool(state)
    assert first["error"].type == "fail"
    assert first["tool_call_attempt_count"] == 1

    retried_state = AgentState(query="환율 알려줘", route="exchange_rate", **first)
    second = call_tool(retried_state)
    assert second["error"] is None
    assert second["tool_call_attempt_count"] == 2
    assert second["tool_result"]["currency_pair"] == "USD/KRW"
    assert second["tool_name"] == first["tool_name"]
    assert second["tool_params"] == first["tool_params"]


def test_fail_exhausts_retry_cap(monkeypatch):
    """fail이 계속되면 상한(2)에서 재시도를 멈춰야 함."""
    monkeypatch.setenv("FAULT_INJECTION", json.dumps({"inquire_exchange_rate": "fail"}))

    state = AgentState(query="환율 알려줘", route="exchange_rate")
    first = call_tool(state)
    assert first["error"].type == "fail"
    assert first["tool_call_attempt_count"] == 1

    retried_state = AgentState(query="환율 알려줘", route="exchange_rate", **first)
    second = call_tool(retried_state)
    assert second["error"].type == "fail"
    assert second["tool_call_attempt_count"] == 2


def test_delay_gives_up_without_retry(monkeypatch):
    """delay는 fail과 달리 상한 체크 없이 즉시 포기해야 함."""
    monkeypatch.setenv("FAULT_INJECTION_DELAY_SECONDS", "0")
    monkeypatch.setenv("FAULT_INJECTION", json.dumps({"inquire_exchange_rate": "delay"}))

    state = AgentState(query="환율 알려줘", route="exchange_rate")
    result = call_tool(state)
    assert result["error"].type == "delay"
    assert result["tool_call_attempt_count"] == 1


def test_empty_result_triggers_tier2():
    """API는 정상 응답했지만 결과가 빔("새마을금고"는 이 API가 커버하는
    은행권 밖이라 실제로 빈 리스트가 옴, 실측 확인됨)."""
    state = AgentState(query="새마을금고 정기예금 좋은 상품 추천해줘", route="product_recommendation")
    result = call_tool(state)
    assert result["error"].type == "empty_result"
    assert result["tier2_retry_count"] == 0  # 트리거만 됐지 아직 재시도 전
    assert result["tool_call_attempt_count"] == 1  # Tier2 재시도가 아닌 첫 시도라 카운트됨


def test_tier2_recovers_via_reinterpreted_params():
    """API에 없는 예치기간(18개월)을 요청하면 1차는 빈 결과, 재해석
    프롬프트를 받은 2차 시도가 파라미터를 스스로 바꿔(예: 12개월) 복구되는지 확인.
    조작 없이 실제로 나올 법한 발화(실측 확인됨 — LLM이 12개월로 재해석)."""
    state = AgentState(query="신한은행 18개월 정기예금 추천해줘", route="product_recommendation")
    first = call_tool(state)
    assert first["error"].type == "empty_result"

    retried_state = AgentState(query=state.query, route="product_recommendation", **first)
    second = call_tool(retried_state)
    assert second["tier2_retry_count"] == 1
    assert second["error"] is None
    assert second["tool_result"]
    assert second["tool_params"] != first["tool_params"]  # 재해석으로 파라미터가 실제로 바뀜


def test_tier2_exhausts_retry_cap_then_routes_to_answer_tier2_exhausted():
    """재해석해도 여전히 안 나오는 경우(새마을금고, MG로 바꿔봐도 이 API
    범위 밖이라 계속 빔, 실측 확인됨) 상한(1) 넘으면 route_after_tool_call이
    answer_tier2_exhausted로 보내야 함(run_guardrail 아님 — 사후 재검토로 가드레일
    스킵하도록 재설계됨, 규칙②가 상품정보 없는데 고지문구를 붙이는 부작용 발견)."""
    state = AgentState(query="새마을금고 정기예금 좋은 상품 추천해줘", route="product_recommendation")
    first = call_tool(state)
    retried_state = AgentState(query=state.query, route="product_recommendation", **first)
    second = call_tool(retried_state)

    assert second["error"].type == "empty_result"
    assert second["tier2_retry_count"] >= MAX_TIER2_RETRIES

    final_state = AgentState(query=state.query, route="product_recommendation", **second)
    assert route_after_tool_call(final_state) == "answer_tier2_exhausted"


def test_answer_tier2_exhausted_sets_low_confidence_and_generates_honest_answer():
    """empty_result/param_invalid 각각 실패 사유가 다르게
    반영되는지, LLM이 짧게라도 실패를 정직하게 안내하는지 확인. 가드레일을 안 거치므로
    guardrail_corrections는 이 노드 호출만으론 안 늘어난다(호출 자체를 안 하니까)."""
    empty_state = AgentState(
        query="새마을금고 정기예금 좋은 상품 추천해줘",
        route="product_recommendation",
        error=ToolError(type="empty_result", message="조회 결과 없음"),
        tool_name="recommend_deposit_products",
        tool_params={"bank_name_filter": "MG"},
    )
    result = answer_tier2_exhausted(empty_state)
    assert result["low_confidence"] is True
    assert result["answer"]

    param_invalid_state = AgentState(
        query="정기예금 추천해줘",
        route="product_recommendation",
        error=ToolError(type="param_invalid", message="검증 실패"),
        tool_name="recommend_deposit_products",
        tool_params={"save_term_months": "열두달"},
    )
    result2 = answer_tier2_exhausted(param_invalid_state)
    assert result2["low_confidence"] is True
    assert result2["answer"]

    no_selection_state = AgentState(
        query="어떻게 신청하나요?",
        route="product_recommendation",
        error=ToolError(type="no_selection", message="tool을 선택하지 않음"),
    )
    result3 = answer_tier2_exhausted(no_selection_state)
    assert result3["low_confidence"] is True
    assert result3["answer"]


def test_no_selection_triggers_tier2():
    """LLM이 tool을 하나도 선택하지 않는 경우(API 예외 아님, 호출 자체를 시도 안 함).
    실제 재현 케이스: "어떻게 신청하나요?"는 조회가 아니라 절차 질문으로 보여서 LLM이
    tool 선택 자체를 건너뜀."""
    history = [
        HumanMessage(content="사업자대출 상품 좀 알아봐줘"),
        AIMessage(content="사업자대출 상품 3건을 안내드립니다."),
    ]
    state = AgentState(query="어떻게 신청하나요?", route="product_recommendation", history=history)
    result = call_tool(state)
    assert result["error"].type == "no_selection"
    assert result["tier2_retry_count"] == 0


def test_no_selection_recovers_via_retry():
    """재시도 프롬프트가 "tool로 literal하게 답 못 해도 상관없이
    호출하라"고 명시해야 복구됨(첫 버전은 일반 지시만 줬다가 재시도에도 계속
    no_selection 나는 것을 실측으로 확인하고 프롬프트를 강화함)."""
    history = [
        HumanMessage(content="사업자대출 상품 좀 알아봐줘"),
        AIMessage(content="사업자대출 상품 3건을 안내드립니다."),
    ]
    state = AgentState(query="어떻게 신청하나요?", route="product_recommendation", history=history)
    first = call_tool(state)
    assert first["error"].type == "no_selection"

    retried_state = AgentState(query=state.query, route="product_recommendation", history=history, **first)
    second = call_tool(retried_state)
    assert second["tier2_retry_count"] == 1
    assert second["error"] is None
    assert second["tool_name"] == "recommend_business_loan_products"
    assert second["tool_result"]


def test_param_invalid_caught_and_classified_correctly():
    """param_invalid는 자연 발화로 사실상 재현이 안 됨(LLM 함수호출 스키마가
    타입을 강제, 실측 확인됨). Tier1 재사용 경로(error.type=="fail"이면 state.tool_params를
    그대로 재사용)를 이용해 실제로 잘못된 타입을 tool.invoke()에 직접 흘려보내
    pydantic.ValidationError가 param_invalid로 올바르게 분류되는지 확인한다(모킹 아님 —
    진짜 pydantic 검증이 진짜로 실패함)."""
    state = AgentState(
        query="정기예금 추천해줘",
        route="product_recommendation",
        error=ToolError(type="fail", message="테스트 셋업용"),
        tool_name="recommend_deposit_products",
        tool_params={"save_term_months": "열두달"},
    )
    result = call_tool(state)
    assert result["error"].type == "param_invalid"
    assert result["tier2_retry_count"] == 0  # 이 시도 자체는 Tier1 경로로 들어왔으므로


def test_history_reused_for_followup_tool_params():
    """이전 turn 조건 재사용 예시("아까 신용점수 750이라 하셨죠")를 실제로 구현.
    1차 발화에서 뽑힌 파라미터(credit_score=750)가 생략된 후속 발화에도 history로
    재사용되는지 확인. history 없으면 tool 선택 자체가 틀어짐(대조군으로 실측 확인됨 —
    recommend_deposit_products로 오분류, credit_score 정보 소실)."""
    turn1_query = "신용점수 750인 고객 신용대출 알아봐줘"
    turn1 = call_tool(AgentState(query=turn1_query, route="product_recommendation"))
    assert turn1["tool_params"]["credit_score"] == 750

    history = [HumanMessage(content=turn1_query), AIMessage(content=str(turn1["tool_result"])[:200])]
    turn2 = call_tool(
        AgentState(query="그 조건으로 농협만 좁혀줘", route="product_recommendation", history=history)
    )
    assert turn2["tool_name"] == "recommend_credit_loan_products"
    assert turn2["tool_params"]["credit_score"] == 750
    assert turn2["tool_params"]["bank_name_filter"] == "농협"


def test_route_after_tool_call_covers_all_branches():
    """조건부 엣지 판단 함수의 분기 전부를 결정론적으로 확인."""
    assert route_after_tool_call(AgentState(query="x", error=None)) == "run_guardrail"
    assert route_after_tool_call(
        AgentState(query="x", error=ToolError(type="fail", message=""), tool_call_attempt_count=1)
    ) == "call_tool"
    assert route_after_tool_call(
        AgentState(
            query="x", error=ToolError(type="fail", message=""), tool_call_attempt_count=MAX_TOOL_CALL_ATTEMPTS
        )
    ) == "answer_tool_error"
    assert route_after_tool_call(AgentState(query="x", error=ToolError(type="delay", message=""))) == "answer_tool_error"
    assert route_after_tool_call(
        AgentState(query="x", error=ToolError(type="empty_result", message=""), tier2_retry_count=0)
    ) == "call_tool"
    assert route_after_tool_call(
        AgentState(
            query="x", error=ToolError(type="empty_result", message=""), tier2_retry_count=MAX_TIER2_RETRIES
        )
    ) == "answer_tier2_exhausted"
    assert route_after_tool_call(
        AgentState(
            query="x", error=ToolError(type="param_invalid", message=""), tier2_retry_count=MAX_TIER2_RETRIES
        )
    ) == "answer_tier2_exhausted"
    assert route_after_tool_call(
        AgentState(query="x", error=ToolError(type="no_selection", message=""), tier2_retry_count=0)
    ) == "call_tool"
    assert route_after_tool_call(
        AgentState(
            query="x", error=ToolError(type="no_selection", message=""), tier2_retry_count=MAX_TIER2_RETRIES
        )
    ) == "answer_tier2_exhausted"
