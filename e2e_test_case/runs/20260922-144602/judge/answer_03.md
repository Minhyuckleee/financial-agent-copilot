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

<case id="C021">
<history>
(없음)
</history>
<question>주택담보대출 금리 낮은 곳 추천해줘</question>
<expected_behavior>
- 주택담보대출 상품을 금리와 함께 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "경남은행",
  "product_name": "집집마다 도움대출II",
  "lend_rate_min": 3.7,
  "lend_rate_max": 5.51
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리아파트론",
  "lend_rate_min": 4.18,
  "lend_rate_max": 5.28
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH주택담보대출",
  "lend_rate_min": 4.49,
  "lend_rate_max": 6.29
 }
]
</source_data>
<answer>
현재 조회된 주택담보대출 상품 중에서 금리가 가장 낮은 곳은 경남은행의 '집집마다 도움대출II'로, 최저 금리가 3.7%입니다. 그 다음으로는 우리은행의 '우리아파트론'(최저 4.18%), 농협은행의 'NH주택담보대출'(최저 4.49%) 순입니다.
</answer>
</case>

<case id="C022">
<history>
(없음)
</history>
<question>신한은행 주담대 금리 알려줘</question>
<expected_behavior>
- 신한은행 주택담보대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "신한은행",
  "product_name": "신한주택대출(아파트)",
  "lend_rate_min": 4.29,
  "lend_rate_max": 5.69
 },
 {
  "bank_name": "신한은행",
  "product_name": "신한주택대출",
  "lend_rate_min": 4.39,
  "lend_rate_max": 5.79
 }
]
</source_data>
<answer>
신한은행의 주택담보대출(주담대) 금리는 상품에 따라 다르며, 현재 조회된 결과에 따르면 다음과 같습니다.

- 신한주택대출(아파트): 연 4.39% ~ 5.69%
- 신한주택대출: 연 4.39% ~ 5.79%

실제 적용 금리는 대출 조건이나 신용도 등에 따라 달라질 수 있으니 참고하시기 바랍니다.
</answer>
</case>

<case id="C023">
<history>
(없음)
</history>
<question>하나은행 주택담보대출 상품 있어?</question>
<expected_behavior>
- 하나은행 주택담보대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "주식회사 하나은행",
  "product_name": "하나원큐아파트론2",
  "lend_rate_min": 4.5,
  "lend_rate_max": 5.7
 }
]
</source_data>
<answer>
네, 하나은행에는 "하나원큐아파트론2"라는 주택담보대출 상품이 있습니다. 이 상품의 대출 금리는 연 4.5%에서 5.7% 사이입니다.
</answer>
</case>

<case id="C024">
<history>
(없음)
</history>
<question>집 사려고 하는데 대출 금리 어디가 괜찮아?</question>
<expected_behavior>
- 주택담보대출 금리를 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "경남은행",
  "product_name": "집집마다 도움대출II",
  "lend_rate_min": 3.7,
  "lend_rate_max": 5.51
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리아파트론",
  "lend_rate_min": 4.18,
  "lend_rate_max": 5.28
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH주택담보대출",
  "lend_rate_min": 4.49,
  "lend_rate_max": 6.29
 }
]
</source_data>
<answer>
현재 조회된 주택담보대출 금리를 보면,  
- 경남은행의 '집집마다 도움대출II'가 연 3.7%~5.51%  
- 우리은행의 '우리아파트론'이 연 4.18%~5.28%  
- 농협은행의 'NH주택담보대출'이 연 4.49%~6.29%입니다.

이 중에서는 경남은행의 최저 금리(3.7%)가 가장 낮고, 우리은행은 최대 금리가 상대적으로 낮은 편(5.28%)입니다. 본인의 조건(신용도, 대출기간 등)에 따라 실제 적용 금리는 달라질 수 있으니, 여러 은행에 상담을 받아보시고 비교해보시는 것이 좋겠습니다.
</answer>
</case>

<case id="C025">
<history>
(없음)
</history>
<question>주담대 금리 은행별로 비교해줘</question>
<expected_behavior>
- 여러 은행의 주택담보대출 금리를 비교해 안내한다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "경남은행",
  "product_name": "집집마다 도움대출II",
  "lend_rate_min": 3.7,
  "lend_rate_max": 5.51
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리아파트론",
  "lend_rate_min": 4.18,
  "lend_rate_max": 5.28
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH주택담보대출",
  "lend_rate_min": 4.49,
  "lend_rate_max": 6.29
 }
]
</source_data>
<answer>
현재 조회된 주택담보대출(주담대) 금리를 은행별로 비교해드리면 다음과 같습니다.

- 경남은행의 '집집마다 도움대출II' 상품은 금리가 연 3.7%에서 5.51% 사이입니다.
- 우리은행의 '우리아파트론' 상품은 연 4.18%에서 5.28% 사이입니다.
- 농협은행의 'NH주택담보대출' 상품은 연 4.49%에서 6.29% 사이입니다.

각 은행별로 최저 금리와 최고 금리가 다르니, 본인의 조건에 맞는 상품을 선택하시는 것이 좋겠습니다.
</answer>
</case>

<case id="C026">
<history>
(없음)
</history>
<question>기업은행 주택담보대출 금리 얼마야?</question>
<expected_behavior>
- 기업은행 주택담보대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "중소기업은행",
  "product_name": "IBK주택담보대출",
  "lend_rate_min": 4.89,
  "lend_rate_max": 4.89
 }
]
</source_data>
<answer>
기업은행(중소기업은행)의 주택담보대출(IBK주택담보대출) 금리는 4.89%입니다.
</answer>
</case>

<case id="C027">
<history>
(없음)
</history>
<question>개인사업자대출 금리 낮은 곳 알려줘</question>
<expected_behavior>
- 개인사업자대출 상품을 금리와 함께 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "제주은행",
  "product_name": "JJB가맹점우대론",
  "credit_score_band": "601~700점",
  "interest_rate": 4.46
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리상생파트너론",
  "credit_score_band": "601~700점",
  "interest_rate": 4.85
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리CUBE론-X(일반,산업단지)",
  "credit_score_band": "601~700점",
  "interest_rate": 4.95
 }
]
</source_data>
<answer>
그 다음으로는 우리은행의 '우리상생파트너론'(4.95%), '우리CUBE론-X(일반,산업단지)'(4.95%)가 있습니다.
</answer>
</case>

<case id="C028">
<history>
(없음)
</history>
<question>신용점수 800점 개인사업자인데 대출 금리 어디가 낮아?</question>
<expected_behavior>
- 신용점수 800점 기준 개인사업자대출을 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "우리은행",
  "product_name": "B2B 대출",
  "credit_score_band": "701~800점",
  "interest_rate": 4.85
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리 지역선도기업 대출",
  "credit_score_band": "701~800점",
  "interest_rate": 4.85
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리 첨단선도기업대출",
  "credit_score_band": "701~800점",
  "interest_rate": 4.86
 }
]
</source_data>
<answer>
조회 결과에 따르면, 신용점수 800점인 개인사업자에게 적용되는 대출 금리는 우리은행의 B2B 대출과 우리 지역선도기업 대출이 각각 연 4.86%로 가장 낮습니다. 우리 첨단선도기업대출은 연 4.86%입니다.
</answer>
</case>

<case id="C029">
<history>
(없음)
</history>
<question>국민은행 개인사업자대출 상품 있어?</question>
<expected_behavior>
- 국민은행 개인사업자대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
국민은행의 개인사업자대출 상품은 현재 조회 결과가 없습니다.

※ 이 조건으로는 충분히 찾지 못해, 확인된 정보만 안내드립니다.
</answer>
</case>

<case id="C030">
<history>
(없음)
</history>
<question>자영업자 대출 금리 비교해줘</question>
<expected_behavior>
- 개인사업자대출 금리를 비교해 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "제주은행",
  "product_name": "JJB가맹점우대론",
  "credit_score_band": "601~700점",
  "interest_rate": 4.46
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리상생파트너론",
  "credit_score_band": "601~700점",
  "interest_rate": 4.85
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리CUBE론-X(일반,산업단지)",
  "credit_score_band": "601~700점",
  "interest_rate": 4.95
 }
]
</source_data>
<answer>
현재 601~700점 신용점수 구간에서 자영업자 대출 금리는 다음과 같이 비교할 수 있습니다.
</answer>
</case>
