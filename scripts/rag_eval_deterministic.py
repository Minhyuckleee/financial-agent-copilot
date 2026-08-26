"""RAG 결정론적 지표(Recall/MRR/Precision) — LLM 미사용, 코드로만 계산.

골든셋(기본값 `data/eval/rag_golden_set_train.json`) 질문을 그대로 `retrieve()`에 넣고
`THRESHOLD_LOW` 필터까지 적용한 뒤(실제 `context.py` 파이프라인과 동일한 최종 후보군),
남은 청크ID가 정답청크ID(`ground_truth_chunk_ids`)를 포함하는지 본다. query rewrite(LLM
호출 필요)는 의도적으로 거치지 않는다 — 이 스크립트는 순수 검색 품질만 LLM 없이 측정하는
게 목적이라 질문 원문을 그대로 쓴다. "@3" 라벨은 강제 truncate가 없어져 더 이상 정확하지
않으므로 뗐다 — top_n=3 후보풀 기준이나 최종 반환 개수는 confidence 필터 후
0~6개 가변. 필터로 0개가 남는 문항은 Recall=0/Precision=0/MRR=0으로 처리한다.

train(120개, threshold_low 실측에 이미 소모된 데이터)/test(40개)/valid(40개) 분리됨
— train으로 계속 튜닝했던 값을 test/valid로 재검증할 때는
`--split test`/`--split valid`로 실행한다.

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/rag_eval_deterministic.py [--split train|test|valid]
"""
import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("HF_TOKEN", "dummy")  # 로컬 손상된 HF 토큰캐시 우회

from rag.retriever import THRESHOLD_LOW, retrieve

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"


def _reciprocal_rank(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    for rank, cid in enumerate(retrieved_ids, start=1):
        if cid in relevant_ids:
            return 1.0 / rank
    return 0.0


def evaluate(golden_set: list[dict]) -> dict:
    per_query = []
    for item in golden_set:
        relevant_ids = set(item["ground_truth_chunk_ids"])
        retrieved = [c for c in retrieve(item["question"]) if c["confidence"] >= THRESHOLD_LOW]
        retrieved_ids = [c["id"] for c in retrieved]

        hit = any(cid in relevant_ids for cid in retrieved_ids)
        precision = sum(1 for cid in retrieved_ids if cid in relevant_ids) / len(retrieved_ids) if retrieved_ids else 0.0
        rr = _reciprocal_rank(retrieved_ids, relevant_ids)

        per_query.append(
            {
                "id": item["id"],
                "question": item["question"],
                "retrieved": [
                    {"id": c["id"], "confidence": round(c["confidence"], 4), "relevant": c["id"] in relevant_ids}
                    for c in retrieved
                ],
                "retrieved_ids": retrieved_ids,
                "relevant_ids": sorted(relevant_ids),
                "recall_hit": hit,
                "precision": precision,
                "reciprocal_rank": rr,
            }
        )

    n = len(per_query)
    summary = {
        "n": n,
        "recall": sum(p["recall_hit"] for p in per_query) / n,
        "precision": sum(p["precision"] for p in per_query) / n,
        "mrr": sum(p["reciprocal_rank"] for p in per_query) / n,
        "empty_after_filter": sum(1 for p in per_query if not p["retrieved_ids"]),
    }
    return {"summary": summary, "per_query": per_query}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["train", "test", "valid"], default="train")
    args = parser.parse_args()

    golden_set_path = EVAL_DIR / f"rag_golden_set_{args.split}.json"
    results_path = EVAL_DIR / f"rag_deterministic_results_{args.split}.json"

    golden_set = json.loads(golden_set_path.read_text(encoding="utf-8"))
    print(f"골든셋({args.split}) {len(golden_set)}문항 로드, retrieve() 실행 중...")

    result = evaluate(golden_set)

    results_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    s = result["summary"]
    print(f"\nRecall:    {s['recall']:.4f}")
    print(f"Precision: {s['precision']:.4f}")
    print(f"MRR:       {s['mrr']:.4f}")
    print(f"필터 후 0개: {s['empty_after_filter']}/{s['n']}건")

    misses = [p for p in result["per_query"] if not p["recall_hit"]]
    if misses:
        print(f"\n미스 {len(misses)}건 (Recall@3 실패):")
        for m in misses:
            print(f"  - {m['id']}: {m['question']}")

    print(f"\n상세 결과 저장: {results_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
