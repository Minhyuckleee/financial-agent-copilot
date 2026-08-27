"""규칙⑤ cosine-vs-LLM 비교 실험용 위조(negative) 40건 추가 생성.

기존 `build_citation_grounding_negatives.py`의 10건(5실패유형 x train/test 각 1개)은
표본이 너무 작아(scripts/README.md 참고) cosine range 비교에 쓰기엔 부족하다. 이 스크립트는
같은 5가지 실패유형을 RAGAS 실행 결과 중 아직 negative 시드로 안 쓴 질문 75개 풀에서
40개(유형당 8개)를 뽑아 LLM 초안 생성 방식으로 확장한다.

방법론(사람이 라벨 검증한다는 원칙 유지):
1. 소스 질문·chunk는 실제 파이프라인 RAGAS 결과에서 그대로 재사용(조작 없음)
2. 위조 claim 문장 자체는 LLM에게 실패유형별 few-shot(기존 10건 중 하나)을 주고 초안 생성시킴
   — "정답 라벨을 매기는 것"과 "위조 문장 초안을 쓰는 것"은 다른 작업이라 순환논리 아님
   (정답 라벨 자체는 "의도적으로 틀리게 저술했다"는 구성으로 이미 확정됨 — 원본 스크립트와 동일 논리)
3. 생성 직후 이 스크립트가 최소 검증(원문 chunk에 실제로 없는 내용인지 문자열 포함 여부로 1차 필터)을
   거치고, 사람이 표본 스팟체크로 2차 확인한다(별도로 수행)

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/build_citation_grounding_negatives_extra.py
"""
import json
import random
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env")

from graph.llm import get_llm  # noqa: E402

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"
RAG_DIR = ROOT / "data" / "rag"

_USED_SOURCE_IDS = {
    "gs_001", "gs_007", "gs_009", "gs_005", "gs_010",
    "gs_test_006", "gs_test_003", "gs_test_005", "gs_test_002", "gs_test_008",
}

_FAILURE_TYPES = [
    "완전 무관 내용",
    "숫자 바꿔치기",
    "근거조항 바꿔치기",
    "없는 세부조항 날조",
    "결론 반전",
]

_FAILURE_INSTRUCTIONS = {
    "완전 무관 내용": (
        "아래 문서와 주제만 살짝 겹치되, 문서에 전혀 나오지 않는 별개의 규정을 하나 지어내 "
        "사실인 것처럼 한 문장으로 서술하세요. 문서의 조항번호나 숫자를 가져다 쓰지 마세요."
    ),
    "숫자 바꿔치기": (
        "아래 문서에 나오는 기간·금액·비율 등 숫자를 하나 골라, 그 숫자만 다른 값으로 바꿔서 "
        "나머지 문맥은 그대로 유지한 문장을 쓰세요(예: 5년→3년). 무엇을 바꿨는지 티나지 않게 "
        "자연스러운 문장으로 쓰세요."
    ),
    "근거조항 바꿔치기": (
        "아래 문서의 실제 내용은 맞게 서술하되, 그 근거로 실제와 다른 조항번호·법령명을 "
        "괄호 등으로 붙이세요(예: 실제론 제14조인데 제17조라고 표기)."
    ),
    "없는 세부조항 날조": (
        "아래 문서의 전체적인 주제와는 어울리지만, 문서에는 나오지 않는 세부 절차·요건을 "
        "구체적인 숫자(기한·횟수 등)까지 붙여서 지어내 사실인 것처럼 서술하세요."
    ),
    "결론 반전": (
        "아래 문서의 결론(가능/불가능, 해야 함/안 해도 됨 등)을 정반대로 뒤집어서, 그 외 "
        "세부사항(주체·상황 설명)은 문서 내용을 그대로 살려 자연스러운 문장으로 쓰세요."
    ),
}

_FEWSHOT = {
    "완전 무관 내용": "대출 이자 관련 분쟁은 대출 실행일로부터 5년이 지나면 소멸시효가 완성되어 더 이상 다툴 수 없다.",
    "숫자 바꿔치기": "대출계약이 성립한 날부터 5년 이내에 상환하는 경우에는 중도상환수수료를 부과할 수 없다.",
    "근거조항 바꿔치기": "보호법 제17조 제1항에 따라 개인정보 처리 업무 위탁 계약을 맺은 경우 민감정보 및 고유식별정보 처리 업무를 위탁할 수 있다.",
    "없는 세부조항 날조": "은행이 예금성 상품 계약을 권유하기 최소 3영업일 전에 서면으로 고객의 재산상황과 투자경험을 사전 고지받아야 한다는 규정이 있다.",
    "결론 반전": "개인정보처리자는 전화상으로는 개인정보 수집에 대한 정보주체의 동의를 받을 수 없고, 반드시 서면으로만 받아야 한다.",
}


def _load_content_to_id() -> dict[str, str]:
    chunks = json.loads((RAG_DIR / "chunks_2300.json").read_text(encoding="utf-8"))
    return {c["content"]: c["id"] for c in chunks}


def _load_pool() -> list[dict]:
    pool = []
    for split in ["train", "test"]:
        d = json.loads((EVAL_DIR / f"rag_ragas_results_{split}.json").read_text(encoding="utf-8"))
        for sid, rec in zip(d["summary"]["sample_ids"], d["per_query"]):
            ctxs = [c for c in rec["retrieved_contexts"] if c]
            if ctxs and sid not in _USED_SOURCE_IDS:
                pool.append({"id": sid, "question": rec["user_input"], "retrieved_contexts": ctxs})
    return pool


def _generate_claim(failure_type: str, contexts: list[str]) -> str:
    llm = get_llm()
    chunks_text = "\n\n---\n\n".join(contexts)
    prompt = (
        "당신은 가드레일 판정기(규칙⑤ citation grounding) 테스트용 '위조 답변' 샘플을 만드는 "
        "중입니다. 아래 문서를 참고해, 지시된 실패유형에 맞는 한 문장짜리 위조 주장을 "
        "작성하세요. 은행 상담직원이 실제로 말할 법한 어투로, 그럴듯하지만 문서와는 다른(또는 "
        "문서에 없는) 내용이어야 합니다. 문장만 출력하세요(따옴표·설명 없이).\n\n"
        f"실패유형: {failure_type}\n지시사항: {_FAILURE_INSTRUCTIONS[failure_type]}\n\n"
        f"참고 예시(다른 문서 기준, 스타일만 참고): {_FEWSHOT[failure_type]}\n\n"
        f"문서:\n{chunks_text}"
    )
    return llm.invoke(prompt).content.strip().strip('"')


def build() -> list[dict]:
    pool = _load_pool()
    random.seed(42)
    random.shuffle(pool)
    selected = pool[:40]
    content_to_id = _load_content_to_id()

    items = []
    for i, entry in enumerate(selected):
        failure_type = _FAILURE_TYPES[i % 5]
        claim = _generate_claim(failure_type, entry["retrieved_contexts"])

        # 1차 필터: 생성된 claim이 원문 chunk 문장을 그대로 베낀 표절(=사실은 grounded)이면 제외 대상 —
        # 통째로 원문에 포함되면 위조가 아니라 정상 인용이라 실패유형이 성립 안 함.
        if claim in "\n".join(entry["retrieved_contexts"]):
            print(f"[SKIP] {entry['id']} ({failure_type}) — 생성된 claim이 원문과 동일, 위조 아님")
            continue

        chunk_ids = [content_to_id.get(c, "UNKNOWN") for c in entry["retrieved_contexts"]]
        chunks = [{"id": cid, "content": c} for cid, c in zip(chunk_ids, entry["retrieved_contexts"])]

        items.append(
            {
                "id": f"neg_extra_{entry['id']}",
                "source_query_id": entry["id"],
                "question": entry["question"],
                "failure_type": failure_type,
                "claimed_phrase": claim,
                "retrieved_contexts": entry["retrieved_contexts"],
                "chunks": chunks,
                "grounded": False,
            }
        )
        print(f"[{i+1}/40] {entry['id']} ({failure_type}): {claim[:60]}...")

    return items


def main() -> None:
    items = build()
    out_path = EVAL_DIR / "citation_grounding_negatives_extra.json"
    out_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n저장: {out_path} ({len(items)}건)")


if __name__ == "__main__":
    main()
