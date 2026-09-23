<case id="E021">
<evidence>
- 주담대만 요청 -> product_recommendation 라우팅 -> recommend_mortgage_loan_products 호출(전세대출 도구 아님)로 의도와 일치
- 도구 3건 결과를 그대로 요약하고 전세대출 제외를 명시
- route -> tool -> guardrail -> finalize 단계가 간결하고 논리적
</evidence>
<result>PASS</result>
</case>

<case id="E022">
<evidence>
- 개인사업자 대출 문의 -> recommend_business_loan_products 호출로 도구 선택 적절
- credit_score 700은 사용자가 주지 않은 값이나 답변에서 601~700점 구간 기준임을 밝혀 투명하게 처리
- 오류 없이 3건 결과를 받아 요약, 단계 진행이 명확하고 효율적
</evidence>
<result>PASS</result>
</case>

<case id="E023">
<evidence>
- 월세 보증금 대출 금리는 대출 상품 금리 문의로 도메인 범위 안에 있는 질문
- route_query가 out_of_scope로 잘못 라우팅되어 도구 호출 없이 바로 거절
- 쿼리 재작성까지 했지만 상품 조회를 전혀 시도하지 않아 목표를 달성하지 못함
</evidence>
<result>FAIL</result>
</case>

<case id="E024">
<evidence>
- "이번엔 개인 신용대출" 의도를 반영해 사업자 대출이 아닌 recommend_credit_loan_products 호출
- guardrail이 disclosure_missing을 감지했고, 최종 답변에 고지 문구가 추가되어 반영됨
- credit_score 700 가정은 답변에 구간으로 명시됨. 전체 흐름이 논리적이고 효율적
</evidence>
<result>PASS</result>
</case>

<case id="E025">
<evidence>
- policy_qa 라우팅은 적절하나 검색 결과가 온라인 설명의무 가이드라인/신용정보법뿐이고 금리인하요구권 관련 문서(은행법 등)는 없음
- 관련 없는 검색 결과를 받은 뒤 재검색이나 쿼리 재구성을 한 번도 시도하지 않음
- 최종적으로 "문서에서 확인할 수 없음"으로 끝나 사용자 목표를 달성하지 못함
</evidence>
<result>FAIL</result>
</case>
