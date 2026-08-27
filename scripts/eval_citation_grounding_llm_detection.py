"""규칙⑤ LLM entailment 판정기(`_check_grounding_llm`, 프로덕션 코드 그대로) 위조탐지율 측정 —
같은 정상 50 + 위조 50 pool 대상.

`_check_grounding_llm(text, chunks)`을 프로덕션 경로와 동일하게 호출한다(가드레일 우회나
mock 없음). 정상은 predicted_grounded == True가 나와야 정답(오탐 없음), 위조는
predicted_grounded == False가 나와야 정답(탐지 성공).

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/eval_citation_grounding_llm_detection.py
"""
import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env")

from graph.guardrail import _check_grounding_llm  # noqa: E402

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"


def main() -> None:
    pool = json.loads((EVAL_DIR / "citation_grounding_pool100.json").read_text(encoding="utf-8"))

    results = []
    for item in pool:
        chunks = [{"id": c.get("id"), "content": c["content"]} for c in item["chunks"]]
        result = _check_grounding_llm(item["text"], chunks)
        predicted = result.grounded
        correct = predicted == item["grounded"]
        results.append(
            {
                "id": item["id"],
                "group": item["group"],
                "expected_grounded": item["grounded"],
                "predicted_grounded": predicted,
                "has_citation_claim": result.has_citation_claim,
                "correct": correct,
            }
        )
        print(f"[{'OK' if correct else 'MISS'}] {item['group']} {item['id']}: predicted={predicted}")

    normal = [r for r in results if r["group"] == "normal"]
    forged = [r for r in results if r["group"] == "forged"]
    normal_correct = sum(r["correct"] for r in normal)
    forged_correct = sum(r["correct"] for r in forged)

    summary = {
        "normal": {"n": len(normal), "correct": normal_correct, "false_alarm": len(normal) - normal_correct},
        "forged": {"n": len(forged), "detected": forged_correct, "missed": len(forged) - forged_correct},
    }

    out = {"per_item": results, "summary": summary}
    out_path = EVAL_DIR / "citation_grounding_llm_detection_results.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== 정상 50건 (오탐 없어야 함) ===")
    print(f"  정상 판정(오탐 없음): {normal_correct}/{len(normal)}")
    print("=== 위조 50건 (탐지돼야 함) ===")
    print(f"  탐지 성공: {forged_correct}/{len(forged)}")
    print(f"\n저장: {out_path}")


if __name__ == "__main__":
    main()
