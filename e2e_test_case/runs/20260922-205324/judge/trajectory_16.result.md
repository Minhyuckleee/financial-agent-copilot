<case id="E006">
<evidence>
- 후속 질의 "하나은행 걸로"를 상품추천으로 라우팅하고, 이전 대화의 6개월 조건을 유지한 채 bank_name_filter "하나"를 적용함
- 도구 호출 1회로 결과 1건을 얻었고, disclosure_missing 가드레일에 따라 고지 문구가 추가됨
- 단계 간 흐름이 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="E007">
<evidence>
- 신용점수 650점 맥락을 이어받아 recommend_business_loan_products를 credit_score 650으로 호출함
- 대출 종류 전환이 올바르며, 결과 3건이 최종 답변에 반영됨
- 불필요한 단계 없이 곧바로 진행됨
</evidence>
<result>PASS</result>
</case>

<case id="E008">
<evidence>
- "전세대출은?"을 전세대출 추천으로 해석하고, 이전 대화의 농협 은행 필터를 이어받음
- recommend_jeonse_loan_products 1회 호출로 결과 3건을 얻어 답변에 반영함
- 진행이 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="E009">
<evidence>
- 주제가 바뀐 질의를 exchange_rate로 올바르게 라우팅함
- inquire_exchange_rate 1회 호출 결과를 그대로 답변에 사용함
- 단계가 최소한이고 목표와 일치함
</evidence>
<result>PASS</result>
</case>

<case id="E010">
<evidence>
- 개인정보 수집 동의 질문을 policy_qa로 라우팅하고, 대화 맥락을 반영해 질의를 재작성함
- 관련 법령·지침 문서(개인정보 질의응답, 신용정보법, 해설서)를 검색해 근거로 활용함
- 검색 결과를 바탕으로 조항별 답변을 생성하여, 흐름이 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>
