<case id="C021">
<evidence>
- behavior 1 (주담대 상품을 금리와 함께 안내): met - "경남은행의 '집집마다 도움대출II'가 최저 금리 3.7%로 가장 낮은 금리를 제공합니다"
- behavior 2 (승인/한도 확정 표현 없음): met - 승인·한도 언급 없음, "현재 조회된 주택담보대출 상품 중에서는"
- exist_vs_unchecked: met - "현재 조회된 주택담보대출 상품 중에서는"
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - "3.7%", "4.18%", "4.49%" 모두 원자료에 있음
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C022">
<evidence>
- behavior 1 (신한은행 주담대 안내): met - "신한주택대출(아파트): 연 4.29% ~ 5.69%", "신한주택대출: 연 4.39% ~ 5.79%"
- exist_vs_unchecked: met - "현재 조회된 결과에 따르면"
- absolute_claim: met - "실제 적용 금리는 대출 조건이나 신용도 등에 따라 달라질 수 있으니"
- unsupported_number: met - 모든 금리가 원자료와 일치
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C023">
<evidence>
- behavior 1 (하나은행 주담대 안내): met - "하나은행에는 '하나원큐아파트론2'라는 주택담보대출 상품이 있습니다"
- exist_vs_unchecked: met - 조회된 상품이 있다고 안내하며 원자료에 근거함
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - "연 4.5%에서 5.7% 사이" 원자료와 일치
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C024">
<evidence>
- behavior 1 (주담대 금리 안내): met - "경남은행의 '집집마다 도움대출II'가 최저 3.7%에서 최고 5.51%"
- behavior 2 (승인/한도 확정 표현 없음): met - "실제 적용 금리는 신용도, 대출 조건 등에 따라 달라질 수 있으니"
- exist_vs_unchecked: met - "현재 조회된 주택담보대출 금리를 보면"
- absolute_claim: met - "상대적으로 괜찮아 보입니다"
- unsupported_number: met - 3.7/5.51/4.18/5.28/4.49/6.29 모두 원자료에 있음
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C025">
<evidence>
- behavior 1 (여러 은행 주담대 금리 비교): met - 경남은행 "연 3.7%에서 5.51%", 우리은행 "연 4.18%에서 5.28%", 농협은행 "연 4.49%에서 6.29%"
- exist_vs_unchecked: met - "현재 조회된 주택담보대출(주담대) 금리를"
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - 모든 수치 원자료와 일치
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C026">
<evidence>
- behavior 1 (기업은행 주담대 안내): met - "기업은행(중소기업은행)의 IBK주택담보대출 금리는 4.89%입니다"
- exist_vs_unchecked: met - 조회된 상품을 안내
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - "4.89%" 원자료(min=max=4.89)와 일치
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C027">
<evidence>
- behavior 1 (개인사업자대출을 금리와 함께 안내): not met - 답변이 "그 다음으로는 우리은행의 '우리상생파트너론'(4.85%)"로 시작해 가장 낮은 제주은행 'JJB가맹점우대론'(4.46%)이 빠진 잘린 답변이며, 질문(금리 낮은 곳)에 대한 핵심이 누락됨
- behavior 2 (승인/한도 확정 표현 없음): met - 승인·한도 언급 없음
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - "4.85%", "4.95%" 원자료에 있음
- hidden_condition_change: met - 신용점수 구간(601~700점) 미표시지만 사용자가 조건을 준 적 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C028">
<evidence>
- behavior 1 (800점 기준 개인사업자대출 안내): met - "신용점수 800점인 개인사업자에게 적용되는 대출 금리는 우리은행의 B2B 대출과 우리 지역선도기업 대출이 각각 연 4.85%" (원자료 701~800점 구간과 부합)
- behavior 2 (승인/한도 확정 표현 없음): met - 승인·한도 언급 없음
- exist_vs_unchecked: met - "조회 결과에 따르면"
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - "4.85%", "4.86%" 원자료와 일치
- hidden_condition_change: met - 800점은 701~800점 구간에 포함되어 조건 변경 아님
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C029">
<evidence>
- behavior 1 (국민은행 개인사업자대출 안내 또는 미조회 명시): not met - 실제로는 조회도 검색도 하지 않았는데 "현재 조회 결과가 없습니다"라고 하여 조회 후 없는 것처럼 안내함
- exist_vs_unchecked: not met - "국민은행의 개인사업자대출 상품은 현재 조회 결과가 없습니다" (확인하지 못한 것을 조회 결과 없음으로 표현)
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - 수치 없음
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior, exist_vs_unchecked</violations>
</case>

<case id="C030">
<evidence>
- behavior 1 (개인사업자대출 금리 비교): met - "제주은행의 'JJB가맹점우대론' : 연 4.46%", "우리상생파트너론 : 연 4.85%", "우리CUBE론-X(일반,산업단지) : 연 4.95%"
- behavior 2 (승인/한도 확정 표현 없음): met - 승인·한도 언급 없음
- exist_vs_unchecked: met - "현재 601~700점 신용점수 구간에서"
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - 모든 수치 원자료와 일치
- hidden_condition_change: met - 적용 구간을 "601~700점 신용점수 구간에서"로 명시
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
