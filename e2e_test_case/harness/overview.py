"""카드 100장을 표 한 장(CASES.md)으로 모은다. 검토용이다. 카드를 고치면 다시 돌린다.

    python e2e_test_case/harness/overview.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from case import load_cases  # noqa: E402

SHORT = {"recommend_deposit_products": "예금", "recommend_credit_loan_products": "신용",
         "recommend_jeonse_loan_products": "전세", "recommend_mortgage_loan_products": "주담대",
         "recommend_business_loan_products": "사업자", "inquire_exchange_rate": "환율",
         "product_recommendation": "상품", "exchange_rate": "환율", "policy_qa": "규정",
         "out_of_scope": "범위밖"}


def _s(xs):
    return " ".join(SHORT.get(x, x) for x in xs)


def _args(d):
    out = []
    for tool, kv in d.items():
        for k, v in kv.items():
            v = f"~{v['포함']}" if isinstance(v, dict) else v
            k = {"save_term_months": "기간", "credit_score": "점수", "bank_name_filter": "은행"}.get(k, k)
            out.append(f"{SHORT.get(tool, tool)}.{k}={v}")
    return " ".join(out)


def main():
    cases = load_cases(HERE.parent)
    lines = ["# 케이스 목록", "",
             "`harness/overview.py` 가 만든 파일이다. 직접 고치지 말고 카드를 고친 뒤 다시 만든다.", "",
             "표기 — 필수 `+` · 금지 `-` · 금지인자 `!` · 부분 일치 `~` · 도구없음 `∅`", ""]
    for tier in ("core", "edge"):
        sub = [c for c in cases if c.tier == tier]
        lines += [f"## {tier} ({len(sub)})", "",
                  "| id | 질문 | 이력 | 태그 | route | 도구 | 인자 | 기대동작 |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for c in sub:
            tools = " ".join(["∅"] * c.no_tools + [f"+{_s([t])}" for t in c.required_tools]
                             + [f"-{_s([t])}" for t in c.forbidden_tools])
            args = " ".join(filter(None, [_args(c.expected_args)] + [
                f"!{SHORT.get(t, t)}.{'은행' if k == 'bank_name_filter' else k}"
                for t, ks in c.forbidden_args.items() for k in ks]))
            hist = " / ".join(t.사용자 for t in c.history)
            beh = "<br>".join(c.expected_behavior)
            lines.append(f"| {c.id} | {c.question} | {hist} | {' '.join(c.tags)} | "
                         f"{_s(c.expected_route)} | {tools} | {args} | {beh} |")
        lines.append("")
    (HERE.parent / "CASES.md").write_text("\n".join(lines), encoding="utf-8")
    print(HERE.parent / "CASES.md")


if __name__ == "__main__":
    main()
