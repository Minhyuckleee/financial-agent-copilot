<case id="E011">
<evidence>
- 이전 대화가 환율 주제였지만 새 질문(주담대 금리)을 독립 질의로 올바르게 처리함
- product_recommendation 라우팅 후 recommend_mortgage_loan_products 호출, 3건 반환
- 가드레일 통과 후 은행별 금리를 제시해 목표 달성, 단계가 간결하고 논리적
</evidence>
<result>PASS</result>
</case>

<case id="E012">
<evidence>
- 약관 열람 질문에서 정기예금 추천으로 주제 전환을 올바르게 인식
- recommend_deposit_products(12개월) 호출, 3건 반환
- 가드레일(disclosure_missing, prohibited_terms) 후 고지문구 포함 최종 답변, 흐름이 명확하고 효율적
</evidence>
<result>PASS</result>
</case>

<case id="E013">
<evidence>
- "왜 그래요?"를 이전 대화(설명의무)의 맥락으로 설명의무 근거·이유 질의로 재작성함
- 설명의무 가이드라인 문서를 검색해 가져온 뒤 가드레일 거쳐 답변
- 법적 근거(금소법 제19조제1항)와 문서 인용으로 답해 단계 간 연결이 논리적이고 효율적
</evidence>
<result>PASS</result>
</case>

<case id="E014">
<evidence>
- 이전 대화는 정기예금 추천이므로 "다른 것도 있어?"는 다른 정기예금 상품을 묻는 질문임
- 그런데 recommend_deposit_products가 아닌 recommend_credit_loan_products를 호출함(도구 선택 오류)
- 최종 답변이 마이너스한도대출을 안내해 사용자 목표에서 벗어남
</evidence>
<result>FAIL</result>
</case>

<case id="E015">
<evidence>
- 질문은 앞서 추천한 신용대출의 신청 방법을 묻는 후속 질문임
- 신청 절차 정보가 없는 상품 추천 도구(recommend_credit_loan_products)를 다시 호출해 질문 해결에 기여하지 않음
- 최종 답변은 조회 결과에 신청 방법이 없다고 하며 은행 문의만 안내함. 질문 의도에 맞게 진행되지 않은 궤적
</evidence>
<result>FAIL</result>
</case>
