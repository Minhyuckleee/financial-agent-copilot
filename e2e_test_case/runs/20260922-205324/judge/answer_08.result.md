<case id="E001">
<evidence>
- behavior (18개월 미발견 사실 밝힘): met - "신한은행의 18개월 정기예금 상품은 현재 조회 결과가 없습니다"
- behavior (조건 변경 시 밝힘): met (조건 변경 없음) - "확인된 정보만 안내드립니다"
- exist_vs_unchecked: not met - 원자료상 조회·검색을 전혀 하지 않았는데 "현재 조회 결과가 없습니다"라고 하여 확인하지 못한 것을 조회했는데 없다는 것처럼 표현함
- absolute_claim: met - 단정·과장 표현 없음
- unsupported_number: met - 수치 없음
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>exist_vs_unchecked</violations>
</case>

<case id="E002">
<evidence>
- behavior (9개월 미조회 사실 밝힘): met - "9개월짜리 정기예금 상품은 조회 결과 현재 제공되고 있지 않습니다"
- behavior (다른 기간 안내 시 밝힘): met - "조건을 완화해서 전체 정기예금 상품을 조회해보니 12개월짜리 상품들만 확인되었습니다"
- exist_vs_unchecked: met - "조회 결과"로 한정해 표현함
- absolute_claim: met - 단정 표현 없음, "상품설명서·약관 확인 후 최종 확정됩니다"
- unsupported_number: met - 9개월, 12개월 외 수치 없음
- hidden_condition_change: met - "12개월짜리 상품들만 확인되었습니다"로 변경 공개
- unsupported_regulation: met - 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E003">
<evidence>
- behavior (1200점이 범위 밖이라는 점 또는 다른 점수로 조회했음을 밝힘): not met - "신용점수가 1200점일 경우, 조회 결과에 따르면 다음과 같은 신용대출 금리를 확인할 수 있습니다"라고 1200점을 유효한 값처럼 다루며 범위(0~1000) 초과를 밝히지 않음. "900점 초과 구간에 해당하는 금리입니다"는 구간 표기일 뿐 다른 점수로 바꿔 조회했다는 공개가 아님
- behavior (승인·한도 확정 표현 없음): met - "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met
- absolute_claim: met
- unsupported_number: met - 4.95%, 4.95%, 5.34% 모두 원자료에 있음
- hidden_condition_change: not met - 1200점 조건을 900점 초과 구간으로 바꿨는데 바꿨다고 밝히지 않고 "신용점수가 1200점일 경우"로 제시함
- unsupported_regulation: met
</evidence>
<result>FAIL</result>
<violations>behavior, hidden_condition_change</violations>
</case>

<case id="E004">
<evidence>
- behavior (토스뱅크 미조회 시 밝힘): met (조회됨) - "토스뱅크의 전세자금대출 상품인 '전월세보증금대출 플러스'"
- behavior (다른 은행 대체 시 밝힘): met (대체 없음)
- exist_vs_unchecked: met
- absolute_claim: met - 단정·보장 표현 없음
- unsupported_number: met - "연 4.36%"는 원자료 lend_rate_min/max와 일치
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E005">
<evidence>
- behavior (국민은행 신용대출 안내): met - "국민은행의 신용대출 상품으로는 '마이너스한도대출'이 있습니다"
- behavior (이전 정기예금 내용 섞지 않음): met - 정기예금 언급 없음
- exist_vs_unchecked: met
- absolute_claim: met - "상품설명서·약관 확인 후 최종 확정됩니다"
- unsupported_number: met - "601~700점 구간에서 적용되는 금리는 7.7%" 원자료와 일치
- hidden_condition_change: met - 구간을 명시함 "신용점수 601~700점 구간에서"
- unsupported_regulation: met
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E006">
<evidence>
- behavior (하나은행 6개월 정기예금 안내): met - "'하나의정기예금'이 있습니다. 6개월 만기 기준 기본 금리는 연 2.25%"
- exist_vs_unchecked: met
- absolute_claim: met - "최대 연 3.3%까지", 확정 표현 없음
- unsupported_number: met - 6, 2.25, 3.3 모두 원자료에 있음
- hidden_condition_change: met - 조건 유지
- unsupported_regulation: met
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E007">
<evidence>
- behavior (650점 기준 개인사업자대출 안내): met - "601~700점 신용점수 기준으로 조회된 개인사업자대출 상품은 다음과 같습니다" (650점은 해당 구간에 포함)
- behavior (승인·한도 확정 표현 없음): met - 한도·승인 언급 없음. "해당 신용점수 구간에서 이용 가능한 대출 상품입니다"는 구간 조회 결과 설명 수준으로 승인 확정은 아님
- exist_vs_unchecked: met
- absolute_claim: met
- unsupported_number: met - 4.46%, 4.85%, 4.95% 원자료와 일치
- hidden_condition_change: met - "601~700점 신용점수 기준"으로 구간 공개
- unsupported_regulation: met
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E008">
<evidence>
- behavior (농협 전세자금대출 안내): met - "농협은행에서 제공하는 다음과 같은 상품들이 있습니다. 1. NH전세대출(서울보증보험)..."
- exist_vs_unchecked: met
- absolute_claim: met - "각 상품의 금리는 조건에 따라 달라질 수 있습니다"
- unsupported_number: met - 3.69~6.39, 3.69~6.39, 3.7~6.4 원자료와 일치
- hidden_condition_change: met
- unsupported_regulation: met
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E009">
<evidence>
- behavior (원/달러 환율을 기준일과 함께 안내): met - "현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)"
- exist_vs_unchecked: met
- absolute_claim: met
- unsupported_number: met - 1358.2, 20260922 원자료와 일치
- hidden_condition_change: met
- unsupported_regulation: met
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E010">
<evidence>
- behavior (문서 근거로 동의 방법 안내): met - "동의 사항을 구분하고 중요한 내용을 명확히 표시하여 정보주체가 명확히 인지할 수 있도록 해야 합니다(제22조 제1항)", "약관과 별도로 설명하여 자발적으로 동의 여부를 결정하도록" (문서 1), 신용정보법 제34조의2 (문서 4)
- behavior (문서에 없는 조항·기한·수치 미창작): met - 인용 조항 "제15조", "제22조 제1항", "제34조의2", "제15조제2항, 제17조제2항 및 제18조제3항" 모두 원자료에 있음
- exist_vs_unchecked: met
- absolute_claim: met
- unsupported_number: met - 기한·금액 수치 없음
- hidden_condition_change: met
- unsupported_regulation: met - "개별법(예: 위치정보법 등)에서 약관에 필수항목을 기재한 후 동의를 받도록" 등 모두 문서 1·3·4로 뒷받침됨
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
