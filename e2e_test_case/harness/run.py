"""e2e 평가 실행 — agent 를 있는 그대로 돌리고 결정론 채점까지 한다.

    python e2e_test_case/harness/run.py            core + edge 전부
    python e2e_test_case/harness/run.py C001 E004  골라서

agent 코드는 건드리지 않는다. `graph.stream(stream_mode="updates")` 로 노드마다의 변경을
받아 궤적을 만든다. state 는 마지막 tool 호출 하나만 남기지만(재시도 때 덮어쓴다),
stream 은 매 호출을 순서대로 준다.

산출물은 e2e_test_case/runs/<시각>/ 아래에 쌓인다.
    traces/<id>.json      케이스별 실행 기록 전체
    deterministic.json    결정론 결과
    summary.md            요약
    judge/                궤적·답변 judge 에 넘길 배치 (batches.py)

외부 API 오류로 실행 자체가 실패한 케이스는 채점하지 않고 따로 센다.
토스가 아니라 finlife·ECOS 가 죽은 것을 agent 점수로 치지 않는다.
"""
import datetime as dt
import json
import logging
import sys
import traceback
from pathlib import Path

# finlife 는 API 키를 URL 쿼리(auth=...)로 받는다. httpx 가 INFO 로 요청 URL 을 찍으면
# 키가 평문으로 터미널에 나간다(실제로 한 번 새었다). 평가 실행 중에는 HTTP 로그를
# WARNING 아래로 전부 끈다. 다른 모듈이 나중에 INFO 로 올려도 다시 막도록 disable 을 쓴다.
logging.disable(logging.INFO)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE))
sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")  # cli.py 와 같은 방식. 값은 어디에도 출력하지 않는다

from langchain_core.messages import AIMessage, HumanMessage  # noqa: E402

from graph.builder import build_graph  # noqa: E402
from graph.state import AgentState  # noqa: E402

from batches import write_batches  # noqa: E402
from case import load_cases, score  # noqa: E402


def _plain(value):
    """stream 이 주는 pydantic 객체를 JSON 으로 바꾼다."""
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    return value


def run_case(graph, case) -> dict:
    history = []
    for turn in case.history:
        history += [HumanMessage(content=turn.사용자), AIMessage(content=turn.에이전트)]

    steps, tool_calls = [], []
    route, answer, chunks, tool_results = None, None, [], []
    for update in graph.stream(AgentState(query=case.question, history=history),
                               stream_mode="updates"):
        for node, change in update.items():
            change = _plain(change or {})
            step = {"node": node}

            if node == "route_query":
                route = change.get("route", route)
                step["route"] = change.get("route")
                if "query" in change:            # Tier0 재작성이 일어났다
                    step["rewritten_query"] = change["query"]
            elif node == "build_context":
                chunks = change.get("retrieved_chunks") or []
                step["rewritten_query"] = change.get("rewritten_query")
                step["retrieved"] = [
                    {"source": c.get("source"), "score": c.get("score")} for c in chunks]
            elif node == "call_tool" and change.get("tool_name"):
                call = {"name": change["tool_name"], "args": change.get("tool_params") or {},
                        "error": (change.get("error") or {}).get("type")}
                tool_calls.append(call)
                step.update(call)
                if change.get("tool_result") is not None:
                    tool_results.append(change["tool_result"])
                    result = change["tool_result"]
                    step["result_count"] = len(result) if isinstance(result, list) else 1
            elif node == "call_tool":
                step["error"] = (change.get("error") or {}).get("type")  # no_selection
            elif node == "run_guardrail":
                step["guardrail"] = [c["rule"] for c in change.get("guardrail_corrections", [])]
            elif node in ("answer_tool_error", "answer_tier2_exhausted"):
                step["low_confidence"] = change.get("low_confidence", False)

            if "answer" in change:
                answer = change["answer"]
            steps.append(step)

    return {"id": case.id, "question": case.question,
            "history": [t.model_dump() for t in case.history],
            "route": route, "tool_calls": tool_calls, "steps": steps,
            "answer": answer,
            # 답변 judge 가 숫자·인용을 대조할 원자료. tool 이름은 넣지 않는다
            "source_data": {"tool_results": tool_results,
                            "documents": [{"source": c.get("source"),
                                           "content": c.get("content")} for c in chunks]}}


def main(only: list[str]) -> int:
    graph = build_graph()
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = HERE.parent / "runs" / stamp
    (out / "traces").mkdir(parents=True, exist_ok=True)

    cases = load_cases(HERE.parent)
    if only:
        cases = [c for c in cases if c.id in set(only)]
    results, traces, infra = [], [], []
    for case in cases:
        try:
            trace = run_case(graph, case)
        except Exception as exc:  # 외부 API·키 문제 — 채점에서 뺀다
            infra.append({"id": case.id, "error": type(exc).__name__,
                          "detail": traceback.format_exception_only(exc)[-1][:200]})
            print(f"  INFRA {case.id}  {type(exc).__name__}")
            continue
        (out / "traces" / f"{case.id}.json").write_text(
            json.dumps(trace, ensure_ascii=False, indent=1), encoding="utf-8")
        result = score(case, trace)
        results.append(result)
        traces.append((case, trace))
        print(f"  {'PASS' if result.passed else 'FAIL'}  {case.id}")
        for r in result.reasons:
            print(f"        {r}")

    (out / "deterministic.json").write_text(json.dumps(
        {"results": [r.model_dump() for r in results], "infra_excluded": infra},
        ensure_ascii=False, indent=1), encoding="utf-8")

    by_id = {c.id: c for c, _ in traces}
    lines = [f"# e2e 실행 {stamp}", "",
             f"결정론 {sum(r.passed for r in results)}/{len(results)}"
             f" · 인프라 오류로 제외 {len(infra)}", ""]
    for tier in ("core", "edge"):
        sub = [r for r in results if by_id[r.case_id].tier == tier]
        if sub:
            lines.append(f"- {tier}: {sum(r.passed for r in sub)}/{len(sub)}")
    lines += ["", "## 실패", ""]
    for r in results:
        if not r.passed:
            lines.append(f"- `{r.case_id}` — " + " / ".join(r.reasons))
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    write_batches(traces, out / "judge")
    print(f"\n{out}")
    print("\n".join(lines[2:4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
