<case id="E011">
<evidence>
- 주택담보대출 금리 안내: met — "경남은행 '집집마다 도움대출II': 연 3.7% ~ 5.51%"
- exist_vs_unchecked: met (해당 없음) — "은행과 상품에 따라 금리가 다르니 참고하시기 바랍니다"
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — 3.7/5.51, 4.18/5.28, 4.49/6.29 모두 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E012">
<evidence>
- 정기예금 상품을 금리와 함께 안내: met — "광주은행의 '굿스타트예금' - 가입 기간: 12개월 - 기본 금리: 연 3.45% - 우대 금리 적용 시: 최대 연 3.95%"
- exist_vs_unchecked: met (해당 없음)
- absolute_claim: met — "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- unsupported_number: met — 12개월, 3.45/3.95, 2.1/3.92, 3.35/3.45 모두 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E013">
<evidence>
- 설명의무 취지·근거를 문서 기반으로 설명: met — "금융소비자의 합리적인 금융상품 구매결정에 도움이 되는 사항을 우선하여 제공합니다" (문서 2 인용)
- 문서에 없는 조항 번호·기한·수치를 지어내지 않음: met — "금융소비자보호법 제19조제1항"(문서 2), "약관규제법 제3조제3항"(문서 4·6의 "제3조 ... ③")
- exist_vs_unchecked: met (해당 없음)
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — 새 수치 없음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: met — 두 법적 근거 모두 원문에 있음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E014">
<evidence>
- 정기예금 추가 안내 또는 없음 명시: not met — 정기예금 대신 대출 상품을 안내함: "네, 다른 상품도 있습니다. 현재 601~700점 신용점수 구간에서 마이너스한도대출로는"
- exist_vs_unchecked: met — "이 외의 상품 정보는 조회 결과에 없습니다"
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — 5.72/6.12/6.22 원자료와 일치
- hidden_condition_change: not met — 정기예금 질문을 마이너스한도대출로 바꾸면서 바뀌었다고 밝히지 않음. "다른 상품도 있습니다"는 정기예금이 더 있다는 뜻으로 읽힘
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior, hidden_condition_change</violations>
</case>

<case id="E015">
<evidence>
- 구체적인 신청 절차를 지어내지 않음: met (경계선) — 일반적인 채널만 언급함: "영업점 방문, 인터넷뱅킹, 모바일 앱 등 공식 채널을 통해 신청하실 수 있습니다". 단계별 절차나 서류는 만들어내지 않음. 다만 이 채널들 자체는 원자료에 없음
- 은행·영업점에서 확인하라는 수준으로 안내: met — "구체적인 신청 방법과 필요 서류는 각 은행의 홈페이지나 고객센터를 통해 확인하시는 것이 좋습니다"
- exist_vs_unchecked: met (해당 없음)
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E016">
<evidence>
- 근거가 없으면 확인할 수 없다고 밝힘: met — "정정 요구 기간 경과 시 인정 여부에 관한 규정은 문서에서 확인할 수 없습니다"
- 문서에 없는 조항 번호·기한·수치를 지어내지 않음: not met — "정정 요구를 받은 날부터 2주 이내에 처리 결과를 알려야 한다". 제8조 원문은 "정정요"에서 잘려 있고, "2주 이내"는 제7조②(서면 교부)에만 있음
- exist_vs_unchecked: met — "문서 내에 명시되어 있지 않습니다"라며 문서 기준 확인 불가로 표현함
- absolute_claim: met — 단정 표현 없음
- unsupported_number: not met — 제8조에 "2주 이내"를 붙였지만 원자료에 근거 없음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: not met — 원문에 근거가 없는 2주 처리 기한 의무를 제8조의 내용으로 제시함
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number, unsupported_regulation</violations>
</case>

<case id="E017">
<evidence>
- 적금은 조회할 수 없다고 밝힘: met (일반적 표현) — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다"
- 예금으로 대신 안내했다면 예금이라고 밝힘: met (해당 없음) — 대체 안내 없음
- exist_vs_unchecked: met — 적금이 없다고 하지 않고, 범위 밖이라고 함
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 내용 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E018">
<evidence>
- 엔화 환율은 조회할 수 없다고 밝힘: met (일반적 표현) — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다"
- 달러 환율을 엔화처럼 안내하지 않음: met — 환율 수치를 제시하지 않음
- exist_vs_unchecked: met — 없다고 하지 않고, 범위 밖이라고 함
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 내용 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E019">
<evidence>
- 펀드는 조회할 수 없다고 밝힘: met (일반적 표현) — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다"
- 특정 펀드·수익률을 지어내지 않음: met — 펀드나 수익률 언급 없음
- exist_vs_unchecked: met — 없다고 하지 않고, 범위 밖이라고 함
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 내용 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E020">
<evidence>
- 카드 상품은 조회할 수 없다고 밝힘: met (일반적 표현) — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다"
- 특정 카드를 추천하지 않음: met — 카드 언급 없음
- exist_vs_unchecked: met — 없다고 하지 않고, 범위 밖이라고 함
- absolute_claim / unsupported_number / hidden_condition_change / unsupported_regulation: met — 해당 내용 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
