"""KUREEmbedder를 LangChain `Embeddings` 인터페이스로 감싸는 얇은 어댑터.

RAGAS TestsetGenerator 등 LangChain 인터페이스를 요구하는 외부 도구에서 실제
`retrieve()`가 쓰는 것과 같은 임베딩(KURE-v1)을 그대로 재사용하기 위함 —
평가용으로 별도 임베딩 모델(OpenAI 등)을 새로 도입하지 않는다.
"""
from langchain_core.embeddings import Embeddings

from .kure_embedder import KUREEmbedder


class KureLangchainEmbeddings(Embeddings):
    def __init__(self, embedder: KUREEmbedder | None = None):
        self._embedder = embedder or KUREEmbedder(device="cpu", show_progress=False)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        embeddings = self._embedder.embed_batch(texts)
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        return self._embedder.embed(text).tolist()
