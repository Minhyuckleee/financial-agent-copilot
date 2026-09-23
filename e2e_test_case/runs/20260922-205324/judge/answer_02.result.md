<case id="C011">
<evidence>
- behavior(카카오뱅크 신용대출 안내): met — "일반신용대출은 연 7.93%, 마이너스한도대출은 연 8.65%입니다"
- behavior(승인/한도 확정 표현 없음): met — "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met — 조회 결과를 그대로 안내함
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — "7.93%", "8.65%", "601~700점" 모두 원자료에 있음
- hidden_condition_change: met — 신용점수 구간을 "신용점수 601~700점 기준으로"라고 밝힘
- unsupported_regulation: met — 규제 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="C012">
<evidence>
- behavior(신한은행 750점 기준 금리 안내): met — "마이너스한도대출(마통)은 금리가 6.52%", "일반신용대출은 금리가 7.36%"
- behavior(승인/한도 확정 표현 없음): met — "상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met — 조회 결과 안내
- absolute_claim: met — 단정 표현 없음
- unsupported_number: met — 6.52, 7.36, 701~800 모두 원자료에 있음
- hidden_condition_change: met — "신용점수 701~800점 구간에 해당하는 금리입니다"라고 구간을 밝힘
- unsupported_regulation: met — 규제 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="C013">
<evidence>
- behavior(신용대출 상품 금리 비교): met — "농협은행...5.72%", "하나은행...6.12%", "우리은행...6.22%"
- behavior(승인/한도 확정 표현 없음): met — "상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked: met — 조회 결과 안내
- absolute_claim: met — "각 은행별로 금리 차이가 있으니 참고하시기 바랍니다"
- unsupported_number: met — 모든 수치가 원자료에 있음
- hidden_condition_change: met — "신용점수 601~700점 기준으로"라고 밝힘
- unsupported_regulation: met — 규제 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="C014">
<evidence>
- behavior(마이너스통장 금리 안내 또는 미조회 사실 명시): not met — 조회 없이 "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다"라고만 답함
- behavior(승인/한도 확정 표현 없음): met — 해당 표현 없음
- exist_vs_unchecked: met — 상품이 없다고 주장하지는 않음 ("범위 밖입니다")
- absolute_claim: met — 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: met — 해당 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>
<case id="C015">
<evidence>
- behavior(전세자금대출 상품 금리와 함께 안내): not met — "'NH전세대출(주택도시보증공사)' 상품의 최저 금리는 3.7%입니다"라고 한 상품만 제시했으며, 이보다 낮은 3.69% 상품(서울보증보험, 주택금융공사)을 빠뜨려 "금리 낮은 데"라는 질문에 답하지 못함
- behavior(승인/한도 확정 표현 없음): met — 해당 표현 없음
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 없음
- unsupported_number: met — "3.7%"는 원자료에 있음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: met — 해당 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>
<case id="C016">
<evidence>
- behavior(국민은행 전세자금대출 안내): met — "KB주택전세자금대출: 연 4.21% ~ 5.61%", "KB플러스전세자금대출: 연 4.22% ~ 5.62%"
- exist_vs_unchecked: met — 조회 결과 안내
- absolute_claim: met — "신청 조건이나 신용도 등에 따라 달라질 수 있으니"
- unsupported_number: met — 모든 수치가 원자료에 있음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="C017">
<evidence>
- behavior(우리은행 전세자금대출 안내): met — "'우리전세론(서울보증)' 상품은 금리가 연 3.89%에서 4.59%", "'우리전세론(주택금융보증)' 상품은 연 3.93%에서 4.63%"
- exist_vs_unchecked: met — "네, 우리은행에는 전세자금대출 상품이 있습니다"라는 표현이 조회 결과로 뒷받침됨
- absolute_claim: met — 없음
- unsupported_number: met — 모든 수치가 원자료에 있음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="C018">
<evidence>
- behavior(전세자금대출 금리 안내): met — "대략 연 3.69%에서 6.4% 사이로 확인됩니다"
- behavior(승인/한도 확정 표현 없음): met — "실제 적용 금리는 신용도, 대출 조건 등에 따라 달라질 수 있으니"
- exist_vs_unchecked: met — "현재 조회된 전세대출 상품의 금리는"
- absolute_claim: met — 없음
- unsupported_number: met — 3.69, 6.39, 3.7, 6.4 모두 원자료에 있음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
<case id="C019">
<evidence>
- behavior(금리 수치 근거 안내): not met — "두 상품 모두 최저 금리가 3.69%로 가장 저렴합니다"라고만 하고 어느 은행·상품인지 밝히지 않아 실제 안내가 되지 않음
- behavior('무조건 최고' 같은 단정 표현 없음): met — "가장 저렴합니다"는 수치 비교에 근거한 표현임
- exist_vs_unchecked: met — 해당 없음
- absolute_claim: met — 없음
- unsupported_number: met — "3.69%"는 원자료에 있음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: met — 해당 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>
<case id="C020">
<evidence>
- behavior(농협 전세자금대출 안내): met — "NH전세대출(서울보증보험): 연 3.69% ~ 6.39%" 등 3개 상품을 모두 안내함
- exist_vs_unchecked: met — 조회 결과 안내
- absolute_claim: met — 없음
- unsupported_number: met — 모든 수치가 원자료에 있음
- hidden_condition_change: met — 해당 없음
- unsupported_regulation: met — 해당 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
