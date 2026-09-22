<case id="C011">
<evidence>
- behavior 1 (카카오뱅크 신용대출 안내) met: "일반신용대출은 연 7.93%, 마이너스한도대출은 연 8.65%입니다"
- behavior 2 (승인·한도 확정 표현 없음) met: "실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다"
- exist_vs_unchecked met: 조회된 두 상품을 그대로 안내함
- absolute_claim met: 단정 표현 없음
- unsupported_number met: 7.93, 8.65, 601~700점 모두 원자료에 있음
- hidden_condition_change met: "신용점수 601~700점 기준으로" 조건을 밝힘
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C012">
<evidence>
- behavior 1 (신한은행 750점 기준 금리 안내) met: "두 상품 모두 신용점수 701~800점 구간에 해당하는 금리입니다"
- behavior 2 (승인·한도 확정 표현 없음) met: "최종 확정됩니다"는 약관 확인을 가리키며 승인·한도를 확정하지 않음
- exist_vs_unchecked met: 조회 결과를 안내함
- absolute_claim met: 단정 표현 없음
- unsupported_number not met: "마이너스한도대출(마통)은 금리가 7.36%" — 원자료의 마이너스한도대출 금리는 6.52이고, 7.36은 일반신용대출 값임
- hidden_condition_change met: "701~800점 구간" 조건을 밝힘
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>FAIL</result>
<violations>unsupported_number</violations>
</case>

<case id="C013">
<evidence>
- behavior 1 (신용대출 상품 금리 비교) met: "농협은행 ... 5.72%", "하나은행 ... 6.12%", "우리은행 ... 6.22%"
- behavior 2 (승인·한도 확정 표현 없음) met: "각 은행별로 금리 차이가 있으니 참고하시기 바랍니다"
- exist_vs_unchecked met: 조회 결과를 안내함
- absolute_claim met: 단정 표현 없음
- unsupported_number met: 5.72, 6.12, 6.22, 601~700점 모두 원자료에 있음
- hidden_condition_change met: "신용점수 601~700점 기준으로" 조건을 밝힘
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C014">
<evidence>
- behavior 1 (마이너스통장 금리 안내, 또는 조회되지 않았다고 밝힘) not met: "요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다" — 금리를 안내하지 않았고, 조회하지 않았다는 사실도 밝히지 않음
- behavior 2 (승인·한도 확정 표현 없음) met: 확정 표현 없음
- exist_vs_unchecked met: 상품이 없다고 단정하지 않음 ("범위 밖입니다")
- absolute_claim met: 단정 표현 없음
- unsupported_number met: 숫자 없음
- hidden_condition_change met: 조건을 바꾸지 않음
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C015">
<evidence>
- behavior 1 (전세자금대출 상품을 금리와 함께 안내) not met: "참고로, 'NH전세대출(주택도시보증공사)' 상품의 최저 금리는 3.7%입니다" — 앞뒤 맥락이 없는 한 줄뿐이고, 금리가 낮은 곳을 물었는데 최저 금리가 3.69%인 두 상품을 빼고 가장 높은 3.7% 상품만 제시함
- behavior 2 (승인·한도 확정 표현 없음) met: 확정 표현 없음
- exist_vs_unchecked met: 없다는 주장 없음
- absolute_claim met: 단정 표현 없음
- unsupported_number met: 3.7은 원자료에 있음
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C016">
<evidence>
- behavior 1 (국민은행 전세자금대출 안내) met: "KB주택전세자금대출", "KB플러스전세자금대출"
- exist_vs_unchecked met: 조회 결과를 안내함
- absolute_claim met: "신청 조건이나 신용도 등에 따라 달라질 수 있으니"
- unsupported_number not met: "KB주택전세자금대출: 연 4.22% ~ 5.61%" — 원자료의 최저 금리는 4.21임
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>FAIL</result>
<violations>unsupported_number</violations>
</case>

<case id="C017">
<evidence>
- behavior 1 (우리은행 전세자금대출 안내) met: "네, 우리은행에는 전세자금대출 상품이 있습니다"
- exist_vs_unchecked met: 조회 결과를 근거로 있다고 답함
- absolute_claim met: 단정 표현 없음
- unsupported_number not met: "'우리전세론(서울보증)' 상품은 금리가 연 3.93%에서 4.59% 사이" — 원자료의 최저 금리는 3.89임
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>FAIL</result>
<violations>unsupported_number</violations>
</case>

<case id="C018">
<evidence>
- behavior 1 (전세자금대출 금리 안내) met: "전세대출 금리는 대략 연 3.69%에서 6.4% 사이로 확인됩니다"
- behavior 2 (승인·한도 확정 표현 없음) met: "실제 적용 금리는 신용도, 대출 조건 등에 따라 달라질 수 있으니"
- exist_vs_unchecked met: "현재 조회된 전세대출 상품의 금리는"
- absolute_claim met: 단정 표현 없음
- unsupported_number met: 3.69, 6.39, 3.7, 6.4 모두 원자료에 있음
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C019">
<evidence>
- behavior 1 (금리 수치를 근거로 안내) met: "최저 금리가 3.69%입니다"
- behavior 2 ('무조건 최고' 같은 단정 표현 없음) met: "현재 조회 결과 기준으로 ... 가장 낮은 곳은"
- exist_vs_unchecked met: 조회 결과 범위임을 밝힘
- absolute_claim met: 단정 표현 없음
- unsupported_number met: 3.69는 원자료에 있음
- hidden_condition_change met: 하나를 요청했지만 최저 금리가 같은 두 상품을 함께 제시했고, 이를 숨기지 않음
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C020">
<evidence>
- behavior 1 (농협 전세자금대출 안내) met: "NH전세대출(서울보증보험): 연 3.69% ~ 6.39%" 등 세 상품
- exist_vs_unchecked met: 조회 결과를 안내함
- absolute_claim met: 단정 표현 없음
- unsupported_number met: 모든 수치가 원자료와 일치함
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: 규제 언급 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
