"""context 구성 단계 — 사내규정질의 RAG 검색

파이프라인
1. BM25 top-N ∪ FAISS top-N : union, 강제 truncate 없음, 최종 3~6개 가변
2. confidence : 청크별 FAISS 코사인 유사도(BM25는 후보검색에만 관여, confidence
   게이트엔 안 들어감 — BM25 raw score는 질문마다 스케일이 달라져 고정 임계값으로 못 거름)
3. 필터링 : 호출부(context.py)가 THRESHOLD_LOW로 판단, 이 함수는 안 함

THRESHOLD_LOW=0.40 : 정밀분리선 아니라 느슨한 바닥선. "그럴듯하지만 문서에 없는 질문"은
이 threshold로 못 거름 — 진짜 방어선은 answer단계 정직성 프롬프트 + 규칙⑤ grounding체크
"""
import json
import os
import pickle
from itertools import zip_longest
from pathlib import Path
from typing import Any

os.environ.setdefault("HF_TOKEN", "dummy")  # 로컬 손상된 HF 토큰캐시 우회

import faiss
import numpy as np
from kiwipiepy import Kiwi

from rag.embeddings.kure_embedder import KUREEmbedder

_ROOT = Path(__file__).resolve().parent.parent.parent
_RAG_DIR = _ROOT / "data" / "rag"
_CANDIDATE_N = 3

THRESHOLD_LOW = 0.40  

_cache: dict[str, Any] = {}


def _load() -> dict[str, Any]:
    if _cache:
        return _cache

    chunks = json.loads((_RAG_DIR / "chunks_2300.json").read_text(encoding="utf-8"))
    with open(_RAG_DIR / "faiss_index_2300.index", "rb") as f:
        faiss_index = faiss.deserialize_index(np.frombuffer(f.read(), dtype=np.uint8))
    with open(_RAG_DIR / "bm25_index_2300.pkl", "rb") as f:
        bm25_index = pickle.load(f)
    embeddings = np.load(_RAG_DIR / "embeddings_2300.npy")

    _cache.update(
        chunks=chunks,
        faiss_index=faiss_index,
        bm25_index=bm25_index,
        embeddings=embeddings,
        embedder=KUREEmbedder(device="cpu", show_progress=False),
        kiwi=Kiwi(),
    )
    return _cache


def _ranked_candidates(query: str, top_n: int) -> tuple[list[int], list[int], np.ndarray]:
    """BM25/FAISS 각각의 순위(내림차순)를 그대로 보존한 후보 인덱스 목록과,
    confidence 계산에 재사용할 정규화된 질문 임베딩을 반환."""
    state = _load()
    bm25_index, faiss_index = state["bm25_index"], state["faiss_index"]

    tokens = [t.form for t in state["kiwi"].tokenize(query)]
    bm25_scores = bm25_index.get_scores(tokens)
    bm25_ranked = np.argsort(bm25_scores)[::-1][:top_n].tolist()

    query_emb = state["embedder"].embed(query).reshape(1, -1).astype("float32")
    faiss.normalize_L2(query_emb)
    _, faiss_idx = faiss_index.search(query_emb, top_n)
    faiss_ranked = faiss_idx[0].tolist()

    return bm25_ranked, faiss_ranked, query_emb


def _confidence(idx: int, query_emb: np.ndarray, embeddings: np.ndarray) -> float:
    """FAISS 코사인 유사도(선택 경로 무관 — BM25로 뽑힌 청크든 FAISS로 뽑힌 청크든, 저장된
    청크 벡터를 질문 임베딩과 직접 내적) 단독. BM25는 후보 검색에만 관여하고 confidence
    게이트에는 안 들어간다 — BM25 raw score는 질문 단어수·희귀도에 따라 스케일이 매번
    달라져 고정 임계값으로 신뢰성 있게 못 거르는 게 실측으로 확인됨."""
    return float(np.dot(embeddings[idx], query_emb[0]))


def retrieve(query: str, top_n: int = _CANDIDATE_N) -> list[dict[str, Any]]:
    """BM25 top-N ∪ FAISS top-N(중복제거, 강제 truncate 없음) + 청크별 confidence score.
    "BM25 1위, FAISS 1위, BM25 2위, FAISS 2위, ..." 순서로 라운드로빈 교차한 뒤 중복만
    제거한다 — 포함 여부(어떤 청크가 살아남는지)는 project1 방식과 동일(전부 보존),
    순서만 두 순위를 번갈아 반영해 MRR 같은 단일순위 지표가 의미를 유지하게 한다."""
    state = _load()
    chunks = state["chunks"]
    bm25_ranked, faiss_ranked, query_emb = _ranked_candidates(query, top_n)

    interleaved = [x for pair in zip_longest(bm25_ranked, faiss_ranked) for x in pair if x is not None]
    union = list(dict.fromkeys(interleaved))

    return [
        {
            "id": chunks[i]["id"],
            "source": chunks[i]["source"],
            "content": chunks[i]["content"],
            "confidence": _confidence(i, query_emb, state["embeddings"]),
        }
        for i in union
    ]
