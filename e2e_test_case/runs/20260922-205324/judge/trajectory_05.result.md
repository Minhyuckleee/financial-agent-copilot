<case id="C021">
<evidence>
- 금리 낮은 주담대 추천 요청을 product_recommendation 으로 라우팅함
- 필터 없이 recommend_mortgage_loan_products 를 호출해 결과 3건을 받음
- 가드레일 확인 후 최종 답변으로 이어지는 흐름이 논리적이고 효율적임
- 최종 답변이 최저 금리 상품을 골라 비교 정보를 제공해 목표를 달성함
</evidence>
<result>PASS</result>
</case>

<case id="C022">
<evidence>
- 신한은행 주담대 금리 질의를 product_recommendation 으로 라우팅함
- bank_name_filter "신한"으로 도구를 호출해 결과 2건을 받음
- 불필요한 단계 없이 가드레일 확인 후 최종 답변으로 진행함
- 최종 답변이 신한은행 상품 2개의 금리 범위를 제시함
</evidence>
<result>PASS</result>
</case>

<case id="C023">
<evidence>
- 하나은행 주담대 상품 존재 여부 질의를 올바르게 라우팅함
- bank_name_filter "하나은행"으로 도구를 호출해 결과 1건을 받음
- 단계가 최소한이고 논리적으로 이어짐
- 최종 답변이 상품명과 금리 범위를 제시하며 질문에 답함
</evidence>
<result>PASS</result>
</case>

<case id="C024">
<evidence>
- 주택 구입 대출 금리 문의를 주담대 추천으로 해석해 라우팅함
- 필터 없이 도구를 호출해 결과 3건을 받음
- 가드레일 확인 후 최종 답변으로 진행해 흐름이 효율적임
- 최종 답변이 3개 은행의 금리를 비교하고 주의 문구를 덧붙임
</evidence>
<result>PASS</result>
</case>

<case id="C025">
<evidence>
- 은행별 주담대 금리 비교 요청을 product_recommendation 으로 라우팅함
- 필터 없이 도구를 호출해 여러 은행 결과 3건을 받음
- 불필요한 재시도나 중복 호출 없이 가드레일 확인 후 최종 답변으로 진행함
- 최종 답변이 은행별 금리 범위를 비교해 제시함
</evidence>
<result>PASS</result>
</case>
