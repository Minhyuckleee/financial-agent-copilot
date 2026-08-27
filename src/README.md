# src

Agent 소스코드 루트.

## 구성

- `cli.py` — CLI 진입점. REPL 루프로 turn마다 history를 누적하며 상담직원의 연속 대화를 시뮬레이션
- `graph/` — Agent 핵심 그래프(라우팅 후 route별로 context 또는 tool call → 가드레일 → answer로 분기). 자세한 내용은 `graph/README.md`
- `rag/` — 사내규정질의(policy_qa) RAG 검색 서브시스템. 자세한 내용은 `rag/README.md`
- `tools/` — 외부 API 연동 tool(환율조회/상품추천) + 예외상황 재현 래퍼. 자세한 내용은 `tools/README.md`

## 실행

```bash
pip install -e .
python src/cli.py
```

`.env`에 `OPENAI_API_KEY`/`FINLIFE_API_KEY`/`ECOS_API_KEY`가 있어야 동작합니다(`.env.example` 참고).
