<case id="E026">
<evidence>
- 예금자보호 한도 질의를 policy_qa로 분류하고 질의 재작성 후 검색으로 이어져 흐름이 논리적임
- 검색된 문서가 예금자보호와 무관하지만 에이전트가 이를 반영해 근거 없음을 밝히고 답을 지어내지 않음
- route -> context -> guardrail -> finalize 순서가 간결하고 불필요한 단계가 없음
</evidence>
<result>PASS</result>
</case>

<case id="E027">
<evidence>
- DSR 규제 질의를 policy_qa로 분류하고 질의를 적절히 구체화함
- 검색 결과에 DSR 근거가 없자 정보가 없다고 답하고 수치를 지어내지 않음
- 단계 진행이 명확하고 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="E028">
<evidence>
- LTV 한도 질의를 policy_qa로 분류하고 질의를 적절히 재작성함
- 검색 문서에 LTV 근거가 없자 확인할 수 없다고 답하고 환각이 없음
- route -> context -> guardrail -> finalize의 일관된 최소 경로임
</evidence>
<result>PASS</result>
</case>

<case id="E029">
<evidence>
- 특정 고객 계좌 잔액 조회는 문서 기반 QA 범위 밖이므로 out_of_scope 분류가 타당함
- 불필요한 검색 없이 answer_out_of_scope -> finalize로 바로 종료해 효율적임
- 최종 출력이 범위 밖 요청임을 안내해 목표와 일치함
</evidence>
<result>PASS</result>
</case>

<case id="E030">
<evidence>
- 개별 고객의 대출 승인 및 한도 판단 요청을 out_of_scope로 분류한 것이 타당함
- 검색을 하지 않고 거절 경로로 바로 가 효율적임
- 최종 출력이 범위 밖 안내로 분류 결과와 일관됨
</evidence>
<result>PASS</result>
</case>
