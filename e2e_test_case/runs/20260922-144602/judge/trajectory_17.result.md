<case id="E011">
<evidence>
- 새 질문(주담대 금리)은 이전 환율 대화와 무관한 독립 질의이며, route=product_recommendation 으로 맞게 분류
- recommend_mortgage_loan_products 를 호출해 3건을 받았고, 다른 도구 호출 없이 바로 답변
- 최종 답변이 도구 결과(은행별 금리 범위)와 일치. 단계가 짧고 논리적
</evidence>
<result>PASS</result>
</case>

<case id="E012">
<evidence>
- "그럼 정기예금 추천해줘" 를 상품 추천으로 분류하고, recommend_deposit_products(12개월)를 한 번 호출
- guardrail 이 disclosure_missing/prohibited_terms 를 표시했고, 최종 답변에 고지 문구가 붙어 있어 반영된 것으로 보임
- 이전 약관 대화에서 추천으로 넘어가는 흐름이 자연스럽고, 불필요한 단계가 없음
</evidence>
<result>PASS</result>
</case>

<case id="E013">
<evidence>
- 맥락에 기대는 질문 "왜 그래요?" 를 설명의무의 법적 근거·취지를 묻는 질의로 다시 써서 policy_qa 로 분류
- 설명의무 가이드라인 두 종류에서 검색해 6건을 받았고, 이어서 답변 생성
- 이전 대화 맥락을 제대로 이어받았고, 단계가 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="E014">
<evidence>
- 직전 대화는 정기예금 추천이었으므로 "다른 것도 있어?" 는 다른 정기예금을 묻는 것
- 그런데 recommend_credit_loan_products 를 인자 없이 호출함. 도구 선택이 맥락과 어긋남
- 최종 답변은 사용자가 말한 적 없는 신용점수 구간(601~700점)을 전제로 마이너스한도대출을 제시. 사용자 의도에서 벗어남
</evidence>
<result>FAIL</result>
</case>

<case id="E015">
<evidence>
- 직전 에이전트 발화에는 "3건" 만 있고 은행 이름이 없어서, 같은 조건(credit_score=800)으로 한 번 다시 조회해 은행을 특정한 것은 이해할 수 있는 선택
- 다시 조회한 것 외에는 불필요한 단계가 없음. 답변은 해당 은행들의 공식 신청 채널을 일반적으로 안내하고, 구체 사항은 은행에 확인하라고 넘김
- 전체 흐름이 질문과 맞고, 비효율도 허용 범위 안
</evidence>
<result>PASS</result>
</case>
