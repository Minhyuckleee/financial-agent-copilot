# data

Agent 런타임에 필요한 데이터 + 평가용 골든셋/결과.

## 구성

- `rag/` — 빌드된 RAG 인덱스(FAISS/BM25/임베딩/청크). `src/rag/retriever.py`가 런타임에 직접 로드. 빌드 방법은 `src/rag/README.md` 참고
- `guardrail/` — `prohibited_terms.json`: 가드레일 규칙②(필수고지)·③(금지표현) 판정 기준 데이터. `src/graph/guardrail.py`가 런타임에 직접 로드
- `eval/` — 골든셋 원본 + 평가 스크립트가 만든 결과. `scripts/README.md` 참고

`raw/`(원본 법령·약관 문서)와 `guardrail/injection_patterns.json`은 이 repo에 포함하지 않았습니다.

## eval/ 파일 목록

| 파일 | 내용 |
| --- | --- |
| `rag_golden_set_{train,test,valid}.json` | RAG 검색 정답셋(질문+정답청크ID) |
| `rag_deterministic_results_{train,test,valid}.json` | Recall/Precision/MRR 결과 |
| `rag_ragas_results_{train,test}.json` | RAGAS 4종 결과 |
| `citation_grounding_dataset_{train,test}.json` | 가드레일 규칙⑤ 판정기 검증용 positive 샘플 |
| `citation_grounding_negatives_{train,test}.json` | 같은 목적의 negative 샘플(의도적으로 틀리게 저술) |
| `citation_grounding_negatives_extra.json` | 위조 표본 확장용 40건(5실패유형×8, LLM 초안+사람 검증) |
| `citation_grounding_pool100.json` | cosine-vs-LLM 비교용 정상 50 + 위조 50 pool |
| `citation_grounding_cosine_range_results.json` | cosine 유사도 range 비교 결과 |
| `citation_grounding_llm_detection_results.json` | LLM entailment 판정 위조탐지 결과 |
| `tool_selection_strategy_dataset.json` | tool 선택 프롬프트 전략 비교용 100건(5상품×모호발화 4유형×5변형) |
| `tool_selection_strategy_testset.json` | 같은 발견의 재현 확인용 추가 50건(100건과 안 겹침) |
| `tool_selection_strategy_results.json` | 100건 기준 naive vs 목적재정의 프롬프트 비교 결과 |
| `tool_selection_strategy_testset_results.json` | 추가 50건 기준 비교 결과 |
| `threshold_calibration_results.json`, `threshold_negative_probes_{train,test,valid}.json` | RAG confidence threshold 캘리브레이션 과정에서 만든 실험 데이터 |
| [`agent_eval_v1.json`](eval/agent_eval_v1.json) / [`_results.json`](eval/agent_eval_v1_results.json) | 1차 평가셋(기능별 최소 1건씩)의 케이스+결과 |
| [`agent_quality_train.json`](eval/agent_quality_train.json) / [`_results.json`](eval/agent_quality_train_results.json) | 2차 복합 시나리오 평가셋(이력·예외분기·가드레일이 동시에 겹치는 케이스) train의 케이스+결과 |
| [`agent_quality_test.json`](eval/agent_quality_test.json) / [`_results.json`](eval/agent_quality_test_results.json) | 같은 평가셋의 개발에 안 쓴 별도 검증용 test 케이스+결과 |
