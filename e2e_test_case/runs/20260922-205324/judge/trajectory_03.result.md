<case id="C011">
<evidence>
- 신용대출 금리 질의가 product_recommendation으로 라우팅되고, 카카오뱅크 필터로 신용대출 도구를 호출함
- 도구가 결과 2건을 반환했고, 공시 문구 가드레일을 거쳐 답변을 마무리함
- 최종 답변은 두 상품의 금리를 제시하고 고지 문구를 포함함. 단계가 효율적이고 논리적임
</evidence>
<result>PASS</result>
</case>

<case id="C012">
<evidence>
- 라우팅이 적절하고, 도구 인자에 credit_score=750과 은행 필터 "신한"이 정확히 반영됨
- 결과 2건이 701~800점 구간 금리로 답변에 반영됨
- 공시 가드레일을 거쳐 마무리하는 흐름이 명확함
</evidence>
<result>PASS</result>
</case>

<case id="C013">
<evidence>
- 여러 은행 비교 요청에 필터 없이 신용대출 도구를 호출한 것이 적절함
- 결과 3건을 은행별 금리 비교로 정리함
- 공시 가드레일과 마무리까지 흐름이 효율적이고 일관됨
</evidence>
<result>PASS</result>
</case>

<case id="C014">
<evidence>
- 마이너스통장 금리 비교는 서비스 범위 안의 신용대출 상품 질의인데 out_of_scope로 잘못 라우팅됨
- 도구를 한 번도 호출하지 않고 거절 답변으로 끝남
- 다시 쓴 질의 자체는 정확한데도 범위 밖으로 분류해, 판단과 목표가 맞지 않음
</evidence>
<result>FAIL</result>
</case>

<case id="C015">
<evidence>
- 라우팅과 전세대출 도구 호출(결과 3건)은 적절함
- prohibited_terms 가드레일을 거친 뒤 최종 답변이 "참고로"로 시작하는 한 문장만 남아, 본문이 잘려 나간 것으로 보임
- 도구 결과 3건 중 1건만 전달됐고 공시 문구도 빠짐. 마지막 단계가 답변의 질을 떨어뜨림
</evidence>
<result>FAIL</result>
</case>
