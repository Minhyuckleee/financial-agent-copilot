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

<case id="C061">
<history>
(없음)
</history>
<question>오늘 서울 날씨 어때?</question>
<expected_behavior>
- 도울 수 있는 범위가 아니라고 안내한다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C062">
<history>
(없음)
</history>
<question>삼성전자 주가 앞으로 오를까?</question>
<expected_behavior>
- 주가를 예측하지 않는다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C063">
<history>
(없음)
</history>
<question>비트코인 지금 사도 돼?</question>
<expected_behavior>
- 투자 판단이나 매수 권유를 하지 않는다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C064">
<history>
(없음)
</history>
<question>파이썬으로 리스트 정렬하는 코드 짜줘</question>
<expected_behavior>
- 도울 수 있는 범위가 아니라고 안내한다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C065">
<history>
(없음)
</history>
<question>이번 휴가 때 갈 만한 여행지 추천해줘</question>
<expected_behavior>
- 도울 수 있는 범위가 아니라고 안내한다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C066">
<history>
사용자: 정기예금 추천해줘
에이전트: 12개월 기준 정기예금 상품 3건을 안내드립니다.
</history>
<question>24개월로도 보여줘</question>
<expected_behavior>
- 24개월 기준으로 다시 안내한다
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
24개월 예금 상품은 다음과 같습니다.

1. 부산은행 '더(The) 특판 정기예금': 기본금리 1.75%, 우대금리 포함 시 3.92%
2. 전북은행 'JB 다이렉트(자유만기) 예금': 기본금리 3.82%, 우대금리 포함 시 3.82%
3. 농협은행주식회사 'NH올원e예금': 기본금리 3.0%, 우대금리 포함 시 3.0%

각 상품의 금리와 조건을 참고해보세요.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C067">
<history>
사용자: 신용대출 금리 낮은 곳 알려줘
에이전트: 신용점수 700점 기준 신용대출 상품 3건을 안내드립니다.
</history>
<question>신용점수 850점이면 어떻게 돼?</question>
<expected_behavior>
- 850점 기준으로 다시 안내한다
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
신용점수가 850점이면, 수협은행의 개인신용대출(일반신용대출), 아이엠뱅크의 장기카드대출(카드론), 농협은행의 가계신용대출(마이너스대출) 등에서 모두 801~900점 구간에 해당합니다. 이 구간의 대출 금리는 각각 다음과 같습니다:

- 수협은행 개인신용대출: 연 5.19%
- 아이엠뱅크 장기카드대출: 연 5.19%
- 농협은행 가계신용대출(마이너스대출): 연 5.7%

즉, 신용점수 850점이면 위와 같은 금리로 대출을 받을 수 있습니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C068">
<history>
사용자: 달러 환율 알려줘
에이전트: 현재 USD/KRW 환율은 1,390원입니다.
</history>
<question>한 번 더 조회해줄래?</question>
<expected_behavior>
- 환율을 다시 조회해 기준일과 함께 안내한다
</expected_behavior>
<source_data>
[조회 결과 1]
{
 "currency_pair": "USD/KRW",
 "rate": 1381.0,
 "base_date": "20260921"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</answer>
</case>

<case id="C069">
<history>
사용자: 전세자금대출 금리 낮은 곳 알려줘
에이전트: 전세자금대출 상품 3건을 안내드립니다.
</history>
<question>그중에 국민은행 것만 보여줘</question>
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
국민은행의 전세자금대출 상품은 다음과 같습니다.

1. KB주택전세자금대출: 금리는 연 4.22%에서 5.61%입니다.
2. KB플러스전세자금대출: 금리는 연 4.22%에서 5.62%입니다.
</answer>
</case>

<case id="C070">
<history>
사용자: 예금거래기본약관은 고객이 볼 수 있어?
에이전트: 네, 영업점에서 영업시간 중 볼 수 있습니다.
</history>
<question>교부도 요청할 수 있어?</question>
<expected_behavior>
- 약관 교부 청구 가능 여부를 약관 근거로 안내한다
- 문서에 없는 조항 번호·기한·수치를 지어내지 않는다
</expected_behavior>
<source_data>
[문서 1] 예금거래기본약관.txt
## Page 1 *이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 1 - 예금거래기본약관 이 예금거래기본약관(이하 “약관”이라 한다)은 우리은행(이하 “은행”이라 한다)과 거래처 (또는 예금주)가 서로 믿음을 바탕으로 예금거래를 빠르고 틀림 없이 처리하는 한편, 서 로의 이해관계를 합리적으로 조정하기 위하여 기본적이고 일반적인 사항을 정한 것이다. 은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수 있고 또한 그 교부를 청구할 수 있다.

[문서 2] 예금거래기본약관.txt
Page 1  
*이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 1 -
예금거래기본약관
이 예금거래기본약관(이하 “약관”이라 한다)은 우리은행(이하 “은행”이라 한다)과 거래처
(또는 예금주)가 서로 믿음을 바탕으로 예금거래를 빠르고 틀림 없이 처리하는 한편, 서
로의 이해관계를 합리적으로 조정하기 위하여 기본적이고 일반적인 사항을 정한 것이다.
은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수
있고 또한 그 교부를 청구할 수 있다.
============================================================
[섹션 전환: 0 → 1]
============================================================
## 제1조(적용범위)
이 약관은 입출금이 자유로운 예금, 거치식예금 및 적립식예금 거래에 적용한다.

[문서 3] NH농협은행_전자금융서비스이용약관.txt
## 제1조(목적)
니다)이 「전자금융거래기본약관」의 기본취지를 바탕으로 농협이 제공하는
인터넷뱅킹, 텔레뱅킹, 모바일뱅킹, 스마트뱅킹 등 농협 전자금융서비스를 이
용하는 이용자 사이의 서비스 이용에 관한 제반사항을 정함을 목적으로 합니
다.
============================================================
[섹션 전환: 1 → 2]
============================================================
## 제2조(용어의 정의)
1. “서비스”란 인터넷뱅킹, 텔레뱅킹, 모바일뱅킹, 스마트뱅킹 등 농협이 신
용사업 중 일부를 「전자금융거래법」에 따른 금융회사로서 수행하는 전자
금융거래 서비스를 말합니다.
2. “이용자”란 이 약관에 의하여 농협과 체결한 계약에 따라 농협이 제공하
는 서비스를 이용하는 고객을 말합니다.
3. “생체인증”이란 이용자가 소유한 본인의 전자적 장치에 미리 저장해 둔
본인의 지문, 홍채, 얼굴 등 생체정보를 이용하여 서비스를 이용할 때에 사
용할 수 있는 본인확인 인증수단을 말합니다.
4. “간편뱅킹 서비스

[문서 4] 예금거래기본약관.txt
## 제10조(지급․해지청구)
① 거래처가 예금․이자를 찾거나 예금계약을 해지하고자 할 때에는 신고한 비밀번호 등
필요사항을 기재하거나 PIN-Pad기에 입력하고, 거래인감을 날인하거나 서명감과 일
치되게 서명한 지급 또는 해지청구서를 제출하여야 한다.
② 거래처가 무통장으로 거래하고 실명확인증표 등에 의해 본인확인된 경우, 은행이 정
하는 바에 따라 제①항에 따른 절차의 전부 또는 일부를 생략할 수 있다.
③ 거래처가 자동이체․전산통신기기․바이오정보 등을 이용하여 찾을 때는 그 약정에서
정한 바에 따른다.
============================================================
[섹션 전환: 13 → 14]
============================================================
## Page 4  
*이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 4 -
</source_data>
<answer>
네, 문서에 따르면 예금거래기본약관의 교부를 고객이 요청할 수 있습니다.  
문서의 내용 중  
> "은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수 있고 또한 그 교부를 청구할 수 있다."  
라고 명시되어 있습니다.  
따라서 고객(거래처)은 영업시간 중 언제든지 약관의 교부를 요청할 수 있습니다.
</answer>
</case>
