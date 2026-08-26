"""2단계 tool call — route별 tool을 Function Calling으로 노출, LLM이 선택+파라미터 결정

예외분기
1. Tier1(API 레벨) : fail(일시적 오류, 같은 파라미터로 최대 1회 재시도) / delay(응답지연, 재시도 없이 포기)
2. Tier2(해석 레벨) : empty_result(결과없음)/param_invalid(파라미터검증실패)/no_selection(tool 미선택) 셋 다 "못 쓸 결과"로 묶어서, LLM이 파라미터 재해석 후 최대 1회 재시도

history 재사용 : 이전 턴에서 확정된 조건을 후속 발화에 재적용

재시도 상한 초과 시 : run_guardrail 거치지 않고(5규칙이 이 상황엔 no-op/부적절), 실패 사유별로 다른 정직한 안내문 생성 + low_confidence=True"""

from langchain_core.messages import BaseMessage
from pydantic import ValidationError

from tools.ecos import inquire_exchange_rate
from tools.finlife import (
    recommend_business_loan_products,
    recommend_credit_loan_products,
    recommend_deposit_products,
    recommend_jeonse_loan_products,
    recommend_mortgage_loan_products,
)

from graph.llm import get_llm
from graph.state import AgentState, ToolError

_TOOLS_BY_ROUTE: dict[str, list] = {
    "exchange_rate": [inquire_exchange_rate],
    "product_recommendation": [
        recommend_deposit_products,
        recommend_credit_loan_products,
        recommend_jeonse_loan_products,
        recommend_mortgage_loan_products,
        recommend_business_loan_products,
    ],
    "policy_qa": [],  # tool 없음 — RAG만 사용
    "out_of_scope": [],
}

MAX_TOOL_CALL_ATTEMPTS = 2  # Tier1 fail 재시도 상한 — 최초 시도 1 + 재시도 1
MAX_TIER2_RETRIES = 1  # Tier2 파라미터 재해석 상한

_TOOL_ERROR_MESSAGES = {
    "fail": "죄송합니다, 일시적인 시스템 오류로 조회에 실패했습니다. 잠시 후 다시 시도해주세요.",
    "delay": "죄송합니다, 응답 지연으로 조회를 완료하지 못했습니다. 잠시 후 다시 시도해주세요.",
}

_TIER2_RETRY_REASON = {
    "empty_result": "결과가 없었습니다",
    "param_invalid": "파라미터가 유효하지 않았습니다",
    "no_selection": "적절한 tool을 찾지 못해 조회 자체를 시도하지 않았습니다",
}


def _format_history(history: list[BaseMessage]) -> str:
    if not history:
        return "(이전 대화 없음)"
    lines = []
    for m in history:
        role = "사용자" if m.type == "human" else "에이전트"
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines)


def call_tool(state: AgentState) -> dict:
    tools = _TOOLS_BY_ROUTE.get(state.route, [])
    if not tools:
        return {}

    tool_by_name = {t.name: t for t in tools}
    is_tier1_retry = (
        state.error is not None and state.error.type == "fail" and state.tool_name in tool_by_name
    )
    is_tier2_retry = state.error is not None and state.error.type in (
        "empty_result",
        "param_invalid",
        "no_selection",
    )

    if is_tier1_retry:
        # 같은 실패한 호출을 그대로 다시 해본다 — 파라미터 재선택 없음.
        tool = tool_by_name[state.tool_name]
        call_args = state.tool_params or {}
    else:
        llm_with_tools = get_llm().bind_tools(tools)
        history_block = (
            f"이전 대화:\n{_format_history(state.history)}\n\n"
            "주의: 은행명·신용점수·기간처럼 tool 파라미터로 넣을 수 있는 조건은 "
            "이번 발화나 위 이전 대화에 실제로 언급된 것만 사용하세요. 언급되지 않은 "
            "조건은 지어내지 말고 파라미터에서 비워두거나 기본값을 쓰세요(은행 언급이 "
            "없는 질문에 은행명을 임의로 지어내 넣지 않도록 주의).\n\n"
        )
        if is_tier2_retry:
            reason = _TIER2_RETRY_REASON[state.error.type]
            if state.error.type == "no_selection":
                # tool_name/tool_params가 없다(애초에 아무것도 선택 안 했으므로) —
                # "이전 시도는 X로 호출했으나"라고 쓰면 앞뒤가 안 맞는다.
                # 첫 재시도에서 일반적인 "반드시 호출하세요" 지시만으로는 부족했다
                # (실측: "어떻게 신청하나요?"류는 재시도에도 계속 no_selection) — LLM이
                # "이 질문은 tool이 직접 답할 내용이 아니다"라고 판단하면 일반 지시로는
                # 그 판단을 안 뒤집는다. tool 호출의 목적이 "질문에 literal하게 답하는
                # 것"이 아니라 "이전 대화 맥락의 상품정보를 다시 확보하는 것"임을
                # 명시적으로 풀어써야 한다.
                prompt = (
                    f"{history_block}"
                    f"다음 요청을 처리할 tool을 선택해 호출하세요: {state.query}\n\n"
                    f"참고: 이전 시도에서는 {reason}. 이 질문이 tool로 직접 답할 수 없는 "
                    "내용(예: 신청 절차, 필요 서류)으로 보여도 상관없습니다 — 그런 "
                    "경우에도 이전 대화에서 다루던 상품을 다시 조회하는 tool을 반드시 "
                    "호출하세요. 조회된 상품 정보를 바탕으로 답변을 작성하되 절차 관련 "
                    "부분은 일반적인 안내로 보완하면 됩니다. tool 호출을 건너뛰지 마세요."
                )
            else:
                prompt = (
                    f"{history_block}"
                    f"다음 요청을 처리할 tool을 선택해 호출하세요: {state.query}\n\n"
                    f"참고: 이전 시도는 {state.tool_name}({state.tool_params})로 호출했으나 "
                    f"{reason}. 조건을 다시 검토해 다른 파라미터로 호출하세요."
                )
        else:
            prompt = (
                f"{history_block}다음 요청을 처리할 tool을 선택해 호출하세요: {state.query}\n\n"
                "참고: 요청이 그 자체로는 모호하거나(예: \"왜 그래요?\", \"다시 한번 봐주세요\") "
                "무엇을 조회할지 불명확해도, 이전 대화가 있으면 그 이전 대화에서 다루던 "
                "상품·조건의 연장선으로 해석해 동일한 tool을 같은(또는 언급된 대로 수정된) "
                "조건으로 호출하세요. 되묻지 말고 이력을 근거로 판단해 반드시 tool을 "
                "호출하세요."
            )
        response = llm_with_tools.invoke(prompt)
        if not response.tool_calls:
            # LLM이 tool을 하나도 선택하지 않음 — API 예외(Tier1)가 아니라 API 호출
            # 자체를 시도 안 한 것이라, tool_call_attempt_count(Tier1 전용)는 안 올리고
            # Tier2 재시도 경로로 편입시킨다(무신호 실패도 "이번 시도가 못 쓸 결과였다"라는
            # 점은 같으므로).
            tier2_count = state.tier2_retry_count + (1 if is_tier2_retry else 0)
            return {
                "tier2_retry_count": tier2_count,
                "error": ToolError(type="no_selection", message="tool을 선택하지 않음"),
            }
        call = response.tool_calls[0]
        tool = tool_by_name[call["name"]]
        call_args = call["args"]

    # tool_call_attempt_count는 Tier1(fail 재시도) 전용 카운터라 Tier2 재시도일 땐 안 올린다.
    attempt_count = state.tool_call_attempt_count + (0 if is_tier2_retry else 1)
    tier2_count = state.tier2_retry_count + (1 if is_tier2_retry else 0)
    counters = {"tool_call_attempt_count": attempt_count, "tier2_retry_count": tier2_count}
    # Tier2 최초 시도(재시도가 아닐 때)가 empty_result/param_invalid로 실패하면 그 시점
    # 파라미터를 보존한다 — 재시도가 조건을 완화해 성공했을 때 answer 단계가 "원래 조건은
    # 뭐였는지" 알 수 있게 한다(조건완화 사실을 답변에 명시 못하던 버그 수정).
    tier2_first_failure = {} if is_tier2_retry else {"tier2_failed_params": call_args}

    try:
        result = tool.invoke(call_args)
    except RuntimeError as e:
        return {
            "tool_name": tool.name,
            "tool_params": call_args,
            **counters,
            "error": ToolError(type="fail", message=str(e)),
        }
    except TimeoutError as e:
        return {
            "tool_name": tool.name,
            "tool_params": call_args,
            **counters,
            "error": ToolError(type="delay", message=str(e)),
        }
    except ValidationError as e:
        return {
            "tool_name": tool.name,
            "tool_params": call_args,
            **counters,
            **tier2_first_failure,
            "error": ToolError(type="param_invalid", message=str(e)),
        }

    if not result:
        return {
            "tool_name": tool.name,
            "tool_params": call_args,
            **counters,
            **tier2_first_failure,
            "error": ToolError(type="empty_result", message="조회 결과 없음"),
        }

    return {
        "tool_name": tool.name,
        "tool_params": call_args,
        "tool_result": result,
        **counters,
        "error": None,
    }


def route_after_tool_call(state: AgentState) -> str:
    """call_tool 이후 조건부 엣지 — Tier1/Tier2 재시도(self-loop)·포기·정상진행 분기."""
    if state.error is None:
        return "run_guardrail"
    if state.error.type == "fail":
        return "call_tool" if state.tool_call_attempt_count < MAX_TOOL_CALL_ATTEMPTS else "answer_tool_error"
    if state.error.type == "delay":
        return "answer_tool_error"
    # empty_result / param_invalid / no_selection — Tier2
    return "call_tool" if state.tier2_retry_count < MAX_TIER2_RETRIES else "answer_tier2_exhausted"


def answer_tool_error(state: AgentState) -> dict:
    """Tier1 최종 포기 — 고정 문구, LLM 호출도 가드레일도 불필요(05의
    answer_no_context와 같은 논리). Tier1 실패는 API 자체가 시스템적으로 안 된
    것이라 무엇을 조회하려 했는지와 무관하게 항상 같은 안내로 충분하다."""
    return {"answer": _TOOL_ERROR_MESSAGES[state.error.type]}


_TIER2_EXHAUSTED_REASON = {
    "empty_result": "조회는 정상적으로 됐으나 조건에 맞는 결과가 없었습니다",
    "param_invalid": "요청하신 조건을 정확히 파악하지 못했습니다",
    "no_selection": "요청하신 내용에 맞는 조회 항목을 찾지 못했습니다",
}


def answer_tier2_exhausted(state: AgentState) -> dict:
    """Tier2 재해석도 실패 — 되묻지 않고 정직하게 실패를 안내한다. run_guardrail을
    거치지 않는다(RAG 0-chunk/Tier1과 같은 논리) — 5규칙 중 실제로 의미 있는 게
    하나도 없다: ①PII/③금지표현은 "실패했다"는 문장에 나올 일이 없고, ④는
    tool_result가 없어 원래도 no-op, ②(필수고지사항 자동삽입)는 오히려 부적절하다
    (상품 정보 자체를 안 준 상황에 "가입조건은 확인 후 확정됩니다" 문구가 붙는 게
    실측으로 확인됨). empty_result와 param_invalid는 원인이
    달라 문구도 다르게 생성되도록 실패 사유를 프롬프트에 명시한다(전자는 "찾아봤는데
    없음", 후자는 "요청 자체를 제대로 못 알아들음" — 사실이 다르니 안내도 달라야 함)."""
    reason = _TIER2_EXHAUSTED_REASON[state.error.type]
    llm = get_llm()
    prompt = (
        "다음 요청을 처리하려 했으나 실패했습니다. 상담직원에게 짧고 정직하게 "
        "안내하는 문장을 작성하세요. 되묻지 말고 안내만 하세요. 뭉뚱그려 \"입력하신 "
        "조건\"이라고만 쓰지 말고, 시도한 조건에 특정 은행명·기간·점수처럼 구체적인 "
        "값이 있으면 그 값을 문장에 그대로 언급하세요.\n\n"
        f"질문: {state.query}\n시도한 조건: {state.tool_params}\n실패 사유: {reason}"
    )
    answer = llm.invoke(prompt).content.strip()
    return {"answer": answer, "low_confidence": True}
