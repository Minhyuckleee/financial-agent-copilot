<case id="C001">
<evidence>
- 정기예금 금리 추천 요청이 product_recommendation 경로로 라우팅됨
- recommend_deposit_products를 오류 없이 한 번 호출했고 결과 3건을 받음 (기간을 따로 말하지 않아 12개월 기본값 사용은 합리적)
- 가드레일(disclosure_missing)을 거쳐 최종 답변에 고지 문구가 포함됨
- 불필요한 단계 없이 순서대로 진행됨
</evidence>
<result>PASS</result>
</case>

<case id="C002">
<evidence>
- 요청한 6개월이 save_term_months=6으로 정확히 반영됨
- 도구를 한 번 호출해 오류 없이 결과 3건을 받았고, 최종 답변에 3건이 모두 나열됨
- 가드레일을 거쳐 고지 문구가 포함됨
- 단계 흐름이 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="C003">
<evidence>
- 요청한 2년이 save_term_months=24로 정확히 변환됨
- 도구를 한 번 호출해 결과 3건을 받았고, 답변에서 최고 금리 상품을 제시함
- 가드레일을 거쳐 고지 문구가 포함됨
- 단계가 명확하고 효율적으로 진행됨
</evidence>
<result>PASS</result>
</case>

<case id="C004">
<evidence>
- 요청한 우리은행이 bank_name_filter="우리"로 반영됨 (기간은 지정하지 않아 필터를 넣지 않은 것이 적절)
- 도구를 한 번 호출해 결과 1건을 받았고, 답변이 그 결과와 일치함
- 가드레일을 거쳐 고지 문구가 포함됨
- 흐름이 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="C005">
<evidence>
- 요청한 하나은행과 3년이 bank_name_filter="하나", save_term_months=36으로 모두 반영됨
- 도구를 한 번 호출해 결과 1건을 받았고, 답변에 기본 금리와 우대 금리가 제시됨
- 가드레일을 거쳐 고지 문구가 포함됨
- 단계 흐름이 명확하고 효율적임
</evidence>
<result>PASS</result>
</case>
