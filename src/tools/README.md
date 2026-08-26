# tools

Agent가 Function Calling으로 호출하는 외부 API 연동 tool.

## 구성

- `ecos.py` — 한국은행 ECOS API. 원/달러 환율조회 tool 1개(`inquire_exchange_rate`)
- `finlife.py` — 금융감독원 「금융상품한눈에」 API. 상품추천 tool 5개(정기예금/개인신용대출/전세자금대출/주택담보대출/개인사업자대출). 신용대출류는 공시된 신용점수구간별 금리표 조회일 뿐 — 실제 대출승인·한도심사(고영향AI 규제 대상, 설명가능성 의무)는 스코프 밖
- `fault_injection.py` — 위 tool들에 씌우는 예외상황 강제 재현 래퍼. 평가/테스트 전용이고 실제 서비스 동작과는 무관

## 실API 사용

전부 mock 없이 실제 외부 API를 호출합니다(연동 확인은 `scripts/smoke/`). 정보조회만 하고 실제 금융거래(송금·개설·승인)는 하지 않습니다.
