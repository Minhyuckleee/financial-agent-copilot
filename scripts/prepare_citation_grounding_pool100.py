"""cosine-vs-LLM 위조탐지율 비교 실험용 정상 50 + 위조 50 pool 구성.

정상 50 : 기존 `citation_grounding_dataset_{train,test}.json`(사람이 chunk 대조로 확정한
grounded=true 64건)에서 seed=42로 50건 샘플링. 새로 생성하지 않음 — 이미 검증 끝난 데이터라
표본만 맞춘다.

위조 50 : 기존 `citation_grounding_negatives_{train,test}.json`(10건, 5유형x2) +
`citation_grounding_negatives_extra.json`(40건, `build_citation_grounding_negatives_extra.py`로
생성) 합산.

두 그룹 모두 "text"(cosine 계산·LLM 판정에 넣을 전체 답변 텍스트)와 "chunks"(claim 추출
근거가 된 retrieved chunk 목록)를 통일된 스키마로 맞춘다.

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/prepare_citation_grounding_pool100.py
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"
RAG_DIR = ROOT / "data" / "rag"


def _load_content_to_id() -> dict[str, str]:
    chunks = json.loads((RAG_DIR / "chunks_2300.json").read_text(encoding="utf-8"))
    return {c["content"]: c["id"] for c in chunks}


def _build_normal_pool() -> list[dict]:
    items = []
    for split in ["train", "test"]:
        data = json.loads((EVAL_DIR / f"citation_grounding_dataset_{split}.json").read_text(encoding="utf-8"))
        for item in data:
            chunks = [{"id": None, "content": c} for c in item["retrieved_contexts"]]
            items.append(
                {
                    "id": item["id"],
                    "group": "normal",
                    "text": item["response"],
                    "claimed_phrase": item["claimed_phrase"],
                    "chunks": chunks,
                    "grounded": True,
                }
            )
    random.seed(42)
    random.shuffle(items)
    return items[:50]


def _build_forged_pool() -> list[dict]:
    items = []
    for split in ["train", "test"]:
        data = json.loads((EVAL_DIR / f"citation_grounding_negatives_{split}.json").read_text(encoding="utf-8"))
        for item in data:
            chunks = [{"id": None, "content": c} for c in item["retrieved_contexts"]]
            items.append(
                {
                    "id": item["id"],
                    "group": "forged",
                    "text": item["claimed_phrase"],
                    "claimed_phrase": item["claimed_phrase"],
                    "failure_type": item["failure_type"],
                    "chunks": chunks,
                    "grounded": False,
                }
            )
    extra = json.loads((EVAL_DIR / "citation_grounding_negatives_extra.json").read_text(encoding="utf-8"))
    for item in extra:
        items.append(
            {
                "id": item["id"],
                "group": "forged",
                "text": item["claimed_phrase"],
                "claimed_phrase": item["claimed_phrase"],
                "failure_type": item["failure_type"],
                "chunks": item["chunks"],
                "grounded": False,
            }
        )
    assert len(items) == 50, f"위조 pool 50건이어야 하는데 {len(items)}건"
    return items


def main() -> None:
    normal = _build_normal_pool()
    forged = _build_forged_pool()
    assert len(normal) == 50, f"정상 pool 50건이어야 하는데 {len(normal)}건"

    pool = normal + forged
    out_path = EVAL_DIR / "citation_grounding_pool100.json"
    out_path.write_text(json.dumps(pool, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장: {out_path} (정상 {len(normal)} + 위조 {len(forged)} = {len(pool)}건)")


if __name__ == "__main__":
    main()
