"""세 판정을 케이스마다 결과 카드 한 장으로 합치고, 요약표를 만든다.

    python e2e_test_case/harness/cards.py e2e_test_case/runs/<시각>

읽는 것
    deterministic.json               결정론
    traces/<id>.json                 실행 기록
    judge/answer_NN.result.md        답변 judge 판정
    judge/trajectory_NN.result.md    궤적 judge 판정

쓰는 것
    core/<id>.md · edge/<id>.md      결과 카드
    README.md                        요약표

최종 통과는 세 판정이 모두 PASS 일 때다. 판정이 빠진 케이스는 최종 판정을 내리지 않고
"판정 없음" 으로 센다 — 빠진 것을 FAIL 로 치면 judge 오류가 agent 점수로 들어간다.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from batches import VIOLATION_KEYS  # noqa: E402
from case import load_cases  # noqa: E402

CASE_RE = re.compile(r'<case id="([^"]+)">(.*?)</case>', re.S)
TAG_RE = {t: re.compile(rf"<{t}>(.*?)</{t}>", re.S) for t in ("evidence", "result", "violations")}

DET_CATEGORY = [
    ("route:", "route 오분류"),
    ("부르면 안 되는데", "도구없음 위반"),
    ("필수 tool", "필수 tool 누락"),
    ("금지 tool", "금지 tool 호출"),
    ("(첫 호출)", "기대인자 불일치"),
    ("말하지 않은 조건", "인자 날조"),
]
AREA = {("product_recommendation",): "상품", ("exchange_rate",): "환율",
        ("policy_qa",): "규정", ("out_of_scope",): "범위 밖"}


def parse_results(folder: Path, prefix: str) -> dict:
    out = {}
    for f in sorted(folder.glob(f"{prefix}_*.result.md")):
        for cid, body in CASE_RE.findall(f.read_text(encoding="utf-8")):
            got = {t: (m.group(1).strip() if (m := r.search(body)) else None)
                   for t, r in TAG_RE.items()}
            result = (got["result"] or "").upper()
            got["result"] = "PASS" if "PASS" in result else "FAIL" if "FAIL" in result else None
            v = (got["violations"] or "").lower()
            got["violations"] = [] if v in ("", "none") else [
                x.strip() for x in v.split(",") if x.strip() in VIOLATION_KEYS]
            out[cid] = got
    return out


def _mark(v):
    return {"PASS": "PASS", "FAIL": "**FAIL**", None: "판정 없음"}[v]


def _frac(items, key):
    judged = [x for x in items if key(x) is not None]
    return f"{sum(1 for x in judged if key(x))}/{len(judged)}" + (
        f" (판정 없음 {len(items) - len(judged)})" if len(judged) < len(items) else "")


def main(run_dir: Path) -> None:
    cases = {c.id: c for c in load_cases(HERE.parent)}
    det_raw = json.loads((run_dir / "deterministic.json").read_text(encoding="utf-8"))
    det = {r["case_id"]: r for r in det_raw["results"]}
    answer = parse_results(run_dir / "judge", "answer")
    # 배치 버그로 다시 판정한 케이스는 재판정 결과를 쓴다. 첫 판정 파일은 기록으로 남겨 둔다
    rejudged = parse_results(run_dir / "judge", "rejudge_answer")
    answer.update(rejudged)
    trajectory = parse_results(run_dir / "judge", "trajectory")

    rows = []
    for cid, d in det.items():
        case = cases[cid]
        trace = json.loads((run_dir / "traces" / f"{cid}.json").read_text(encoding="utf-8"))
        a, t = answer.get(cid, {}), trajectory.get(cid, {})
        verdicts = [("PASS" if d["passed"] else "FAIL"), t.get("result"), a.get("result")]
        final = None if None in verdicts else all(v == "PASS" for v in verdicts)
        row = {"id": cid, "case": case, "det": d["passed"], "det_reasons": d["reasons"],
               "traj": t.get("result"), "ans": a.get("result"),
               "violations": a.get("violations", []), "final": final,
               "area": AREA.get(tuple(case.expected_route), "복수 허용")}
        rows.append(row)

        calls = " → ".join(
            f"`{c['name']}` {json.dumps(c['args'], ensure_ascii=False)}"
            + (f" ✗{c['error']}" if c.get("error") else "") for c in trace["tool_calls"]) or "(tool 호출 없음)"
        flags = []
        if not d["passed"] and t.get("result") == "PASS":
            flags.append("결정론 FAIL · 궤적 PASS → 라벨을 다시 본다")
        if d["passed"] and a.get("result") == "FAIL":
            flags.append("결정론 PASS · 답변 FAIL → 행동은 맞고 답이 틀렸다. 기대동작이 과한지도 본다")
        hist = "\n".join(f"> 사용자: {h['사용자']}  \n> 에이전트: {h['에이전트']}" for h in trace["history"])
        card = [
            f"# {cid} — {_mark('PASS' if final else 'FAIL' if final is False else None)}", "",
            f"**질문** {case.question}", "",
            *([hist, ""] if hist else []),
            f"{case.tier} · {case.question_type}" + (f" · {', '.join(case.tags)}" if case.tags else ""), "",
            "## 실행", "",
            f"- route: `{trace['route']}`",
            f"- 호출: {calls}", "",
            "## ① 결정론 — " + _mark("PASS" if d["passed"] else "FAIL"), "",
            *([f"- {r}" for r in d["reasons"]] or ["- 모든 항목 통과"]), "",
            "## ② 궤적 judge — " + _mark(t.get("result")), "",
            (t.get("evidence") or "(판정 없음)"), "",
            "## ③ 답변 judge — " + _mark(a.get("result"))
            + (" (재판정 — 첫 판정은 문서를 700자로 자른 배치로 했다)" if cid in rejudged else ""), "",
            *([f"위반: {', '.join(VIOLATION_KEYS[v] for v in a['violations'])}", ""]
              if a.get("violations") else []),
            (a.get("evidence") or "(판정 없음)"), "",
            *(["## 불일치", "", *[f"- {f}" for f in flags], ""] if flags else []),
            "## 최종 답변", "", (trace["answer"] or "(없음)"), "",
            "## 기대동작", "", *[f"- {b}" for b in case.expected_behavior], "",
        ]
        folder = run_dir / case.tier
        folder.mkdir(exist_ok=True)
        (folder / f"{cid}.md").write_text("\n".join(card), encoding="utf-8")

    # ── 요약표 ──────────────────────────────────────────────────────────
    def line(name, sub):
        return (f"| {name} | {_frac(sub, lambda r: r['det'])} | {_frac(sub, lambda r: None if r['traj'] is None else r['traj'] == 'PASS')} "
                f"| {_frac(sub, lambda r: None if r['ans'] is None else r['ans'] == 'PASS')} | {_frac(sub, lambda r: r['final'])} |")

    head = ["| | 결정론 | 궤적 | 답변 | 최종 |", "| --- | --- | --- | --- | --- |"]
    out = [f"# e2e 결과 — {run_dir.name}", "",
           "퍼센트가 아니라 분수로 쓴다. 태그별 숫자는 문제가 적어 측정이 아니라 탐침이다.", "",
           "## 전체", "", *head, line("전체", rows),
           line("core", [r for r in rows if r["case"].tier == "core"]),
           line("edge", [r for r in rows if r["case"].tier == "edge"]), "",
           "## 영역", "", *head,
           *[line(a, [r for r in rows if r["area"] == a])
             for a in ("상품", "규정", "환율", "범위 밖", "복수 허용")
             if any(r["area"] == a for r in rows)], "",
           "## 태그 (탐침)", "", *head,
           *[line(t, [r for r in rows if t in r["case"].tags])
             for t in sorted({t for r in rows for t in r["case"].tags})], ""]

    det_fail = Counter(label for r in rows for reason in r["det_reasons"]
                       for key, label in DET_CATEGORY if key in reason)
    out += ["## 결정론 실패 원인", ""] + (
        [f"- {k}: {v}건" for k, v in det_fail.most_common()] or ["- 없음"]) + [""]

    vio = Counter(v for r in rows for v in r["violations"])
    out += ["## 답변 위반 규칙", ""] + (
        [f"- {VIOLATION_KEYS[k]}: {v}건" for k, v in vio.most_common()] or ["- 없음"]) + [""]

    d_fail_t_pass = [r["id"] for r in rows if not r["det"] and r["traj"] == "PASS"]
    d_pass_a_fail = [r["id"] for r in rows if r["det"] and r["ans"] == "FAIL"]
    out += ["## 평가자 불일치", "",
            f"- 결정론 FAIL · 궤적 PASS ({len(d_fail_t_pass)}) — 라벨 의심: {', '.join(d_fail_t_pass) or '없음'}",
            f"- 결정론 PASS · 답변 FAIL ({len(d_pass_a_fail)}) — 행동은 맞고 답이 틀림: {', '.join(d_pass_a_fail) or '없음'}", "",
            "## 실패 케이스", ""]
    out += [f"- [{r['id']}]({r['case'].tier}/{r['id']}.md) {r['case'].question} — "
            + " · ".join(n for n, ok in (("결정론", r["det"]), ("궤적", r["traj"] != "FAIL"),
                                         ("답변", r["ans"] != "FAIL")) if not ok)
            for r in rows if r["final"] is False] or ["- 없음"]
    out += ["", "## 조건", "",
            f"- 인프라 오류로 제외: {len(det_raw.get('infra_excluded', []))}건",
            f"- 답변 판정 재실행: {len(rejudged)}건 — 첫 배치가 RAG 문서를 청크당 700자로 잘라서 judge 가 "
            "근거를 못 보고 '문서에 없다' 로 판정했다. 문서 전문을 넣어 그 케이스만 다시 판정했다. "
            "agent · 문제 카드 · judge 프롬프트는 바꾸지 않았다. 첫 판정은 judge/answer_*.result.md 에 남아 있다",
            "- 케이스는 Claude 가 작성했다. 실사용 발화가 아니다",
            "- judge 는 Claude(Opus) 서브에이전트. 배치마다 새로 띄우고 배치 파일 하나만 읽게 했다",
            "- 외부 API 를 녹화하지 않았다. 금리·환율은 실행한 날 기준이다", ""]
    (run_dir / "README.md").write_text("\n".join(out), encoding="utf-8")
    print(run_dir / "README.md")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
