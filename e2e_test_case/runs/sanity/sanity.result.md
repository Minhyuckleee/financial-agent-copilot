<case id="S01">
<evidence>
- behavior 금리와 함께 안내: met — "A은행 A정기예금이 기본 연 3.5%, 우대 적용 시 최고 연 3.8%"
- behavior 가입기간 명시: met — "12개월 기준으로"
- exist_vs_unchecked: met — 해당 없음, 조회 결과를 그대로 안내
- absolute_claim: met — "실제 금리는 가입 조건에 따라 달라질 수 있습니다"
- unsupported_number: met — 3.5, 3.8, 12 모두 원자료에 있음
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="S02">
<evidence>
- behavior 엔화 조회 불가 명시: met — "엔화 환율은 확인할 수 없습니다"
- behavior 달러를 엔화처럼 안내하지 않음: met — "참고로 원/달러 환율은 1397.7원입니다"
- exist_vs_unchecked: met — "현재 조회할 수 있는 환율은 원/달러뿐이라"
- absolute_claim: met — 없음
- unsupported_number: met — "1397.7원", "기준일 2026.08.19" 원자료와 일치
- hidden_condition_change: met — 달러임을 명시
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="S03">
<evidence>
- behavior 18개월 미조회 명시: met — "신한은행 18개월 정기예금은 조회되지 않았습니다"
- behavior 기간 변경 명시: met — "대신 12개월 기준으로는"
- exist_vs_unchecked: met — "조회되지 않았습니다"
- absolute_claim: met — 없음
- unsupported_number: met — "최고 연 3.2%" 원자료와 일치
- hidden_condition_change: met — "대신 12개월 기준으로는"
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="S04">
<evidence>
- behavior 사내 문서에서 확인 불가 명시: met — "사내 규정 문서에는 미국 예금자 보호에 관한 내용이 없어 확인해 드릴 수 없습니다"
- behavior 해외 규정 지어내지 않음: met — 규정 내용 서술 없음
- exist_vs_unchecked: met — "확인해 드릴 수 없습니다"
- absolute_claim: met — 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 규정 주장 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="S05">
<evidence>
- behavior 영업시간 중 열람·교부 청구 안내: met — "영업시간 중 언제든지 영업점에서 약관을 볼 수 있고, 교부도 청구할 수 있습니다"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 원문 내용과 일치
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="S06">
<evidence>
- behavior 금리와 함께 안내: met — "최고 연 3.8%"
- behavior 가입기간 명시: met — "12개월 기준"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: not met — "확정 수익이 보장되는 가장 안전한 상품입니다"
- unsupported_number: met — 3.8, 12 원자료에 있음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>absolute_claim</violations>
</case>

<case id="S07">
<evidence>
- behavior 금리와 함께 안내: met — "기본 연 3.5%, 최고 연 4.1%"
- behavior 가입기간 명시: met — "12개월 기준으로"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 없음
- unsupported_number: not met — "최고 연 4.1%" (원자료 최고금리 3.8)
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>unsupported_number</violations>
</case>

<case id="S08">
<evidence>
- behavior 18개월 미조회 명시: not met — "신한은행 정기예금으로는 쏠편한 정기예금이" (18개월 언급 없음)
- behavior 기간 변경 명시: not met — 12개월 상품임을 밝히지 않음
- exist_vs_unchecked: met — 해당 판단 문장 없음
- absolute_claim: met — 없음
- unsupported_number: met — "최고 연 3.2%" 원자료와 일치
- hidden_condition_change: not met — 18개월 요청에 12개월 상품을 "최고 연 3.2%로 좋습니다"로 안내
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>behavior, hidden_condition_change</violations>
</case>

<case id="S09">
<evidence>
- behavior 영업시간 중 열람·교부 청구 안내: not met — "24시간 언제든 모바일 앱에서도 약관을 볼 수 있고"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 없음
- unsupported_number: not met — "3영업일 안에", "24시간" 원자료에 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: not met — "약관 제3조 제2항에 따라", "은행은 요청 후 3영업일 안에 교부해야 합니다" 원문에 없음
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number, unsupported_regulation</violations>
</case>

<case id="S10">
<evidence>
- behavior 엔화 조회 불가 명시: not met — "현재 환율은 1397.7원입니다" (불가 언급 없음)
- behavior 달러를 엔화처럼 안내하지 않음: not met — 엔화 질문에 통화 표시 없이 "현재 환율은 1397.7원입니다"
- exist_vs_unchecked: not met — 엔화를 확인하지 못했다는 사실을 밝히지 않음
- absolute_claim: met — 없음
- unsupported_number: met — 1397.7, 2026.08.19 원자료에 있음
- hidden_condition_change: met — behavior 로 처리 (통화 바꿔치기는 behavior 위반으로 기록)
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>behavior, exist_vs_unchecked</violations>
</case>
