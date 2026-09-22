<case id="C021">
<evidence>
- 주택담보대출 상품을 금리와 함께 안내: met — "경남은행의 '집집마다 도움대출II'로, 최저 금리가 3.7%입니다"
- 승인·한도 확정 표현 없음: met — 승인·한도 언급 없음
- exist_vs_unchecked: met — "현재 조회된 주택담보대출 상품 중에서"
- absolute_claim: met — 해당 표현 없음
- unsupported_number: met — 3.7, 4.18, 4.49 모두 원자료에 있음
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C022">
<evidence>
- 신한은행 주택담보대출 안내: met — "신한주택대출(아파트)", "신한주택대출"
- exist_vs_unchecked: met — "현재 조회된 결과에 따르면"
- absolute_claim: met — "실제 적용 금리는 ... 달라질 수 있으니"
- unsupported_number: not met — "신한주택대출(아파트): 연 4.39% ~ 5.69%" (원자료 최저 4.29, 4.39는 다른 상품 값)
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>unsupported_number</violations>
</case>

<case id="C023">
<evidence>
- 하나은행 주택담보대출 안내: met — "하나원큐아파트론2"라는 주택담보대출 상품이 있습니다
- exist_vs_unchecked: met — 조회된 상품을 그대로 안내
- absolute_claim: met — 해당 표현 없음
- unsupported_number: met — "연 4.5%에서 5.7% 사이" 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C024">
<evidence>
- 주택담보대출 금리 안내: met — "경남은행의 '집집마다 도움대출II'가 연 3.7%~5.51%"
- 승인·한도 확정 표현 없음: met — "실제 적용 금리는 달라질 수 있으니"
- exist_vs_unchecked: met — "현재 조회된 주택담보대출 금리를 보면"
- absolute_claim: met — 해당 표현 없음
- unsupported_number: met — 3.7/5.51, 4.18/5.28, 4.49/6.29 모두 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C025">
<evidence>
- 여러 은행 주담대 금리 비교 안내: met — 경남·우리·농협 3개 은행 금리 범위 나열
- exist_vs_unchecked: met — "현재 조회된 주택담보대출(주담대) 금리를"
- absolute_claim: met — 해당 표현 없음
- unsupported_number: met — "연 3.7%에서 5.51%", "연 4.18%에서 5.28%", "연 4.49%에서 6.29%" 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C026">
<evidence>
- 기업은행 주택담보대출 안내: met — "기업은행(중소기업은행)의 주택담보대출(IBK주택담보대출)"
- exist_vs_unchecked: met — 조회된 상품 안내
- absolute_claim: met — 해당 표현 없음
- unsupported_number: met — "금리는 4.89%입니다" (min=max=4.89)
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C027">
<evidence>
- 개인사업자대출 상품을 금리와 함께 안내: not met — 답변이 "그 다음으로는"으로 시작하고 가장 낮은 제주은행 JJB가맹점우대론(4.46%)이 빠짐
- 승인·한도 확정 표현 없음: met — 해당 표현 없음
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 해당 표현 없음
- unsupported_number: not met — "'우리상생파트너론'(4.95%)" (원자료 4.85)
- hidden_condition_change: not met에 해당하지 않음 — 다만 원자료의 601~700점 구간을 밝히지 않음(질문에 조건이 없어 변경은 아님)
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number</violations>
</case>

<case id="C028">
<evidence>
- 신용점수 800점 기준 개인사업자대출 안내: met — "신용점수 800점인 개인사업자에게 적용되는 대출 금리는 우리은행의 B2B 대출과 우리 지역선도기업 대출"
- 승인·한도 확정 표현 없음: met — 해당 표현 없음
- exist_vs_unchecked: met — "조회 결과에 따르면"
- absolute_claim: met — 해당 표현 없음
- unsupported_number: not met — "각각 연 4.86%로 가장 낮습니다" (원자료 4.85)
- hidden_condition_change: met — 800점은 701~800점 구간에 포함
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>unsupported_number</violations>
</case>

<case id="C029">
<evidence>
- 국민은행 개인사업자대출 안내 또는 미조회 명시: 부분 met — "현재 조회 결과가 없습니다"
- exist_vs_unchecked: not met — 원자료는 "조회도 검색도 하지 않았다"인데 "현재 조회 결과가 없습니다"로 조회해서 없던 것처럼 표현함. "충분히 찾지 못해"는 확인 불가를 분명히 밝히지 않음
- absolute_claim: met — 해당 표현 없음
- unsupported_number: met — 숫자 없음
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>exist_vs_unchecked</violations>
</case>

<case id="C030">
<evidence>
- 개인사업자대출 금리 비교 안내: not met — "다음과 같이 비교할 수 있습니다."로 끝나고 상품·금리가 하나도 없음
- 승인·한도 확정 표현 없음: met — 해당 표현 없음
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 해당 표현 없음
- unsupported_number: met — "601~700점" 원자료에 있음
- hidden_condition_change: met — "601~700점 신용점수 구간에서"로 구간을 밝힘
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>
