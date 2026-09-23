<case id="C001">
<evidence>
- 정기예금을 금리와 함께 안내: met - "광주은행의 '굿스타트예금'이 12개월 기준 기본금리 3.45%, 우대금리 적용 시 3.95%"
- 가입기간 기준 명시: met - "12개월 기준"
- 단정 표현 미사용: met - "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met - "현재 조회된 정기예금 상품 중에서는"
- absolute_claim: met - 원금보장·확정수익 표현 없음
- unsupported_number: met - 3.45/3.95/3.92/3.45 모두 source와 일치
- hidden_condition_change: met - 조건 변경 없음, "12개월 기준" 명시
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C002">
<evidence>
- 6개월 기준 정기예금 안내: met - "6개월짜리 정기예금 상품은 다음과 같습니다."
- exist_vs_unchecked: met - 해당 없음, 조회 결과 제시
- absolute_claim: met - 단정 표현 없음
- unsupported_number: met - "연 2.5%", "연 3.72%", "연 3.2%", "연 3.55%", "연 3.15%", "연 3.25%" 모두 source와 일치
- hidden_condition_change: met - 6개월 조건 유지
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C003">
<evidence>
- 24개월 기준 정기예금 안내: met - "2년(24개월)짜리 예금 상품 중 금리가 높은 곳은 다음과 같습니다."
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 단정 표현 없음, "우대금리 적용 시" 조건 명시
- unsupported_number: met - "최고 연 3.92%", "연 3.82%", "연 3.0%" source와 일치
- hidden_condition_change: met - 24개월 유지
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C004">
<evidence>
- 우리은행 정기예금 안내: met - "우리은행의 정기예금 상품으로는 \"WON플러스예금\"이 있습니다."
- exist_vs_unchecked: met - 조회된 상품 안내
- absolute_claim: met - 단정 표현 없음
- unsupported_number: met - "12개월", "연 3.5%" source와 일치
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C005">
<evidence>
- 하나은행 36개월 정기예금 안내: met - "하나은행의 3년(36개월) 정기예금 금리는 기본 연 2.3%"
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - "우대금리 적용 시 최대 연 2.7%" 조건부 표현
- unsupported_number: met - 2.3%, 2.7% source와 일치
- hidden_condition_change: met - 36개월 유지
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C006">
<evidence>
- 정기예금 상품을 금리와 함께 안내: not met - "이자를 많이 주는 예금 상품은 다음과 같습니다." 이후 상품명·금리가 하나도 제시되지 않음
- 단정 표현 미사용: met - 원금보장·확정수익 표현 없음
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 단정 표현 없음
- unsupported_number: met - 수치 제시 없음
- hidden_condition_change: met - "1년(12개월) 기준으로" 명시
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C007">
<evidence>
- 12개월 기준 정기예금을 우대금리와 함께 안내: met - "광주은행의 '굿스타트예금'으로, 우대금리가 3.95%", "부산은행의 '더(The) 특판 정기예금'이 3.92%의 우대금리"
- 단정 표현 미사용: met - 원금보장·확정수익 표현 없음
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 단정 표현 없음
- unsupported_number: met - 3.95%, 3.92% source와 일치
- hidden_condition_change: met - "1년 만기 예금 중에서" 조건 유지
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C008">
<evidence>
- 신용대출 상품을 금리와 함께 안내: met - "농협은행주식회사의 '가계신용대출(마이너스대출)'로, 601~700점 신용구간에서 금리가 5.72%"
- 승인·한도 확정 표현 미사용: met - 승인·한도 언급 없음, "실제 가입 조건과 금리는 ... 최종 확정됩니다"
- exist_vs_unchecked: met - "현재 조회된 결과 중"
- absolute_claim: met - 단정 표현 없음
- unsupported_number: met - 5.72%, 6.12%, 6.22% source와 일치
- hidden_condition_change: met - "601~700점 신용구간에서" 기준 구간 공개
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C009">
<evidence>
- 신용점수 900점 기준 상품 안내: met - "신용점수가 900점일 경우, 조회 결과 기준으로 가장 낮은 금리의 신용대출 상품은 수협은행의 '개인신용대출'" (source 801~900점 구간)
- 승인·한도 확정 표현 미사용: met - 승인·한도 언급 없음
- exist_vs_unchecked: met - "조회 결과 기준으로"
- absolute_claim: met - 단정 표현 없음
- unsupported_number: met - 5.18%, 5.19%, 5.7% source와 일치
- hidden_condition_change: met - 900점은 801~900점 구간에 포함되어 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C010">
<evidence>
- 점수 조건에 맞는 금리 안내: not met - 사용자는 600점대 초반(601~700점 구간)인데 "모두 501~600점 구간에 해당하는 금리입니다."를 제시
- 승인·한도 확정 표현 미사용: met - 한도·승인 확정 표현 없음 ("받을 수 있는 신용대출 금리는"은 질문 반복 수준)
- exist_vs_unchecked: not applicable/met - 해당 구간 미조회 사실을 밝히지는 않음(behavior에서 반영)
- absolute_claim: met - 단정 표현 없음
- unsupported_number: met - 7.25%, 7.45%, 8.1% source와 일치
- hidden_condition_change: not met - "신용점수가 600점대 초반이라면, 받을 수 있는 신용대출 금리는 다음과 같습니다."라며 다른 구간(501~600점)을 사용자 조건에 맞는 것처럼 제시, 조건이 바뀌었다는 점을 밝히지 않음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior, hidden_condition_change</violations>
</case>
