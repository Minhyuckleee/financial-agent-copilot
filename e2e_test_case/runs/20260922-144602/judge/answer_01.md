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

<case id="C001">
<history>
(없음)
</history>
<question>정기예금 금리 좋은 거 추천해줘</question>
<expected_behavior>
- 정기예금 상품을 금리와 함께 안내한다
- 어느 가입기간 기준인지 밝힌다
- 원금보장·확정수익 같은 단정 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "광주은행",
  "product_name": "굿스타트예금",
  "save_term_months": 12,
  "interest_rate": 3.45,
  "interest_rate_preferential": 3.95
 },
 {
  "bank_name": "부산은행",
  "product_name": "더(The) 특판 정기예금",
  "save_term_months": 12,
  "interest_rate": 2.1,
  "interest_rate_preferential": 3.92
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH왈츠회전예금 II",
  "save_term_months": 12,
  "interest_rate": 3.35,
  "interest_rate_preferential": 3.45
 }
]
</source_data>
<answer>
그 외에도 부산은행의 '더(The) 특판 정기예금'이 최대 3.92%, 농협은행의 'NH왈츠회전예금 II'가 최대 3.45%의 금리를 제공하고 있습니다. 금리와 조건을 비교해보시고 선택하시면 좋을 것 같습니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C002">
<history>
(없음)
</history>
<question>6개월짜리 정기예금 보여줘</question>
<expected_behavior>
- 6개월 기준 정기예금을 안내한다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "부산은행",
  "product_name": "더(The) 레벨업 정기예금",
  "save_term_months": 6,
  "interest_rate": 2.5,
  "interest_rate_preferential": 3.72
 },
 {
  "bank_name": "수협은행",
  "product_name": "Sh해양플라스틱Zero!예금\n(만기일시지급식)",
  "save_term_months": 6,
  "interest_rate": 3.2,
  "interest_rate_preferential": 3.55
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH왈츠회전예금 II",
  "save_term_months": 6,
  "interest_rate": 3.15,
  "interest_rate_preferential": 3.25
 }
]
</source_data>
<answer>
6개월짜리 정기예금 상품은 다음과 같습니다.

1. 부산은행 - 더(The) 레벨업 정기예금  
   - 기본 금리: 연 2.5%  
   - 우대 금리 포함: 연 3.72%

2. 수협은행 - Sh해양플라스틱Zero!예금(만기일시지급식)  
   - 기본 금리: 연 3.2%  
   - 우대 금리 포함: 연 3.55%

3. 농협은행주식회사 - NH왈츠회전예금 II  
   - 기본 금리: 연 3.15%  
   - 우대 금리 포함: 연 3.25%

각 상품의 금리와 조건을 참고해보시기 바랍니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C003">
<history>
(없음)
</history>
<question>2년짜리 예금 금리 높은 곳 알려줘</question>
<expected_behavior>
- 24개월 기준 정기예금을 안내한다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "부산은행",
  "product_name": "더(The) 특판 정기예금",
  "save_term_months": 24,
  "interest_rate": 1.75,
  "interest_rate_preferential": 3.92
 },
 {
  "bank_name": "전북은행",
  "product_name": "JB 다이렉트(자유만기) 예금",
  "save_term_months": 24,
  "interest_rate": 3.82,
  "interest_rate_preferential": 3.82
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH올원e예금",
  "save_term_months": 24,
  "interest_rate": 3.0,
  "interest_rate_preferential": 3.0
 }
]
</source_data>
<answer>
2년(24개월)짜리 예금 상품 중 금리가 높은 곳은 다음과 같습니다.

- 부산은행의 '더(The) 특판 정기예금': 최고 연 3.92% (우대금리 포함)
- 전북은행의 'JB 다이렉트(자유만기) 예금': 연 3.82%
- 농협은행의 'NH올원e예금': 연 3.0%

이 중 부산은행의 '더(The) 특판 정기예금'이 우대금리 적용 시 가장 높은 금리(3.92%)를 제공합니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C004">
<history>
(없음)
</history>
<question>우리은행 정기예금 상품 뭐 있어?</question>
<expected_behavior>
- 우리은행 정기예금을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "우리은행",
  "product_name": "WON플러스예금",
  "save_term_months": 12,
  "interest_rate": 3.5,
  "interest_rate_preferential": 3.5
 }
]
</source_data>
<answer>
우리은행의 정기예금 상품으로는 "WON플러스예금"이 있습니다. 가입 기간은 12개월이고, 금리는 연 3.5%입니다. (우대금리 포함 시에도 3.5%입니다.)

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C005">
<history>
(없음)
</history>
<question>하나은행 3년 정기예금 금리 알려줘</question>
<expected_behavior>
- 하나은행 36개월 정기예금을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "주식회사 하나은행",
  "product_name": "하나의정기예금",
  "save_term_months": 36,
  "interest_rate": 2.3,
  "interest_rate_preferential": 2.7
 }
]
</source_data>
<answer>
하나은행의 3년(36개월) 정기예금 금리는 기본 연 2.3%이고, 우대금리 적용 시 최대 연 2.7%입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C006">
<history>
(없음)
</history>
<question>목돈 맡기려는데 이자 많이 주는 예금 어디야?</question>
<expected_behavior>
- 정기예금 상품을 금리와 함께 안내한다
- 원금보장·확정수익 같은 단정 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "광주은행",
  "product_name": "굿스타트예금",
  "save_term_months": 12,
  "interest_rate": 3.45,
  "interest_rate_preferential": 3.95
 },
 {
  "bank_name": "부산은행",
  "product_name": "더(The) 특판 정기예금",
  "save_term_months": 12,
  "interest_rate": 2.1,
  "interest_rate_preferential": 3.92
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH왈츠회전예금 II",
  "save_term_months": 12,
  "interest_rate": 3.35,
  "interest_rate_preferential": 3.45
 }
]
</source_data>
<answer>
현재 1년(12개월) 기준으로 이자를 많이 주는 예금 상품은 다음과 같습니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C007">
<history>
(없음)
</history>
<question>1년 만기 예금 중에 우대금리 높은 거 알려줘</question>
<expected_behavior>
- 12개월 기준 정기예금을 우대금리와 함께 안내한다
- 원금보장·확정수익 같은 단정 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "광주은행",
  "product_name": "굿스타트예금",
  "save_term_months": 12,
  "interest_rate": 3.45,
  "interest_rate_preferential": 3.95
 },
 {
  "bank_name": "부산은행",
  "product_name": "더(The) 특판 정기예금",
  "save_term_months": 12,
  "interest_rate": 2.1,
  "interest_rate_preferential": 3.92
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH왈츠회전예금 II",
  "save_term_months": 12,
  "interest_rate": 3.35,
  "interest_rate_preferential": 3.45
 }
]
</source_data>
<answer>
그 다음으로는 부산은행의 '더(The) 특판 정기예금'이 3.92%, 농협은행의 'NH왈츠회전예금 II'가 3.45%의 우대금리를 제공합니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C008">
<history>
(없음)
</history>
<question>신용대출 금리 낮은 곳 추천해줘</question>
<expected_behavior>
- 신용대출 상품을 금리와 함께 안내한다
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
현재 조회된 결과 중 신용점수 601~700점 기준으로 신용대출 금리가 가장 낮은 곳은 농협은행주식회사의 '가계신용대출(마이너스대출)'로, 금리는 5.72%입니다.  
다음으로 하나은행(6.12%), 우리은행(6.22%) 순으로 금리가 높으니 참고하시면 좋겠습니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C009">
<history>
(없음)
</history>
<question>신용점수 900점이면 신용대출 어디가 싸?</question>
<expected_behavior>
- 신용점수 900점 기준 상품을 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "수협은행",
  "product_name": "개인신용대출",
  "loan_type": "일반신용대출",
  "credit_score_band": "801~900점",
  "interest_rate": 5.18
 },
 {
  "bank_name": "아이엠뱅크",
  "product_name": "장기카드대출",
  "loan_type": "장기카드대출(카드론)",
  "credit_score_band": "801~900점",
  "interest_rate": 5.19
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "가계신용대출(마이너스대출)",
  "loan_type": "마이너스한도대출",
  "credit_score_band": "801~900점",
  "interest_rate": 5.7
 }
]
</source_data>
<answer>
신용점수가 900점일 경우, 조회 결과 기준으로 가장 낮은 금리의 신용대출 상품은 수협은행의 '개인신용대출'(일반신용대출)로, 금리는 5.18%입니다. 그 다음으로는 아이엠뱅크의 '장기카드대출'(카드론)이 5.19%, 농협은행의 '가계신용대출(마이너스대출)'이 5.7%입니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C010">
<history>
(없음)
</history>
<question>신용점수 600점대 초반인데 받을 수 있는 신용대출 금리 알려줘</question>
<expected_behavior>
- 점수 조건에 맞는 금리를 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "우리은행",
  "product_name": "협약금리 外 신용대출상품",
  "loan_type": "일반신용대출",
  "credit_score_band": "501~600점",
  "interest_rate": 7.25
 },
 {
  "bank_name": "신한은행",
  "product_name": "개인신용대출(일반신용대출)",
  "loan_type": "일반신용대출",
  "credit_score_band": "501~600점",
  "interest_rate": 7.45
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "가계신용대출(일반)",
  "loan_type": "일반신용대출",
  "credit_score_band": "501~600점",
  "interest_rate": 8.1
 }
]
</source_data>
<answer>
신용점수가 600점대 초반이라면, 받을 수 있는 신용대출 금리는 다음과 같습니다.

- 우리은행: 연 7.25%
- 신한은행: 연 7.45%
- 농협은행: 연 8.1%

위 금리는 모두 신용점수 501~600점 구간에 해당하는 일반신용대출 상품 기준입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>
