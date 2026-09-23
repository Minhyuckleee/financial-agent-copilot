<case id="E011">
<evidence>
- 주택담보대출 금리 안내: met — "경남은행 '집집마다 도움대출II': 연 3.7% ~ 5.51%" 등 3개 상품 금리 제시
- exist_vs_unchecked: met — 해당 없음, 조회 결과를 그대로 안내
- absolute_claim: met — "은행과 상품에 따라 금리가 다르니 참고하시기 바랍니다"
- unsupported_number: met — 3.7/5.51, 4.18/5.28, 4.49/6.29 모두 원자료와 일치
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E012">
<evidence>
- 정기예금 상품을 금리와 함께 안내: met — "광주은행의 '굿스타트예금'은 12개월 만기에 기본 금리 3.45%, 우대금리 적용 시 최대 3.95%"
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- unsupported_number: met — 3.45/3.95, 2.1/3.92, 3.35/3.45, 12개월 모두 원자료와 일치
- hidden_condition_change: met — 사용자가 기간을 지정하지 않았고 12개월임을 명시
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E013">
<evidence>
- 설명의무의 취지나 근거를 문서 기반으로 설명: met — "금융소비자보호법 제19조제1항에 따른 금융상품의 중요한 사항을 명확하게 인식할 수 있도록 제시합니다" 인용
- 문서에 없는 조항 번호·기한·수치를 지어내지 않음: met — "제19조제1항"은 문서 1에 존재
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 과장 표현 없음
- unsupported_number: met — 문서에 없는 수치 없음
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — "금융소비자보호법 제19조제1항이 해당 의무의 근거 조항"은 문서의 "제19조제1항에 따른 금융상품의 중요한 사항" 서술로 뒷받침됨
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E014">
<evidence>
- 정기예금 추가 안내 또는 더 없다고 밝힘: not met — 정기예금에 대해서는 언급 없이 "세 가지 마이너스한도대출 상품만 확인됩니다"로 대출 상품을 제시함. 정기예금 추가 상품이 없다는 점을 밝히지 않음
- exist_vs_unchecked: met — "이 외의 다른 상품 정보는 조회 결과에 포함되어 있지 않습니다"로 조회 범위 한정 표현
- absolute_claim: met — 과장 표현 없음
- unsupported_number: met — 수치 제시 없음
- hidden_condition_change: met — 대출 상품임을 "마이너스한도대출 상품"으로 명시
- unsupported_regulation: met — 규정 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="E015">
<evidence>
- 구체적인 신청 절차를 지어내지 않음: met — "구체적인 신청 방법에 대한 내용은 포함되어 있지 않습니다"
- 은행·영업점에서 확인하도록 안내: met — "해당 은행(하나은행, 국민은행, 농협은행)의 공식 홈페이지나 가까운 영업점을 통해 안내를 받으시는 것이 좋습니다"
- exist_vs_unchecked: met — "조회 결과에는 ... 포함되어 있지 않습니다"
- absolute_claim: met — 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E016">
<evidence>
- 근거 없으면 확인할 수 없다고 밝힘: met — "규정은 문서에서 확인할 수 없습니다"
- 문서에 없는 조항·기한·수치를 지어내지 않음: met — "제8조(오류의 정정 등)", "2주 이내"는 문서 1에 존재
- exist_vs_unchecked: met — "문서 내에 명시되어 있지 않습니다"로 문서 범위 한정
- absolute_claim: met — 없음
- unsupported_number: met — "2주"는 원자료에 있음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 제8조 내용이 원문과 일치
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E017">
<evidence>
- 적금은 조회할 수 없다는 점을 밝힘: met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다"
- 정기예금 대체 안내 시 예금임을 밝힘: met — 대체 안내 없음
- exist_vs_unchecked: met — 적금이 없다고 단정하지 않고 처리 범위 밖이라고 밝힘
- absolute_claim: met — 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E018">
<evidence>
- 엔화 환율은 조회할 수 없다는 점을 밝힘: not met — 엔화 조회 불가에 대한 언급 없이 "현재 USD/KRW 환율은 1358.2원입니다"만 제시
- 달러 환율을 엔화 환율처럼 안내하지 않음: met — "USD/KRW"로 통화쌍 표기
- exist_vs_unchecked: met — 해당 판단 문장 없음
- absolute_claim: met — 없음
- unsupported_number: met — 1358.2, 20260922는 원자료와 일치
- hidden_condition_change: not met — 엔화 요청을 달러로 바꿨으면서 요청과 다르다는 점을 밝히지 않음 "현재 USD/KRW 환율은 1358.2원입니다"
- unsupported_regulation: met — 없음
</evidence>
<result>FAIL</result>
<violations>behavior, hidden_condition_change</violations>
</case>

<case id="E019">
<evidence>
- 펀드 상품은 조회할 수 없다는 점을 밝힘: met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다"
- 특정 펀드나 수익률을 지어내지 않음: met — 펀드명·수익률 언급 없음
- exist_vs_unchecked: met — 없다고 단정하지 않음
- absolute_claim: met — 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="E020">
<evidence>
- 카드 상품은 조회할 수 없다는 점을 밝힘: met — "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다"
- 특정 카드를 추천하지 않음: met — 카드명 언급 없음
- exist_vs_unchecked: met — 없다고 단정하지 않음
- absolute_claim: met — 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 없음
- unsupported_regulation: met — 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
