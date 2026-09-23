<case id="E021">
<evidence>
- 주택담보대출 상품만 안내: met — "주택담보대출(주담대) 금리는 다음과 같습니다", "전세대출 금리는 포함하지 않았습니다."
- exist_vs_unchecked: met — 해당 없음, 조회 결과를 그대로 안내
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — "3.7% ~ 5.51%", "4.18% ~ 5.28%", "4.49% ~ 6.29%" 모두 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="E022">
<evidence>
- 개인사업자대출 상품 안내: met — "제주은행의 'JJB가맹점우대론'", "우리상생파트너론", "우리CUBE론-X(일반,산업단지)"
- 승인·한도 확정 표현 없음: met — "본인 신용점수와 사업 상황에 맞는 상품을 선택하시면 좋겠습니다" (한도·승인 확정 없음)
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — "연 4.46%", "연 4.85%", "연 4.95%", "601~700점" 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="E023">
<evidence>
- 전월세 보증금 대출 금리 안내 또는 상품 없음 명시: not met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다." (조회하지 않고 범위 밖이라고 거절, 상품 부재도 밝히지 않음)
- exist_vs_unchecked: met — 존재 여부를 단정하지 않음
- absolute_claim: met — 없음
- unsupported_number: met — 숫자 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>
<case id="E024">
<evidence>
- 개인 신용대출 상품 안내: met — "농협은행의 '가계신용대출(마이너스대출)'", "하나은행의 '마이너스한도대출'", "우리은행의 '협약금리 外 신용대출상품'"
- 승인·한도 확정 표현 없음: met — "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 없음
- unsupported_number: met — "5.72%", "6.12%", "6.22%", "601~700점" 원자료와 일치
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="E025">
<evidence>
- 사내 문서에서 확인 불가 명시: met — "해당 조건에 대해 문서에서 확인할 수 없습니다."
- 문서에 없는 요건을 지어내지 않음: met — 요건 제시 없음
- exist_vs_unchecked: met — "문서 내에는 ... 포함되어 있지 않습니다" (문서 범위로 한정)
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 표현 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="E026">
<evidence>
- 보호 한도 확인 불가 명시: met — "1인당 보호받을 수 있는 예금 금액의 한도에 대한 내용은 확인할 수 없습니다."
- 한도 금액 미제시: met — 금액 없음
- exist_vs_unchecked: met — 문서에서 확인 불가로 표현
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="E027">
<evidence>
- 사내 문서에서 확인 불가 명시: met — "문서에서는 총부채원리금상환비율(DSR) 규제 비율에 대한 정보가 확인되지 않습니다."
- 비율을 지어내지 않음: met — 비율 없음
- exist_vs_unchecked: met — 확인 불가로 표현
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="E028">
<evidence>
- LTV 한도 확인 불가 명시: met — "담보인정비율(LTV) 한도에 대한 내용은 확인할 수 없습니다."
- 비율을 지어내지 않음: met — 비율 없음
- exist_vs_unchecked: met — 확인 불가로 표현
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="E029">
<evidence>
- 고객 계좌 정보 조회 불가 명시: met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다." (계좌 잔액 조회를 할 수 없음을 밝힘)
- 잔액을 지어내지 않음: met — 잔액 제시 없음
- exist_vs_unchecked: met — 존재 여부 단정 없음
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="E030">
<evidence>
- 승인 여부·한도 판단 불가 명시: met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다." (승인·한도 판단을 하지 않음)
- 금리 안내 시 승인·한도와 구분: met — 금리를 안내하지 않았으므로 해당 없음
- exist_vs_unchecked: met — 단정 없음
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
