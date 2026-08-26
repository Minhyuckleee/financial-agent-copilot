# rag

사내규정질의(policy_qa) RAG 검색 서브시스템입니다. `graph/context.py`가 `retrieve()`를 호출해서 씁니다

## 구성

- `retriever.py` — 런타임 검색 실행부. `graph/context.py`가 호출하는 진입점(BM25∪FAISS union, confidence 계산)
- `embeddings/` — KURE-v1(한국어 특화) 임베딩 모델. `kure_embedder.py`가 실제 구현, `langchain_adapter.py`는 RAGAS 평가(`scripts/rag_eval_ragas.py`)가 요구하는 LangChain `Embeddings` 인터페이스로 감싸는 어댑터
- `preprocessing/` — 문서 청킹(`hybrid_chunker_2300.py`, section-aware 2300자) + 텍스트 정제(`text_cleaner.py`). 인덱스 빌드(오프라인) 전용이라 Agent 실행 시엔 안 쓰임 — 빌드 산출물(`data/rag/*`)은 이미 repo에 포함돼있음

## 검색 파이프라인 (retriever.py)

1. BM25 top-N ∪ FAISS top-N — union, 중복제거, 강제 truncate 없음, 최종 3~6개
2. 청크별 confidence = FAISS 코사인 유사도 단독(BM25는 후보검색에만 관여)
3. `THRESHOLD_LOW`(0.40) 미만은 호출부(`context.py`)가 필터링

## confidence 설계 — threshold 캘리브레이션 여정

confidence를 FAISS 코사인 단독으로 정하기까지 세 단계를 거쳤습니다:

1. **후보군 내 최고점 비율** — 그 질문 BM25 1위가 항상 confidence=1.0이 되는 구조적 결함으로 폐기
2. **BM25 절대스케일 saturating**(`score/(score+25)`) — golden set 정답청크 BM25 raw 15.5, 오프토픽 질문 raw 21.2인 경우가 있어(15.5 < 21.2) 원점수 자체가 두 그룹을 완벽히 분리 못 함이 드러남. 표본을 늘려도 해결 안 되는 근본적 겹침이었습니다.
   - 대안으로 질문별 이론적 최댓값 정규화도 시도 — 짧은 질문은 상대점수가 인위적으로 높아지고 긴 법률질문은 낮아지는 반대방향 편향이 생겨 폐기
3. **FAISS 단독 재실측** — golden set 정답청크 FAISS 최솟값(0.5094) vs 오프토픽 probe FAISS 최댓값(0.4744) 완전분리 확인, 채택

`THRESHOLD_LOW=0.40`은 정밀 분리선이 아니라 느슨한 바닥선입니다. 소표본으로 정밀 캘리브레이션(0.50 등)을 계속 시도했지만 표본을 늘릴수록 golden/오프토픽 margin이 계속 줄어들어(0.035→0.0042) 일반화 안 되는 숫자놀음이라 판단해 중단했습니다(오버피팅 자각).

`THRESHOLD_LOW`가 실제로 막는 건 "코퍼스와 무관한 질문"이 아니라 라우터가 잘못 분류한 극단적 저신호 케이스뿐입니다 — "법령스럽게 들리지만 문서에 없는 질문"(예: 보험업법)은 BM25/FAISS 둘 다 그럴듯한 점수를 줘서 threshold로 못 거릅니다. 진짜 방어선은 답변생성 단계의 정직성 프롬프트 + 가드레일 규칙⑤(citation grounding)입니다 — 둘 다 실API로 검증됐습니다.

top_n=3: BM25 top-final_n 자체가 이미 final_n개의 서로 다른 청크를 보장해서, FAISS 쪽 4위 이후는 애초에 최종 결과에 영향을 줄 수 없습니다.

## 인덱스 빌드 방법

청킹(`HybridChunker2300`, 2300자 section-aware)·임베딩(KURE-v1)·인덱스(BM25+FAISS) 로직은 [financial-security-rag-qa](https://github.com/Minhyuckleee/financial-security-rag-qa)(금융보안원 AI 경진대회, baseline 대비 +32.7% 상대향상 달성)에서 검증된 방법론을 그대로 재사용했습니다 — 새 문서셋(이 프로젝트의 사내규정 13개)으로 재실행만 했습니다.

1. 청킹 — 2300자 단위, 섹션 경계 오버랩 300자(문장이 섹션 중간에서 안 잘리도록)
2. 임베딩 — KURE-v1(한국어 특화 sentence-transformers)로 청크별 벡터 생성
3. 인덱스 구축 — BM25(Kiwi 형태소분석)와 FAISS(코사인, L2정규화) 둘 다 생성 — `retriever.py`가 검색 시점에 둘을 union으로 사용

`data/rag/`에 이미 빌드된 결과가 포함돼있어 별도 빌드 없이 바로 실행 가능합니다. 빌드 로직(`preprocessing/`)은 오프라인 도구라 이 repo의 실행경로엔 포함되지 않습니다.
