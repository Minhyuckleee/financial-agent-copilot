"""은행 상담직원용 CLI — REPL 루프. turn마다 history 누적."""
import sys

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from graph.builder import build_graph
from graph.state import AgentState


def main() -> None:
    # Windows 콘솔 기본 코드페이지가 UTF-8이 아니면 한글 입력이 surrogate로 깨져
    # 이후 OpenAI API 요청 인코딩 단계에서 터진다 — stdin/stdout을 명시적으로 UTF-8로 강제.
    if sys.stdin.encoding.lower() != "utf-8":
        sys.stdin.reconfigure(encoding="utf-8")
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    load_dotenv()
    graph = build_graph()
    history: list = []

    print("은행 상담직원용 업무보조 에이전트. 종료하려면 'exit' 입력.")
    while True:
        query = input("\n> ").strip()
        if query.lower() in {"exit", "quit"}:
            break
        if not query:
            continue

        result = graph.invoke(AgentState(query=query, history=history))
        answer = result["answer"]
        print(answer)

        history.append(HumanMessage(content=query))
        history.append(AIMessage(content=answer))


if __name__ == "__main__":
    main()
