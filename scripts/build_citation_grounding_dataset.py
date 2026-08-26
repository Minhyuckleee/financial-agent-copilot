"""규칙⑤(citation grounding) LLM entailment 판정기 정확도 검증용 데이터 추출. — difflib/임베딩 코사인 둘 다 폐기되고 `_check_grounding_llm`(claim추출+
entailment판정을 한 콜에서 처리)로 전환되면서, 이 스크립트의 역할이 바뀌었다:
"threshold 스윕용 연속값"이 아니라 "**분류기(LLM) 예측이 실제 정답 라벨과 얼마나
일치하나**"를 재는 데이터를 만든다.

RAGAS 평가 시 이미 확보해둔 실제 파이프라인 출력(`response`+`retrieved_contexts`,
data/eval/rag_ragas_results_{split}.json)을 원재료로 재사용한다 — 새로 그래프를 돌리지
않는다(train/test 한정). `retrieved_contexts`는 content 문자열로만 남아있어 chunk_id가
없으므로 `chunks_2300.json`과 내용 대조로 복원한다.

`predicted_grounded`는 `_check_grounding_llm`이 직접 낸 판정(운영 코드와 완전히 동일한
경로) — 여기서 자동으로 채운다. `grounded`(사람이 chunk 원문 읽고 확정하는 정답 라벨)는
채우지 않는다 — 이후 별도 라벨링 단계에서 채워서 `predicted_grounded`와 대조해 정확도를
낸다.

기존 dataset 파일이 있으면 판정 결과를 재사용한다 — 불필요한 API 재호출을 피하기 위함.

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/build_citation_grounding_dataset.py --split train
"""
import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from graph.guardrail import _check_grounding_llm  # noqa: E402

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"
RAG_DIR = ROOT / "data" / "rag"


def _load_content_to_id() -> dict[str, str]:
    chunks = json.loads((RAG_DIR / "chunks_2300.json").read_text(encoding="utf-8"))
    return {c["content"]: c["id"] for c in chunks}


def build(split: str) -> list[dict]:
    source_path = EVAL_DIR / f"rag_ragas_results_{split}.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    content_to_id = _load_content_to_id()

    existing_path = EVAL_DIR / f"citation_grounding_dataset_{split}.json"
    existing_by_id = {}
    if existing_path.exists():
        for item in json.loads(existing_path.read_text(encoding="utf-8")):
            existing_by_id[item["id"]] = item

    items = []
    skipped_no_claim = 0
    skipped_no_context = 0
    skipped_unmapped_chunk = 0
    reused = 0
    for sample_id, record in zip(source["summary"]["sample_ids"], source["per_query"]):
        response = record["response"]

        contexts = [c for c in record["retrieved_contexts"] if c]  # threshold_low 필터로 0개 남으면 '' 플레이스홀더 하나만 옴
        if not contexts:
            skipped_no_context += 1  # 실제 파이프라인도 이 경우 규칙⑤ 자체를 안 돈다(guardrail.py:275)
            continue
        try:
            chunk_ids = [content_to_id[c] for c in contexts]
        except KeyError:
            skipped_unmapped_chunk += 1
            continue
        chunks = [{"id": cid, "content": c} for cid, c in zip(chunk_ids, contexts)]

        cached = existing_by_id.get(sample_id)
        if cached is not None and "predicted_grounded" in cached:  # 구 스키마(유사도 기반) 캐시는 재사용 안 함
            reused += 1
            claimed_phrase = cached["claimed_phrase"]
            predicted_grounded = cached["predicted_grounded"]
            grounded_label = cached.get("grounded")
        else:
            result = _check_grounding_llm(response, chunks)
            if not result.has_citation_claim or not result.claimed_phrase or result.claimed_phrase not in response:
                skipped_no_claim += 1
                continue
            claimed_phrase = result.claimed_phrase
            predicted_grounded = result.grounded
            grounded_label = None

        items.append(
            {
                "id": sample_id,
                "question": record["user_input"],
                "response": response,
                "claimed_phrase": claimed_phrase,
                "predicted_grounded": predicted_grounded,  # _check_grounding_llm의 실제 판정(운영 경로와 동일)
                "faithfulness": record.get("faithfulness"),  # 참고용 힌트일 뿐, 정답 아님
                "retrieved_contexts": contexts,
                "grounded": grounded_label,  # 사람이 chunk 읽고 채울 정답 라벨 — true/false
            }
        )

    print(
        f"[{split}] claim 있는 답변 {len(items)}개(재사용 {reused}건), "
        f"claim 없어서 제외 {skipped_no_claim}개, chunk 0개(has_no_context)라 해당없음 {skipped_no_context}개, "
        f"chunk_id 매칭 실패로 제외 {skipped_unmapped_chunk}개"
    )
    return items


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["train", "test"], default="train")
    args = parser.parse_args()

    items = build(args.split)
    out_path = EVAL_DIR / f"citation_grounding_dataset_{args.split}.json"
    out_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장: {out_path} ({len(items)}건, 정답 라벨링 대기 중)")


if __name__ == "__main__":
    main()
