"""1단계 context 구성 — history+RAG 결합, policy_qa route만 실행

파이프라인
1. query rewrite : 지시대명사·생략맥락 채워서 검색전용 문장으로 재작성(법령/약관 격식체, 사용자 비노출)
2. retrieve() : RAG 검색
3. confidence 필터(threshold_low=0.40) : 정밀분리선 아니라 "극단적 저신호만 거르는 느슨한 바닥선" — 애매한 케이스는 여기서 못 거름

방어선 : confidence 필터가 못 거른 "그럴듯하지만 문서에 없는 질문"은 answer 생성단계의 정직한 안내("확인 불가")와 규칙⑤(citation grounding)가 최종 방어

0개 남으면 : call_tool/run_guardrail 건너뛰고 고정문구로 바로 종료(has_no_context)
"""
from langchain_core.messages import BaseMessage

from graph.llm import get_llm
from graph.state import AgentState

_REWRITE_PROMPT = """목표는 사용자 질문의 의도에 가장 잘 맞는 문서(chunk)를 검색하여 사용자 질문에 답하는 데
필요한 최적의 context를 뽑아내는 것입니다.
아래 발화를 이전 대화를 참고해 지시대명사·생략된 맥락을 채운 뒤,
법령·약관 문서에서 쓸 법한 격식체·전문 용어로 바꿔 완결된 검색 문장 하나로 쓰세요.
발화나 이전 대화에 없는 내용을 새로 지어내지는 마세요.
다시 쓴 문장만 출력하세요."""


def _format_history(history: list[BaseMessage]) -> str:
    if not history:
        return "(이전 대화 없음)"
    lines = []
    for m in history:
        role = "사용자" if m.type == "human" else "에이전트"
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines)


def _rewrite_for_retrieval(query: str, history: list[BaseMessage]) -> str:
    llm = get_llm()
    prompt = f"{_REWRITE_PROMPT}\n\n" f"이전 대화:\n{_format_history(history)}\n\n" f"발화: {query}"
    response = llm.invoke(prompt)
    return response.content.strip()


def _filter_confident(chunks: list[dict], threshold: float) -> list[dict]:
    return [c for c in chunks if c["confidence"] >= threshold]


def build_context(state: AgentState) -> dict:
    if state.route != "policy_qa":
        return {"retrieved_chunks": []}

    from rag.retriever import THRESHOLD_LOW, retrieve

    rewritten = _rewrite_for_retrieval(state.query, state.history)
    chunks = retrieve(rewritten)
    confident_chunks = _filter_confident(chunks, THRESHOLD_LOW)

    return {"rewritten_query": rewritten, "retrieved_chunks": confident_chunks}


NO_CONTEXT_ANSWER = "해당 질문은 사내규정질의DB 스코프 외입니다."


def has_no_context(state: AgentState) -> bool:
    """build_context 이후 조건부 엣지가 참조하는 분기 조건 — policy_qa인데 confidence
    필터를 통과한 청크가 0개인 경우만 해당(다른 route는 원래 retrieved_chunks가 비어
    있는 게 정상이라 여기 안 걸림)."""
    return state.route == "policy_qa" and not state.retrieved_chunks


def answer_no_context(state: AgentState) -> dict:
    """LLM 호출 없이 고정 문구로 즉시 종료 — 정적 문자열이라 가드레일(call_tool·
    run_guardrail) 통과가 애초에 불필요해서 그래프 레벨에서 건너뛴다."""
    return {"answer": NO_CONTEXT_ANSWER}
