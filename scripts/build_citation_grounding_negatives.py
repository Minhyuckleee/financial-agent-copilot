"""규칙⑤ LLM entailment 판정기 정확도 검증용 negative(진짜 근거없는 claim) — train/test.

자연채굴(실제 파이프라인 답변 중 저신뢰 케이스 mining)로는 negative가 하나도 안 잡혀서
(train 39건 중 최저 유사도 3건도 전부 정상 paraphrase였음), 실패유형별로
직접 seed-answer를 작성한다. 질문·chunk pool은 실제 골든셋(train/test)에서 가져오고,
claim만 의도적으로 틀리게 저술한다(5가지 서로 다른 실패유형).

test 시드는 train과 **다른 소스 질문/chunk**로 구성한다(held-out) — 같은 5가지 실패유형이
train에서만 본 특정 chunk가 아니라 새로운 내용에도 일반화되는지 확인하기 위함.

`_check_grounding_llm`(difflib/임베딩 폐기 후 LLM entailment 직접판정으로
전환된 운영 로직 그대로)이 실제로 negative를 잡아내는지 검증한다. `grounded=False`는
의도적으로 틀리게 저술했다는 구성 자체가 정답 라벨이다.

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/build_citation_grounding_negatives.py --split train
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


# (source_query_id, 실패유형, 조작된 claim) — chunk pool은 source_query_id의 실제 retrieved_contexts 그대로 재사용
SEEDS_TRAIN = [
    (
        "gs_001",
        "완전 무관 내용",
        "대출 이자 관련 분쟁은 대출 실행일로부터 5년이 지나면 소멸시효가 완성되어 더 이상 다툴 수 없다.",
    ),
    (
        "gs_007",
        "숫자 바꿔치기",
        "대출계약이 성립한 날부터 5년 이내에 상환하는 경우에는 중도상환수수료를 부과할 수 없다.",
    ),
    (
        "gs_009",
        "근거조항 바꿔치기",
        "보호법 제17조 제1항에 따라 개인정보 처리 업무 위탁 계약을 맺은 경우 민감정보 및 고유식별정보 처리 업무를 위탁할 수 있다.",
    ),
    (
        "gs_005",
        "없는 세부조항 날조",
        "은행이 예금성 상품 계약을 권유하기 최소 3영업일 전에 서면으로 고객의 재산상황과 투자경험을 사전 고지받아야 한다는 규정이 있다.",
    ),
    (
        "gs_010",
        "결론 반전",
        "개인정보처리자는 전화상으로는 개인정보 수집에 대한 정보주체의 동의를 받을 수 없고, 반드시 서면으로만 받아야 한다.",
    ),
]

# held-out — train과 다른 소스(gs_test_*)로 구성, 같은 5가지 실패유형을 새 내용에 적용
SEEDS_TEST = [
    (
        "gs_test_006",
        "완전 무관 내용",
        "개인정보 유출 사고가 발생한 경우 개인정보처리자는 72시간 이내에 정보주체에게 통지해야 한다.",
    ),
    (
        "gs_test_003",
        "숫자 바꿔치기",
        "계약이 체결되지 않은 경우 제공받은 고객정보는 10일 이내에 파기하여야 한다.",
    ),
    (
        "gs_test_005",
        "근거조항 바꿔치기",
        "수탁자는 위탁받은 업무 범위를 초과하여 개인정보를 이용하거나 제3자에게 제공해서는 안 된다. (법 제17조 ⑤)",
    ),
    (
        "gs_test_002",
        "없는 세부조항 날조",
        "홈페이지에 공개된 개인정보를 동의 없이 수집·이용하려면 사전에 정보주체에게 서면으로 통지하고 7일간 이의제기 기간을 두어야 한다는 규정이 있다.",
    ),
    (
        "gs_test_008",
        "결론 반전",
        "고객이 의식을 잃는 등 긴급한 상황이라도 가족에게 연락하기 위해 정보주체의 동의 없이 개인정보를 제공하는 것은 허용되지 않는다.",
    ),
]


def build(split: str) -> list[dict]:
    seeds = SEEDS_TRAIN if split == "train" else SEEDS_TEST
    # citation_grounding_dataset_{split}.json이 아니라 RAGAS 원본에서 직접 가져온다 — 그 파일은
    # "claim 있는 답변만" 필터링돼있고 그 필터 자체가 LLM 재호출 때마다 살짝 흔들릴 수 있어서
    # (예: gs_007이 재호출 때 claim 없음으로 재분류됨) 시드 소스 조회를 그 결과에 의존하면 깨진다.
    ragas = json.loads((EVAL_DIR / f"rag_ragas_results_{split}.json").read_text(encoding="utf-8"))
    by_id = {
        sid: {"question": rec["user_input"], "retrieved_contexts": [c for c in rec["retrieved_contexts"] if c]}
        for sid, rec in zip(ragas["summary"]["sample_ids"], ragas["per_query"])
    }
    content_to_id = _load_content_to_id()

    items = []
    correct = 0
    for source_id, failure_type, claim in seeds:
        source = by_id[source_id]
        contexts = source["retrieved_contexts"]
        chunk_ids = [content_to_id[c] for c in contexts]
        chunks = [{"id": cid, "content": c} for cid, c in zip(chunk_ids, contexts)]

        result = _check_grounding_llm(claim, chunks)
        predicted_grounded = result.grounded
        is_correct = predicted_grounded is False
        correct += is_correct
        items.append(
            {
                "id": f"neg_{source_id}",
                "source_query_id": source_id,
                "question": source["question"],
                "failure_type": failure_type,
                "claimed_phrase": claim,
                "predicted_grounded": predicted_grounded,
                "retrieved_contexts": contexts,
                "grounded": False,  # 의도적으로 틀리게 저술함 — 구성 자체가 정답 라벨
            }
        )
        print(f"[{'OK' if is_correct else 'MISS'}] {failure_type} ({source_id}) predicted_grounded={predicted_grounded}")

    print(f"[{split}] 정확도 {correct}/{len(items)}")
    return items


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["train", "test"], default="train")
    args = parser.parse_args()

    items = build(args.split)
    out_path = EVAL_DIR / f"citation_grounding_negatives_{args.split}.json"
    out_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장: {out_path} ({len(items)}건)")


if __name__ == "__main__":
    main()
