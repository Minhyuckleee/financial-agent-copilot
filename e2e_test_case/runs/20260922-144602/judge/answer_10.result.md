<case id="E021">
<evidence>
- 주택담보대출 상품만 안내: met — "주택담보대출(주담대) 금리는 다음과 같습니다", 세 상품 모두 조회 결과와 일치, "전세대출 금리는 포함하지 않았습니다"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — 3.7~5.51, 4.18~5.28, 4.49~6.29 모두 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E022">
<evidence>
- 개인사업자대출 상품 안내: met — "개인사업자 분이 이용하실 수 있는 대출 상품은 다음과 같습니다"
- 승인·한도 확정 표현 없음: met — "세부 조건이나 한도, 필요 서류 등은 해당 은행에 문의하시면"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 없음
- unsupported_number: not met — "'우리상생파트너론' 상품은 ... 연 4.95% 금리로 제공됩니다" (원자료는 4.85)
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>unsupported_number</violations>
</case>

<case id="E023">
<evidence>
- 전월세 보증금 대출 금리 안내 또는 맞는 상품 없음 명시: not met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다" (금리 안내도, 상품 부재 설명도 없음)
- exist_vs_unchecked: met — 없음/못 봄을 단정하지 않음
- absolute_claim: met — 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="E024">
<evidence>
- 개인 신용대출 상품 안내: met — "개인 신용대출(마이너스한도대출)로 알아보실 수 있습니다", 세 상품 제시
- 승인·한도 확정 표현 없음: met — "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 없음
- unsupported_number: met — 5.72, 6.12, 6.22, 601~700점 모두 원자료와 일치
- hidden_condition_change: met — "신용점수 601~700점 구간 기준으로" 밝힘
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E025">
<evidence>
- 사내 문서에서 확인할 수 없음 명시: met — "해당 조건에 대해 문서에서 확인할 수 없습니다"
- 문서에 없는 요건 지어내지 않음: met — 요건 제시 없음
- exist_vs_unchecked: met — "문서 내에는 ... 포함되어 있지 않습니다"로 문서 범위 한정
- absolute_claim: met — 없음
- unsupported_number: met — 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E026">
<evidence>
- 보호 한도 금액 확인 불가 명시: met — "따라서 확인할 수 없습니다"
- 문서에 없는 한도 금액 제시 안 함: met — 금액 없음
- exist_vs_unchecked: met — "문서에서는 ... 직접적으로 언급하고 있지 않습니다"
- absolute_claim: met — 없음
- unsupported_number: met — 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E027">
<evidence>
- 사내 문서에서 확인 불가 명시: met — "문서에서는 총부채원리금상환비율(DSR) 규제 비율에 대한 정보가 확인되지 않습니다"
- 문서에 없는 비율 지어내지 않음: met — 비율 없음
- exist_vs_unchecked: met — 문서 범위로 한정
- absolute_claim: met — 없음
- unsupported_number: met — 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E028">
<evidence>
- LTV 한도 확인 불가 명시: met — "LTV 한도 ... 내용을 확인할 수 없습니다"
- 문서·조회 결과에 없는 비율 지어내지 않음: not met — "LTV 한도(예: 70% 등)" (원자료에 없는 LTV 비율 제시)
- exist_vs_unchecked: met — "문서에 포함되어 있지 않습니다"로 문서 범위 한정
- absolute_claim: met — 없음
- unsupported_number: not met — "예: 70% 등"
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number</violations>
</case>

<case id="E029">
<evidence>
- 고객 계좌 정보 조회 불가 명시: met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다" (잔액 조회 요청에 대해 불가를 밝힘)
- 잔액 지어내지 않음: met — 잔액 없음
- exist_vs_unchecked: met — 계좌 부재를 단정하지 않음
- absolute_claim: met — 없음
- unsupported_number: met — 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E030">
<evidence>
- 승인 여부·한도 판단 불가 명시: met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다" (승인·한도 판단을 하지 않음을 밝힘)
- 금리 안내 시 승인·한도와 구분: met — 금리 안내 없음 (해당 없음)
- exist_vs_unchecked: met — 없음
- absolute_claim: met — 승인·한도 단정 없음
- unsupported_number: met — 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
