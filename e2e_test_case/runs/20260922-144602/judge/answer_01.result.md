<case id="C001">
<evidence>
- 정기예금 상품을 금리와 함께 안내: not met (partial; answer is a fragment starting mid-thought and omits the top product 광주은행 굿스타트예금) - "그 외에도 부산은행의 '더(The) 특판 정기예금'이 최대 3.92%"
- 가입기간 기준 명시: not met - no term (12개월) mentioned anywhere; "금리와 조건을 비교해보시고"
- 단정 표현 미사용: met - "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met (not applicable)
- unsupported_number: met - "최대 3.92%", "최대 3.45%" match source
- hidden_condition_change: met (no condition changed)
- unsupported_regulation: met (none claimed)
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C002">
<evidence>
- 6개월 기준 정기예금 안내: met - "6개월짜리 정기예금 상품은 다음과 같습니다."
- exist_vs_unchecked: met (not applicable)
- absolute_claim: met - "각 상품의 금리와 조건을 참고해보시기 바랍니다."
- unsupported_number: met - "연 2.5%", "연 3.72%", "연 3.2%", "연 3.55%", "연 3.15%", "연 3.25%" all in source
- hidden_condition_change: met - term kept at 6개월
- unsupported_regulation: met (none claimed)
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C003">
<evidence>
- 24개월 기준 정기예금 안내: met - "2년(24개월)짜리 예금 상품 중 금리가 높은 곳은 다음과 같습니다."
- exist_vs_unchecked: met (not applicable)
- absolute_claim: met - "우대금리 적용 시 가장 높은 금리(3.92%)" is conditioned, not absolute
- unsupported_number: met - "3.92%", "3.82%", "3.0%" match source
- hidden_condition_change: met - term kept at 24개월
- unsupported_regulation: met (none claimed)
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C004">
<evidence>
- 우리은행 정기예금 안내: met - "우리은행의 정기예금 상품으로는 \"WON플러스예금\"이 있습니다."
- exist_vs_unchecked: met (not applicable; product found)
- absolute_claim: met - "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- unsupported_number: met - "12개월", "연 3.5%" match source
- hidden_condition_change: met (none)
- unsupported_regulation: met (none claimed)
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C005">
<evidence>
- 하나은행 36개월 정기예금 안내: met - "하나은행의 3년(36개월) 정기예금 금리는 기본 연 2.3%이고"
- exist_vs_unchecked: met (not applicable)
- absolute_claim: met - "우대금리 적용 시 최대 연 2.7%"
- unsupported_number: met - "2.3%", "2.7%" match source
- hidden_condition_change: met - term kept at 36개월
- unsupported_regulation: met (none claimed)
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C006">
<evidence>
- 정기예금 상품을 금리와 함께 안내: not met - announces a list but gives no product or rate: "이자를 많이 주는 예금 상품은 다음과 같습니다." followed directly by the disclaimer
- 단정 표현 미사용: met - no absolute claims
- exist_vs_unchecked: met (not applicable)
- unsupported_number: met - "1년(12개월)" matches source
- hidden_condition_change: met - "1년(12개월) 기준" disclosed
- unsupported_regulation: met (none claimed)
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C007">
<evidence>
- 12개월 기준 정기예금을 우대금리와 함께 안내: not met - fragment that begins "그 다음으로는" and omits the highest product (광주은행 굿스타트예금 3.95%); term not stated
- 단정 표현 미사용: met - "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met (not applicable)
- unsupported_number: met - "3.92%", "3.45%" match source
- hidden_condition_change: met (none)
- unsupported_regulation: met (none claimed)
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C008">
<evidence>
- 신용대출 상품을 금리와 함께 안내: met - "농협은행주식회사의 '가계신용대출(마이너스대출)'로, 금리는 5.72%입니다"
- 승인·한도 확정 표현 미사용: met - no approval/limit claim; "참고하시면 좋겠습니다"
- exist_vs_unchecked: met (not applicable)
- absolute_claim: met
- unsupported_number: met - "5.72%", "6.12%", "6.22%", "601~700점" match source
- hidden_condition_change: met - basis disclosed: "신용점수 601~700점 기준으로"
- unsupported_regulation: met (none claimed)
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C009">
<evidence>
- 신용점수 900점 기준 상품 안내: met - "신용점수가 900점일 경우, 조회 결과 기준으로 ... 수협은행의 '개인신용대출'(일반신용대출)로, 금리는 5.18%" (source band 801~900점 includes 900)
- 승인·한도 확정 표현 미사용: met - no approval/limit claim
- exist_vs_unchecked: met (not applicable)
- absolute_claim: met
- unsupported_number: met - "5.18%", "5.19%", "5.7%" match source
- hidden_condition_change: met (900 is within the source band)
- unsupported_regulation: met (none claimed)
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C010">
<evidence>
- 점수 조건에 맞는 금리 안내: not met - user is 600점대 초반 (601+), but answer gives 501~600 band rates as applicable: "위 금리는 모두 신용점수 501~600점 구간에 해당하는 일반신용대출 상품 기준입니다."
- 승인·한도 확정 표현 미사용: met (borderline) - "받을 수 있는 신용대출 금리는 다음과 같습니다" frames rates as available but does not confirm approval or limit
- exist_vs_unchecked: met (not applicable)
- absolute_claim: met
- unsupported_number: met - "7.25%", "7.45%", "8.1%" match source
- hidden_condition_change: met - band change is stated: "501~600점 구간에 해당하는"
- unsupported_regulation: met (none claimed)
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>
