"""RAGAS 4종(context precision/recall, faithfulness, answer relevancy) — 검색+생성 전체
파이프라인(StateGraph.invoke())을 돌린 뒤 OpenAI(gpt-4.1)를 judge로 사용해 측정한다.

이 프로젝트에서 LLM judge를 쓰는 유일한 지점 — 나머지 3개 route는
tool_result라는 구조화된 정답이 있어 가드레일 규칙④(코드 비교)로 이미 검증되지만, RAG는
검색된 비정형 텍스트에 답변이 근거했는지를 코드만으로 잴 수 없어 여기서만 LLM judge를 쓴다.

골든셋 120개 전부가 아니라 문서당 3개씩(17개 문서 × 3 = 51개) 층화샘플 사용 — 그래프
invoke()+judge 호출이 문항당 여러 번이라 전체를 돌리면 비용/시간이 과도함(사용자와 상의해
축소, 2026-08-12).

train(threshold_low 실측에 이미 소모된 120개)/test(40개)/valid(40개) 분리됨
— 기본값은 train, `--split test`/`--split valid`로 held-out 재검증 가능.

실행: PYTHONPATH=src PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/rag_eval_ragas.py [--split train|test|valid] [--full]
`--full`이면 층화샘플 없이 split 전량 사용(test/valid는 40개라 문서당3개 캡을 씌워도
37개로 거의 안 줄어서, 층화 자체를 생략하고 전량 쓰는 쪽을 택할 수 있음, 2026-08-16).
"""
import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("HF_TOKEN", "dummy")  # 로컬 손상된 HF 토큰캐시 우회

from dotenv import load_dotenv

load_dotenv()

from datasets import Dataset
from langchain_openai import ChatOpenAI
from ragas import evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness

from graph.builder import build_graph
from rag.embeddings.langchain_adapter import KureLangchainEmbeddings

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"
PER_SOURCE_N = 3


def _stratified_sample(golden_set: list[dict], per_source: int) -> list[dict]:
    """문서(source)당 앞에서부터 per_source개씩 선정 — 모든 문서를 빠짐없이 포함."""
    by_source: dict[str, list[dict]] = {}
    for item in golden_set:
        by_source.setdefault(item["source"], []).append(item)

    sample = []
    for items in by_source.values():
        sample.extend(items[:per_source])
    sample.sort(key=lambda x: x["id"])
    return sample


def _run_pipeline(graph, question: str) -> tuple[str, list[str]]:
    result = graph.invoke({"query": question})
    contexts = [c["content"] for c in result.get("retrieved_chunks", [])]
    return result.get("answer", ""), contexts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["train", "test", "valid"], default="train")
    parser.add_argument("--full", action="store_true", help="층화샘플 대신 split 전량 사용")
    args = parser.parse_args()

    golden_set_path = EVAL_DIR / f"rag_golden_set_{args.split}.json"
    results_path = EVAL_DIR / f"rag_ragas_results_{args.split}.json"

    golden_set = json.loads(golden_set_path.read_text(encoding="utf-8"))
    if args.full:
        sample = golden_set
        print(f"골든셋({args.split}) {len(golden_set)}개 전량 사용(층화샘플 안 함)")
    else:
        sample = _stratified_sample(golden_set, PER_SOURCE_N)
        n_sources = len({item["source"] for item in sample})
        print(f"골든셋({args.split}) {len(golden_set)}개 중 {len(sample)}개 층화샘플(문서 {n_sources}개 × {PER_SOURCE_N}개) 사용")

    graph = build_graph()

    rows = {"question": [], "answer": [], "contexts": [], "reference": []}
    for i, item in enumerate(sample, 1):
        print(f"  [{i}/{len(sample)}] invoke: {item['id']} - {item['question'][:40]}...")
        answer, contexts = _run_pipeline(graph, item["question"])
        rows["question"].append(item["question"])
        rows["answer"].append(answer)
        rows["contexts"].append(contexts or [""])
        rows["reference"].append(item["reference_answer"])

    dataset = Dataset.from_dict(rows)

    llm = LangchainLLMWrapper(ChatOpenAI(model=os.environ.get("OPENAI_MODEL", "gpt-4.1"), temperature=0))
    embeddings = LangchainEmbeddingsWrapper(KureLangchainEmbeddings())

    print("\nRAGAS evaluate() 실행 중 (OpenAI judge)...")
    result = evaluate(
        dataset=dataset,
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
        llm=llm,
        embeddings=embeddings,
    )

    df = result.to_pandas()
    summary = {
        "n": len(sample),
        "sample_ids": [item["id"] for item in sample],
        "context_precision": float(df["context_precision"].mean()),
        "context_recall": float(df["context_recall"].mean()),
        "faithfulness": float(df["faithfulness"].mean()),
        "answer_relevancy": float(df["answer_relevancy"].mean()),
    }

    results_path.write_text(
        json.dumps({"summary": summary, "per_query": df.to_dict(orient="records")}, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print(f"\ncontext_precision: {summary['context_precision']:.4f}")
    print(f"context_recall:    {summary['context_recall']:.4f}")
    print(f"faithfulness:      {summary['faithfulness']:.4f}")
    print(f"answer_relevancy:  {summary['answer_relevancy']:.4f}")
    print(f"\n상세 결과 저장: {results_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
