"""0단계 라우팅 — 발화를 4클래스로 분류, 범위외는 Tier0 재작성으로 1회 복구

분류
1. product_recommendation : 예금/신용대출/전세자금대출/주택담보대출/개인사업자대출 5종 상품 추천 및 후속질문(재조회·조건변경 등)
2. exchange_rate : 원/달러 환율 조회
3. policy_qa : 사내규정/약관/법령 등 문서기반 질의. 상품 관련 후속질문이어도 규정·권리·의무를 묻는 화제전환이면 여기로 분류
4. out_of_scope : 위 3가지 외 전부 (계좌조회, 여신심사/신용평가 기준, 잡담 등)

Tier0 재작성 : 1차 분류가 out_of_scope면 history 참고해 지시대명사·생략맥락을 채운 발화로 재작성 후 1회 재분류
확신 없으면 조용히 틀리지 않고 out_of_scope로 정직하게 분류

history 활용 : 매 호출마다 이전 대화를 프롬프트에 반영 — 같은 발화도 history 유무에 따라 분류결과가 실제로 갈림(실API로 검증됨, `tests/test_router.py`/`tests/test_graph_tier0.py`)
"""
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

from graph.llm import get_llm
from graph.state import AgentState, RouteLabel

_TIER0_RETRY_CAP = 1

_SYSTEM_PROMPT = """당신은 은행 상담직원용 업무보조 에이전트의 라우터입니다.
사용자 발화를 아래 4가지 중 하나로 분류하세요.

- product_recommendation: 정기예금, 신용대출, 전세자금대출, 주택담보대출, 개인사업자대출
  이 5종만 해당한다(취급 tool이 이 5종뿐이다) — 보험 등 이 5종 밖의 금융상품은 "상품"이라는
  단어가 들어가도 product_recommendation이 아니다(문서 유무와 무관하게 out_of_scope다).
  직전에 안내한 금융상품(위 5종)에 대한 후속 질문(왜 조회가 안 됐는지, 조건을 바꿔서 다시
  봐달라는 요청 등)도 새 추천 요청 없이 "왜 그래요?"처럼 짧게만 물어도 포함한다 —
  상담 현장에서 실제로 나오는 표현이다.
  단, 그 후속 질문이 조회결과 자체(재조회·조건변경·조회실패 이유)가 아니라 그 상품과
  관련된 규정·권리·의무(계약 전 확인사항, 해지 시 불이익, 설명의무, 예금자보호 여부 등
  문서 기반 답이 필요한 성격)를 묻는 것이면 policy_qa로 화제가 전환된 것이다 — "상품"이라는
  단어가 이어져도 이 경우는 product_recommendation이 아니다.
- exchange_rate: 원/달러 환율 조회 요청
- policy_qa: 사내규정, 약관, 법령 등 문서 기반 질의. 다루는 문서는 개인정보보호·전자금융·
  금융상품 설명의무·마이데이터·예금거래약관 등이다. "신용정보의 이용 및 보호에 관한 법률"
  문서가 있다고 해서 여신심사 기준·대출승인 절차·신용평가 로직까지 다루는 것은 아니다 —
  이런 요청은 문서 유무와 무관하게 out_of_scope다.
- out_of_scope: 위 3가지에 해당하지 않는 모든 요청. 계좌조회, 여신심사/신용평가 기준이나
  절차, 기업분석, 잡담, 보험상품 안내 등. "신용" 관련 단어가 있어도 실제 심사기준·승인여부
  판단을 묻는 질문이면 out_of_scope다.

확신이 없으면 out_of_scope로 분류하세요. 조용히 틀린 클래스로 배정하지 마세요."""


class _RouteClassification(BaseModel):
    route: RouteLabel


def _format_history(history: list[BaseMessage]) -> str:
    if not history:
        return "(이전 대화 없음)"
    lines = []
    for m in history:
        role = "사용자" if m.type == "human" else "에이전트"
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines)


def _classify(query: str, history: list[BaseMessage]) -> RouteLabel:
    llm = get_llm().with_structured_output(_RouteClassification)
    prompt = (
        f"{_SYSTEM_PROMPT}\n\n"
        f"이전 대화:\n{_format_history(history)}\n\n"
        f"이번 발화: {query}"
    )
    result: _RouteClassification = llm.invoke(prompt)
    return result.route


def route_query(state: AgentState) -> dict:
    route = _classify(state.query, state.history)

    if route != "out_of_scope":
        return {"route": route}

    if state.tier0_retry_count >= _TIER0_RETRY_CAP:
        return {"route": "out_of_scope"}

    rewritten = _rewrite_for_retry(state.query, state.history)
    retried_route = _classify(rewritten, state.history)
    return {
        "route": retried_route,
        "query": rewritten,
        "tier0_retry_count": state.tier0_retry_count + 1,
    }


OUT_OF_SCOPE_ANSWER = "죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다."


def answer_out_of_scope(state: AgentState) -> dict:
    """LLM 호출 없이 고정 문구로 즉시 종료 — 정적 문자열이라 build_context·call_tool·
    run_guardrail 통과가 애초에 불필요해서 그래프 레벨에서 건너뛴다(context.py의
    answer_no_context와 같은 논리)."""
    return {"answer": OUT_OF_SCOPE_ANSWER}


def _rewrite_for_retry(query: str, history: list[BaseMessage]) -> str:
    llm = get_llm()
    prompt = (
        "다음 발화가 모호하거나 맥락이 빠져 있어 분류에 실패했습니다. "
        "이전 대화를 참고해 지시대명사·생략된 맥락을 채운, 더 명확한 발화로 다시 쓰세요. "
        "다시 쓴 발화만 출력하세요.\n\n"
        f"이전 대화:\n{_format_history(history)}\n\n"
        f"원래 발화: {query}"
    )
    response = llm.invoke(prompt)
    return response.content.strip()
