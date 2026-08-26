"""4단계 answer — 가드레일 통과 후 최종 답변. 낮은확신이면 한계를 명시."""
from graph.state import AgentState

_LOW_CONFIDENCE_NOTICE = "\n\n※ 이 조건으로는 충분히 찾지 못해, 확인된 정보만 안내드립니다."


def finalize_answer(state: AgentState) -> dict:
    answer = state.answer or ""
    if state.low_confidence and _LOW_CONFIDENCE_NOTICE not in answer:
        answer += _LOW_CONFIDENCE_NOTICE
    return {"answer": answer}
