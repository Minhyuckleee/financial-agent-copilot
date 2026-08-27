"""규칙⑤ cosine 유사도 재현 실험 — 정상/위조 각 50건의 claimed_phrase-chunk 코사인 유사도 range 비교.

`_check_grounding_llm`(현재 프로덕션, LLM entailment 판정)으로 전환하기 전 방식이었던
"임베딩 코사인 유사도로 근거검증"을 재현한다. 실제 코드는 이미 폐기돼 저장소에 없어(guardrail.py
주석 참고), `src/rag/embeddings/kure_embedder.py`(런타임과 동일 임베딩 모델)로 재구성한다.

계산 방식(사전에 고정, 결과 보고 나서 바꾸지 않음):
claimed_phrase 임베딩과 그 답변이 참조한 retrieved_contexts 각 chunk 임베딩의 코사인 유사도 중
최댓값(best-matching chunk) — cosine 방법에 가장 유리한 조건으로만 비교(그래도 갈리는지 보기 위함).

이 스크립트는 정확도(threshold 기반 분류)를 내지 않는다 — 정상/위조 두 그룹의 유사도 range가
겹치는지만 기술(descriptive)한다. threshold를 임의로 골라 accuracy를 내면 사후에 유리한 값을
고르는 것(overfitting to narrative)이 될 수 있어 여기서는 하지 않는다.

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/eval_citation_grounding_cosine_range.py
"""
import json
import statistics
from pathlib import Path

import numpy as np

from rag.embeddings.kure_embedder import KUREEmbedder

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"


def main() -> None:
    pool = json.loads((EVAL_DIR / "citation_grounding_pool100.json").read_text(encoding="utf-8"))
    embedder = KUREEmbedder(device="cpu", show_progress=True, batch_size=64)

    # 개별 encode() 호출 200회 대신 claim/청크 텍스트를 전부 모아 한 번에 배치 인코딩
    # (텍스트 중복 제거로 재계산도 줄인다) — 실행시간 단축용, 결과값 자체는 동일.
    claim_texts = [item["claimed_phrase"] for item in pool]
    all_chunk_texts = sorted({c["content"] for item in pool for c in item["chunks"]})
    chunk_index = {text: i for i, text in enumerate(all_chunk_texts)}

    print(f"claim {len(claim_texts)}개, 고유 chunk {len(all_chunk_texts)}개 임베딩 계산 중...")
    claim_embs = embedder.embed_batch(claim_texts)
    chunk_embs = embedder.embed_batch(all_chunk_texts) if all_chunk_texts else np.array([])

    results = []
    for item, claim_emb in zip(pool, claim_embs):
        chunk_texts = [c["content"] for c in item["chunks"]]
        if not chunk_texts:
            continue
        idxs = [chunk_index[t] for t in chunk_texts]
        item_chunk_embs = chunk_embs[idxs]
        sims = embedder.compute_similarity(claim_emb, item_chunk_embs)
        max_sim = float(np.max(sims))
        results.append({"id": item["id"], "group": item["group"], "max_cosine": max_sim})
        print(f"[{item['group']}] {item['id']}: {max_sim:.4f}")

    normal_scores = [r["max_cosine"] for r in results if r["group"] == "normal"]
    forged_scores = [r["max_cosine"] for r in results if r["group"] == "forged"]

    summary = {
        "normal": {
            "n": len(normal_scores),
            "min": min(normal_scores),
            "max": max(normal_scores),
            "mean": statistics.mean(normal_scores),
            "stdev": statistics.stdev(normal_scores),
        },
        "forged": {
            "n": len(forged_scores),
            "min": min(forged_scores),
            "max": max(forged_scores),
            "mean": statistics.mean(forged_scores),
            "stdev": statistics.stdev(forged_scores),
        },
    }
    overlap_lo = max(summary["normal"]["min"], summary["forged"]["min"])
    overlap_hi = min(summary["normal"]["max"], summary["forged"]["max"])
    summary["overlap_range"] = [overlap_lo, overlap_hi] if overlap_hi >= overlap_lo else None
    # 위조 점수 중 정상 range 안에 묻힌(=cosine으로 구분 불가한) 비율
    n_lo, n_hi = summary["normal"]["min"], summary["normal"]["max"]
    buried = sum(1 for s in forged_scores if n_lo <= s <= n_hi)
    summary["forged_buried_in_normal_range"] = {"count": buried, "total": len(forged_scores)}

    out = {"per_item": results, "summary": summary}
    out_path = EVAL_DIR / "citation_grounding_cosine_range_results.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== 정상(그라운드 정답) ===")
    print(f"  n={summary['normal']['n']} range=[{summary['normal']['min']:.4f}, {summary['normal']['max']:.4f}] mean={summary['normal']['mean']:.4f}")
    print("=== 위조 ===")
    print(f"  n={summary['forged']['n']} range=[{summary['forged']['min']:.4f}, {summary['forged']['max']:.4f}] mean={summary['forged']['mean']:.4f}")
    print(f"\n겹치는 구간: {summary['overlap_range']}")
    print(f"위조 중 정상 range에 묻힌 건수: {buried}/{len(forged_scores)}")
    print(f"\n저장: {out_path}")


if __name__ == "__main__":
    main()
