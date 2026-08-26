"""전 구간 공용 LLM 인스턴스 — 단일 모델. 역할별로 다른 모델 안 씀."""
import os

from langchain_openai import ChatOpenAI

_cache: ChatOpenAI | None = None


def get_llm() -> ChatOpenAI:
    global _cache
    if _cache is None:
        _cache = ChatOpenAI(model=os.environ.get("OPENAI_MODEL", "gpt-4.1"), temperature=0)
    return _cache
