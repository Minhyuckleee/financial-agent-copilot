<case id="C039">
<evidence>
- 영업시간 중 열람·교부 청구 안내: met — "거래처(고객)는 영업시간 중 언제든지 이 약관을 볼 수 있고, 그 교부를 청구할 수 있습니다"
- 조항 번호·기한·수치 날조 없음: met — 조항 번호나 수치를 쓰지 않음, "은행 영업점에 비치되어 있으며"는 문서 1 서문과 일치
- exist_vs_unchecked: met (해당 없음, 문서에 있는 내용을 그대로 안내)
- absolute_claim: met — 과장 표현 없음
- unsupported_number: met — 수치 없음
- hidden_condition_change: met — 조건 변경 없음
- unsupported_regulation: met — "문서에 따르면" 서문 내용만 사용
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C040">
<evidence>
- 분실 신고 절차를 약관 근거로 안내: not met — "통장 또는 인감을 분실한 경우 취해야 할 조치(예: 분실신고, 재발급 절차 등)에 관한 구체적인 규정이 포함되어 있지 않습니다". 제공된 source_data(제4조·제5조·제10조·제18조 일부)에도 분실 신고 조항은 없으므로 답변 자체는 source 와 맞지만, 기대 행동 항목은 충족되지 않음
- 조항 번호·기한·수치 날조 없음: met — 수치·조항 번호를 쓰지 않음
- exist_vs_unchecked: met — "제공해주신 문서의 내용에는 ... 포함되어 있지 않습니다. 따라서 ... 문서에서 확인할 수 없다"로 제공 문서 범위에서 확인 불가라고 한정함
- absolute_claim: met
- unsupported_number: met
- hidden_condition_change: met
- unsupported_regulation: met
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C041">
<evidence>
- 전화 동의 가능 여부 결론 + 문서 근거: met — "네, 전화 통화를 통해 개인정보 수집에 대한 동의를 받는 것은 관련 법령상 허용됩니다", 문서 5("전화상으로 ... 동의를 받을 수 있다")와 문서 6 Q50 인용
- 조항 번호·기한·수치 날조 없음: met — "보호법 제22조 제1항, 보호법 시행령 제17조 제2항"은 문서 6에 있음. 다만 첫 인용 출처를 "문서(Page 428)"로 적었는데, 이 문장은 해설서 Page 91 앞쪽 구간(문서 5)에 있어서 쪽 번호가 틀림. 위반 목록에서 말하는 수치(금리·한도·날짜·금액)에는 해당하지 않음
- exist_vs_unchecked: met (해당 없음)
- absolute_claim: met — "녹취 등 입증 가능한 방법을 사용하는 것이 필요합니다"로 조건을 붙임
- unsupported_number: met
- hidden_condition_change: met
- unsupported_regulation: met — 인용 조문 모두 source 에 있음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C042">
<evidence>
- 처리방침 기재 사항을 문서 근거로 안내: met — 제30조 각 호를 1~10으로 나열("개인정보의 처리 목적" ... "자동으로 수집하는 장치의 설치·운영 및 그 거부에 관한 사항")했고 문서 3·6과 일치함
- 조항 번호·기한·수치 날조 없음: met — "제21조제1항 단서", "제23조제3항", "제28조의2 및 제28조의3"은 모두 문서 3에 있음. 작성 원칙("명시적으로 구분하고, 알기 쉬운 용어로")은 표준지침 제18조제1항 설명과, "~등" 지양·법적 근거 구분 기재는 문서 5와 일치함
- exist_vs_unchecked: met (해당 없음)
- absolute_claim: met
- unsupported_number: met
- hidden_condition_change: met
- unsupported_regulation: met — "14세 미만 아동 ... (해당시)"는 문서 2 표에 있고, 보호책임자 업무 내용은 문서 5에 있음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C043">
<evidence>
- 통지·신고 기한을 문서 근거로 안내: not met — 신고 기한만 안내함("72시간 이내에 관계 기관(개인정보보호위원회 또는 전문기관)에 신고해야 합니다"). 정보주체 통지 기한(제26조 72시간, 법 제34조 "지체 없이")은 빠져 있음
- 조항 번호·기한·수치 날조 없음: met — "제40조", "72시간"은 문서 2에 있음
- exist_vs_unchecked: met (해당 없음)
- absolute_claim: met
- unsupported_number: met
- hidden_condition_change: met — 사용자가 준 조건을 바꾸지는 않음
- unsupported_regulation: not met — 제40조를 인용하면서 "다음 각 호의 어느 하나에 해당하는 경우로서"를 빼고 "개인정보가 유출된 사실을 알게 되었을 때에는 72시간 이내에 ... 신고해야 합니다"라고 적어, 모든 유출이 신고 대상인 것처럼 안내함. source 에서 신고 대상은 1천명 이상·민감/고유식별정보·외부 불법접근 경우로 한정되며(문서 3), 위험이 현저히 낮아진 경우의 신고 면제도 생략됨
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_regulation</violations>
</case>
