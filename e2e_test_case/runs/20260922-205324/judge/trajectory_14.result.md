<case id="C066">
<evidence>
- 후속 질문 "24개월로도"를 product_recommendation으로 라우팅함
- recommend_deposit_products를 save_term_months=24로 호출했고 3건을 받음
- disclosure 가드레일 후 고지 문구를 붙여 마무리함. 단계가 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="C067">
<evidence>
- history의 신용대출 맥락을 이어받아 credit_score=850으로 recommend_credit_loan_products를 호출함
- 3건을 받았고 disclosure 가드레일 후 마무리함
- 불필요한 단계 없이 순서대로 진행됨
</evidence>
<result>PASS</result>
</case>

<case id="C068">
<evidence>
- 재조회 요청을 exchange_rate로 라우팅하고 inquire_exchange_rate를 한 번 호출함
- 새로 조회한 값과 기준일로 답변함
- 짧고 효율적인 흐름임
</evidence>
<result>PASS</result>
</case>

<case id="C069">
<evidence>
- 이전 전세자금대출 맥락에 bank_name_filter="국민"을 적용해 recommend_jeonse_loan_products를 호출함
- 2건을 받아 둘 다 국민은행 상품으로 제시함
- 단계가 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="C070">
<evidence>
- 후속 질문을 policy_qa로 라우팅하고 약관 교부 여부로 쿼리를 재작성함
- 예금거래기본약관 청크를 검색했고, 그 근거로 교부 청구가 가능하다고 답함
- 명확하게 진행되고 효율적임
</evidence>
<result>PASS</result>
</case>
