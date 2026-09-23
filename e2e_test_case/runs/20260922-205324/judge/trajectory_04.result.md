<case id="C016">
<evidence>
- 국민은행 전세대출 금리 질의가 product_recommendation 경로로 라우팅됨
- bank_name_filter="국민은행"으로 도구를 1회 호출했고, 오류 없이 결과 2건을 받음
- 가드레일 통과 후 두 상품의 금리 범위를 답변함. 단계가 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="C017">
<evidence>
- 우리은행 상품 유무 질의가 추천 경로로 라우팅됨
- bank_name_filter="우리은행"으로 도구를 호출해 결과 2건을 받음
- 상품이 있음을 확인하고 상품명 2개와 금리를 제시함. 흐름이 명확하고 불필요한 단계가 없음
</evidence>
<result>PASS</result>
</case>

<case id="C018">
<evidence>
- 은행을 지정하지 않은 일반 금리 질의라서 필터 없이 도구를 1회 호출했고 결과 3건을 받음
- 조회 결과를 나열하고 전체 금리 범위(3.69%~6.4%)를 요약함
- 결과가 모두 NH 상품이지만 답변에 '조회된 상품' 기준임을 밝힘. 흐름이 논리적임
</evidence>
<result>PASS</result>
</case>

<case id="C019">
<evidence>
- 필터 없이 도구를 호출해 결과 3건을 받음. 여기까지는 논리적임
- 가드레일에서 prohibited_terms가 걸렸고, 이후 재생성이나 보정 없이 바로 finalize함
- 최종 답변이 "두 상품"이라고만 할 뿐 어떤 상품인지 이름을 밝히지 않음. 결과는 3건인데 두 상품이라고 해 지시 대상이 불명확함
- 가드레일 개입 후 답변이 손상된 채 마무리되어 사용자 목표(가장 싼 곳 식별)를 달성하지 못함
</evidence>
<result>FAIL</result>
</case>

<case id="C020">
<evidence>
- 농협 금리 질의에 bank_name_filter="농협"으로 도구를 1회 호출했고 결과 3건을 받음
- 가드레일 통과 후 NH 상품 3개의 금리를 제시함
- 단계가 일관되고 효율적이며 목표를 달성함
</evidence>
<result>PASS</result>
</case>
