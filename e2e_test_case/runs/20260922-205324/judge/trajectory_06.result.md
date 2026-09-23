<case id="C026">
<evidence>
- 금리 질문을 product_recommendation으로 라우팅하고 주담대 도구를 기업은행 필터로 호출함. 흐름이 논리적임
- 결과 1건을 얻은 뒤 guardrail을 거쳐 finalize까지 곧바로 진행해 효율적임
- 최종 답변이 질문에 직접 답함(IBK주택담보대출 4.89%)
</evidence>
<result>PASS</result>
</case>

<case id="C027">
<evidence>
- 라우팅과 사업자대출 도구 호출(결과 3건)까지는 적절함
- prohibited_terms guardrail이 발동한 뒤 최종 답변이 "그 다음으로는"으로 시작함. 금리가 가장 낮은 1순위 상품이 빠진 잘린 답변임
- 목표인 "금리 낮은 곳"을 제대로 안내하지 못함. guardrail 단계가 답변을 훼손했는데 이를 복구하는 단계가 없음
</evidence>
<result>FAIL</result>
</case>

<case id="C028">
<evidence>
- 신용점수 800을 도구 인자로 정확히 넘겨 사업자대출 도구를 호출함(결과 3건)
- guardrail 이후 finalize로 이어지는 진행이 명확하고 효율적임
- 최종 답변에 최저금리 상품과 비교 금리가 온전히 담겨 질문에 답함
</evidence>
<result>PASS</result>
</case>

<case id="C029">
<evidence>
- 은행 필터로 호출했으나 결과가 없어 필터를 "국민"으로 바꿔 한 번 재시도함. 빈 결과 뒤 1회 재시도는 허용 범위임
- 재시도 후 tier2_exhausted로 처리하고 low_confidence 고지와 함께 마무리함. 논리적인 종료임
- 최종 답변이 조회 결과가 없다는 점을 정직하게 안내함
</evidence>
<result>PASS</result>
</case>

<case id="C030">
<evidence>
- 비교 요청을 사업자대출 도구 1회 호출로 처리함(결과 3건). guardrail과 finalize 흐름이 간결함
- 최종 답변이 3개 상품의 금리를 비교하고 최저금리 상품을 명시해 목표를 달성함
- 사용자가 신용점수를 주지 않았는데 답변은 기본 구간(601~700점)을 전제로 함. 경미한 사항이며 궤적의 논리성을 해치지 않음
</evidence>
<result>PASS</result>
</case>
