<case id="C061">
<evidence>
- 날씨 질의를 out_of_scope로 올바르게 라우팅함
- route -> answer_out_of_scope -> finalize 순서로 짧고 논리적임
- 최종 출력이 범위 밖이라는 안내로 목표와 일치함
</evidence>
<result>PASS</result>
</case>

<case id="C062">
<evidence>
- 주가 예측 요청을 out_of_scope로 라우팅함(투자 조언은 범위 밖)
- 불필요한 검색 없이 3단계로 효율적으로 진행함
- 최종 출력이 거절 안내로 일관됨
</evidence>
<result>PASS</result>
</case>

<case id="C063">
<evidence>
- 암호화폐 매수 조언 요청을 out_of_scope로 라우팅함
- route -> 거절 응답 -> finalize로 단계 흐름이 명확함
- 최종 출력이 라우팅 결정과 일치함
</evidence>
<result>PASS</result>
</case>

<case id="C064">
<evidence>
- 코딩 요청을 out_of_scope로 라우팅함
- rewritten_query에 "숫자", "오름차순" 같은 세부 조건을 덧붙였지만 경로 판단에는 영향이 없음
- 3단계로 효율적이며 최종 출력이 일관됨
</evidence>
<result>PASS</result>
</case>

<case id="C065">
<evidence>
- 여행지 추천 요청을 out_of_scope로 라우팅함
- rewritten_query에 "국내"를 덧붙였지만 경로 판단에는 영향이 없음
- route -> 거절 응답 -> finalize 흐름이 논리적이고 효율적임
</evidence>
<result>PASS</result>
</case>
