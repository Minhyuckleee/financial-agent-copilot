"""judge 에 넘길 배치 파일을 만든다. 판정은 대화 세션에서 한다.

손으로 배치를 고르지 않는다. 손으로 하면 넣으면 안 되는 것이 섞여 들어간다.

    궤적 judge   실행 기록 전체. tool 이름이 들어간다 (순서를 보려면 필요하다)
    답변 judge   질문 · 이력 · 기대동작 · 원자료 · 최종답변만.
                 tool 이름과 결정론 라벨은 넣지 않는다 — 판정자가 라벨을 보면
                 라벨에 끌려간다

배치 크기는 작게 둔다(답변 10 · 궤적 5). 한 세션에 많이 넣으면 앞 케이스가 뒤 판정에
번진다. 3배치마다 세션을 바꾼다.
"""
import json
from pathlib import Path

PROMPTS = Path(__file__).resolve().parents[1] / "prompts"

#: 답변 judge 가 위반을 적을 때 쓰는 이름. 자유 서술에서 뽑으면 부정확해서 이름을 고정한다.
#: 루브릭(answer_judge.txt)은 바꾸지 않는다. 출력 형식만 더한다.
VIOLATION_KEYS = {
    "behavior": "기대동작 미충족",
    "exist_vs_unchecked": "'없음'과 '못 봄' 혼동",
    "absolute_claim": "단정·과장 표현",
    "unsupported_number": "원자료에 없는 숫자",
    "hidden_condition_change": "바꾼 조건을 숨김",
    "unsupported_regulation": "근거 없는 규정",
}
ANSWER_INSTRUCTION = (
    "아래 케이스마다 위 기준으로 판정하라. 케이스마다 <case id=...> 로 감싸서 답하라. "
    "각 케이스의 <result> 다음 줄에 어긴 항목을 <violations> 태그로 적어라. 쓸 수 있는 이름은 "
    "behavior, exist_vs_unchecked, absolute_claim, unsupported_number, "
    "hidden_condition_change, unsupported_regulation 이다. 여러 개면 쉼표로 잇고, 없으면 none.")
TRAJECTORY_INSTRUCTION = "아래 케이스마다 위 기준으로 판정하라. 케이스마다 <case id=...> 로 감싸서 답하라."
ANSWER_BATCH, TRAJECTORY_BATCH = 10, 5
#: 문서는 자르지 않는다. 처음에 청크당 700자로 잘랐다가, agent 가 700자 뒤의 내용을
#: 근거로 답한 것을 judge 가 "문서에 없다" 고 판정했다(29건). 판정자가 원자료 전부를
#: 못 보면 근거 없음 판정이 agent 탓인지 배치 탓인지 가릴 수 없다.
DOC_CHARS = None


def _chunks(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


def _history_text(history) -> str:
    if not history:
        return "(없음)"
    return "\n".join(f"사용자: {t['사용자']}\n에이전트: {t['에이전트']}" for t in history)


LINE_CHARS = 800


def _wrap(text: str) -> str:
    """긴 줄을 나눈다. 판정자가 쓰는 파일 읽기 도구는 한 줄이 2,000자를 넘으면 뒤를 자른다.
    그러면 문서를 자르지 않아도 판정자가 못 보는 부분이 다시 생긴다. 글자는 하나도 빼지 않는다."""
    out = []
    for line in text.splitlines():
        out += [line[i:i + LINE_CHARS] for i in range(0, max(len(line), 1), LINE_CHARS)]
    return "\n".join(out)


def _source_text(source) -> str:
    parts = []
    for i, result in enumerate(source["tool_results"], 1):
        parts.append(f"[조회 결과 {i}]\n" + json.dumps(result, ensure_ascii=False, indent=1))
    for i, doc in enumerate(source["documents"], 1):
        parts.append(f"[문서 {i}] {doc['source']}\n{_wrap((doc['content'] or '')[:DOC_CHARS])}")
    return "\n\n".join(parts) or "(원자료 없음 — 조회도 검색도 하지 않았다)"


def _trajectory_text(trace) -> str:
    lines = [f"input: {trace['question']}"]
    if trace["history"]:
        lines.append("history:\n" + _history_text(trace["history"]))
    for s in trace["steps"]:
        # guardrail_details 는 사후 분석용이다. 궤적 judge 입력을 이전 실행과 같게 유지한다
        rest = {k: v for k, v in s.items() if k not in ("node", "guardrail_details")}
        lines.append(f"- {s['node']} {json.dumps(rest, ensure_ascii=False)}")
    lines.append(f"final output: {trace['answer']}")
    return "\n".join(lines)


def write_answer_batches(traces, out: Path, prefix: str = "answer") -> None:
    out.mkdir(parents=True, exist_ok=True)
    answer_prompt = (PROMPTS / "answer_judge.txt").read_text(encoding="utf-8")
    for n, batch in enumerate(_chunks(traces, ANSWER_BATCH), 1):
        body = [answer_prompt, "", ANSWER_INSTRUCTION, ""]
        for case, trace in batch:
            behavior = "\n".join(f"- {b}" for b in case.expected_behavior) or "(없음)"
            body += [f'<case id="{case.id}">',
                     f"<history>\n{_history_text(trace['history'])}\n</history>",
                     f"<question>{trace['question']}</question>",
                     f"<expected_behavior>\n{behavior}\n</expected_behavior>",
                     f"<source_data>\n{_source_text(trace['source_data'])}\n</source_data>",
                     f"<answer>\n{trace['answer']}\n</answer>",
                     "</case>", ""]
        (out / f"{prefix}_{n:02d}.md").write_text("\n".join(body), encoding="utf-8")


def write_batches(traces, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    write_answer_batches(traces, out)
    trajectory_prompt = (PROMPTS / "trajectory_judge.txt").read_text(encoding="utf-8")
    for n, batch in enumerate(_chunks(traces, TRAJECTORY_BATCH), 1):
        body = [trajectory_prompt, "", TRAJECTORY_INSTRUCTION, ""]
        for case, trace in batch:
            body += [f'<case id="{case.id}">', "<trajectory>",
                     _trajectory_text(trace), "</trajectory>", "</case>", ""]
        (out / f"trajectory_{n:02d}.md").write_text("\n".join(body), encoding="utf-8")


def write_sanity_batch(path: Path, out: Path) -> None:
    """judge_sanity.yaml → 배치 한 개 + 정답지.

    기대판정은 배치에 넣지 않는다. judge 가 답을 보고 채점하면 점검이 안 된다.
    정답지는 따로 저장해서 판정 결과와 사람이 대조한다.
    """
    import yaml

    cases = yaml.safe_load(path.read_text(encoding="utf-8"))
    prompt = (PROMPTS / "answer_judge.txt").read_text(encoding="utf-8")
    body = [prompt, "", ANSWER_INSTRUCTION, ""]
    for c in cases:
        behavior = "\n".join(f"- {b}" for b in c["기대동작"])
        body += [f'<case id="{c["id"]}">', "<history>\n(없음)\n</history>",
                 f"<question>{c['질문']}</question>",
                 f"<expected_behavior>\n{behavior}\n</expected_behavior>",
                 f"<source_data>\n{c['원자료']}\n</source_data>",
                 f"<answer>\n{c['답변']}\n</answer>", "</case>", ""]
    out.mkdir(parents=True, exist_ok=True)
    (out / "sanity_batch.md").write_text("\n".join(body), encoding="utf-8")
    key = [f"{c['id']}  {c['기대판정']}  {c.get('어긴규칙', '')}" for c in cases]
    (out / "sanity_answer_key.txt").write_text("\n".join(key) + "\n", encoding="utf-8")


def rebuild(run_dir: Path) -> None:
    """저장된 traces 로 배치를 다시 만든다. 에이전트를 다시 돌리지 않는다."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from case import load_cases

    root = Path(__file__).resolve().parents[1]
    cases = {c.id: c for c in load_cases(root)}
    traces = []
    for f in sorted((run_dir / "traces").glob("*.json")):
        t = json.loads(f.read_text(encoding="utf-8"))
        traces.append((cases[t["id"]], t))
    write_batches(traces, run_dir / "judge")


if __name__ == "__main__":
    import sys

    root = Path(__file__).resolve().parents[1]
    if len(sys.argv) > 1:
        rebuild(Path(sys.argv[1]))
        print(Path(sys.argv[1]) / "judge")
    else:
        write_sanity_batch(root / "judge_sanity.yaml", root / "runs" / "sanity")
        print(root / "runs" / "sanity")
