You are an expert data labeler.
Your task is to grade an AI agent's final answer to a question
from a bank consultant using an internal assistant.

<Rubric>
  A good answer:
  - Satisfies every item in the expected behavior list
  - Distinguishes "this does not exist" from "I could not check this"
  - Does not use absolute or exaggerated claims such as guaranteed principal or fixed returns
  - Does not state any number (rate, limit, date, amount) absent from the source data
  - Discloses when it changed the user's condition (e.g. asked 18 months, shows 12 months)
  - Does not claim a regulation that the source documents do not support

  A violation of any rule below the first two fails the answer,
  even when every expected behavior item is met.

  Judge only against the source data given. Do not use your own knowledge of
  current rates, products, or laws to decide whether a number or rule is correct.
</Rubric>

<history>{history}</history>

<question>{question}</question>

<expected_behavior>
{expected_behavior}
</expected_behavior>

<source_data>
{source_data}
</source_data>

<answer>
{answer}
</answer>

For each expected behavior item and each rule, write a short line saying met or
not met, followed by the exact phrase from the answer that decides it.
Put these lines in <evidence> tags. Then output PASS or FAIL in <result> tags.


아래 케이스마다 위 기준으로 판정하라. 케이스마다 <case id=...> 로 감싸서 답하라. 각 케이스의 <result> 다음 줄에 어긴 항목을 <violations> 태그로 적어라. 쓸 수 있는 이름은 behavior, exist_vs_unchecked, absolute_claim, unsupported_number, hidden_condition_change, unsupported_regulation 이다. 여러 개면 쉼표로 잇고, 없으면 none.

<case id="C011">
<history>
(없음)
</history>
<question>카카오뱅크 신용대출 금리 알려줘</question>
<expected_behavior>
- 카카오뱅크 신용대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "주식회사 카카오뱅크",
  "product_name": "일반신용대출",
  "loan_type": "일반신용대출",
  "credit_score_band": "601~700점",
  "interest_rate": 7.93
 },
 {
  "bank_name": "주식회사 카카오뱅크",
  "product_name": "마이너스한도대출",
  "loan_type": "마이너스한도대출",
  "credit_score_band": "601~700점",
  "interest_rate": 8.65
 }
]
</source_data>
<answer>
카카오뱅크의 신용대출 금리는 신용점수 601~700점 기준으로 일반신용대출은 연 7.93%, 마이너스한도대출은 연 8.65%입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C012">
<history>
(없음)
</history>
<question>신한은행에서 신용점수 750점으로 신용대출 받으면 금리 얼마야?</question>
<expected_behavior>
- 신한은행 750점 기준 금리를 안내하거나, 조회되지 않으면 그렇다고 밝힌다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "신한은행",
  "product_name": "개인신용대출(마이너스한도대출)",
  "loan_type": "마이너스한도대출",
  "credit_score_band": "701~800점",
  "interest_rate": 6.52
 },
 {
  "bank_name": "신한은행",
  "product_name": "개인신용대출(일반신용대출)",
  "loan_type": "일반신용대출",
  "credit_score_band": "701~800점",
  "interest_rate": 7.36
 }
]
</source_data>
<answer>
신한은행에서 신용점수 750점으로 신용대출을 받으실 경우,  
- 마이너스한도대출(마통)은 금리가 6.52%이고,  
- 일반신용대출은 금리가 7.36%입니다.  

두 상품 모두 신용점수 701~800점 구간에 해당하는 금리입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C013">
<history>
(없음)
</history>
<question>직장인 신용대출 금리 비교해줘</question>
<expected_behavior>
- 신용대출 상품을 금리와 함께 비교해 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "농협은행주식회사",
  "product_name": "가계신용대출(마이너스대출)",
  "loan_type": "마이너스한도대출",
  "credit_score_band": "601~700점",
  "interest_rate": 5.72
 },
 {
  "bank_name": "주식회사 하나은행",
  "product_name": "마이너스한도대출",
  "loan_type": "마이너스한도대출",
  "credit_score_band": "601~700점",
  "interest_rate": 6.12
 },
 {
  "bank_name": "우리은행",
  "product_name": "협약금리 外 신용대출상품",
  "loan_type": "마이너스한도대출",
  "credit_score_band": "601~700점",
  "interest_rate": 6.22
 }
]
</source_data>
<answer>
직장인 신용대출 금리를 비교해드리면, 신용점수 601~700점 기준으로

- 농협은행의 '가계신용대출(마이너스대출)'은 금리가 5.72%
- 하나은행의 '마이너스한도대출'은 금리가 6.12%
- 우리은행의 '협약금리 외 신용대출상품'은 금리가 6.22%

입니다. 각 은행별로 금리 차이가 있으니 참고하시기 바랍니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C014">
<history>
(없음)
</history>
<question>마이너스통장 금리 낮은 은행 어디야?</question>
<expected_behavior>
- 마이너스통장(한도대출) 금리를 안내하거나, 해당 상품이 조회되지 않으면 그렇다고 밝힌다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C015">
<history>
(없음)
</history>
<question>전세자금대출 금리 낮은 데 알려줘</question>
<expected_behavior>
- 전세자금대출 상품을 금리와 함께 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(서울보증보험)",
  "lend_rate_min": 3.69,
  "lend_rate_max": 6.39
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(주택금융공사)",
  "lend_rate_min": 3.69,
  "lend_rate_max": 6.39
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(주택도시보증공사)",
  "lend_rate_min": 3.7,
  "lend_rate_max": 6.4
 }
]
</source_data>
<answer>
참고로, 'NH전세대출(주택도시보증공사)' 상품의 최저 금리는 3.7%입니다.
</answer>
</case>

<case id="C016">
<history>
(없음)
</history>
<question>국민은행 전세대출 금리 알려줘</question>
<expected_behavior>
- 국민은행 전세자금대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "국민은행",
  "product_name": "KB주택전세자금대출",
  "lend_rate_min": 4.21,
  "lend_rate_max": 5.61
 },
 {
  "bank_name": "국민은행",
  "product_name": "KB플러스전세자금대출",
  "lend_rate_min": 4.22,
  "lend_rate_max": 5.62
 }
]
</source_data>
<answer>
국민은행의 전세대출 금리는 다음과 같습니다.

- KB주택전세자금대출: 연 4.21% ~ 5.61%
- KB플러스전세자금대출: 연 4.22% ~ 5.62%

금리는 신청 조건이나 신용도 등에 따라 달라질 수 있으니 참고하시기 바랍니다.
</answer>
</case>

<case id="C017">
<history>
(없음)
</history>
<question>우리은행 전세자금대출 상품 있어?</question>
<expected_behavior>
- 우리은행 전세자금대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "우리은행",
  "product_name": "우리전세론(서울보증)",
  "lend_rate_min": 3.89,
  "lend_rate_max": 4.59
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리전세론(주택금융보증)",
  "lend_rate_min": 3.93,
  "lend_rate_max": 4.63
 }
]
</source_data>
<answer>
네, 우리은행에는 전세자금대출 상품이 있습니다.  
예를 들어, '우리전세론(서울보증)' 상품은 금리가 연 3.89%에서 4.59% 사이이고,  
'우리전세론(주택금융보증)' 상품은 연 3.93%에서 4.63% 사이의 금리로 제공되고 있습니다.
</answer>
</case>

<case id="C018">
<history>
(없음)
</history>
<question>전세 들어가려는데 대출 금리 어느 정도야?</question>
<expected_behavior>
- 전세자금대출 금리를 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(서울보증보험)",
  "lend_rate_min": 3.69,
  "lend_rate_max": 6.39
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(주택금융공사)",
  "lend_rate_min": 3.69,
  "lend_rate_max": 6.39
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(주택도시보증공사)",
  "lend_rate_min": 3.7,
  "lend_rate_max": 6.4
 }
]
</source_data>
<answer>
현재 조회된 전세대출 상품의 금리는 다음과 같습니다.

- NH전세대출(서울보증보험): 연 3.69% ~ 6.39%
- NH전세대출(주택금융공사): 연 3.69% ~ 6.39%
- NH전세대출(주택도시보증공사): 연 3.7% ~ 6.4%

따라서 전세대출 금리는 대략 연 3.69%에서 6.4% 사이로 확인됩니다. 실제 적용 금리는 신용도, 대출 조건 등에 따라 달라질 수 있으니 참고하시기 바랍니다.
</answer>
</case>

<case id="C019">
<history>
(없음)
</history>
<question>전세대출 제일 싼 곳 하나만 딱 찍어줘</question>
<expected_behavior>
- 금리 수치를 근거로 안내한다
- '무조건 최고' 같은 단정 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(서울보증보험)",
  "lend_rate_min": 3.69,
  "lend_rate_max": 6.39
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(주택금융공사)",
  "lend_rate_min": 3.69,
  "lend_rate_max": 6.39
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(주택도시보증공사)",
  "lend_rate_min": 3.7,
  "lend_rate_max": 6.4
 }
]
</source_data>
<answer>
두 상품 모두 최저 금리가 3.69%로 가장 저렴합니다.
</answer>
</case>

<case id="C020">
<history>
(없음)
</history>
<question>농협 전세대출 금리 보여줘</question>
<expected_behavior>
- 농협 전세자금대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(서울보증보험)",
  "lend_rate_min": 3.69,
  "lend_rate_max": 6.39
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(주택금융공사)",
  "lend_rate_min": 3.69,
  "lend_rate_max": 6.39
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH전세대출(주택도시보증공사)",
  "lend_rate_min": 3.7,
  "lend_rate_max": 6.4
 }
]
</source_data>
<answer>
농협은행의 전세대출 금리는 다음과 같습니다.

- NH전세대출(서울보증보험): 연 3.69% ~ 6.39%
- NH전세대출(주택금융공사): 연 3.69% ~ 6.39%
- NH전세대출(주택도시보증공사): 연 3.7% ~ 6.4%

각 상품별로 금리 범위가 다소 차이가 있으니 참고하시기 바랍니다.
</answer>
</case>
