You are an expert data labeler.
Your task is to grade the accuracy of an AI agent's internal trajectory.

<Rubric>
  An accurate trajectory:
  - Makes logical sense between steps
  - Shows clear progression
  - Is relatively efficient, though it does not need to be perfectly efficient
  - A single retry or reinterpretation after an API failure or empty result is expected, not inefficient
</Rubric>

First, try to understand the goal of the trajectory by looking at the input
(if the input is not present try to infer it from the content of the first message),
as well as the output of the final message. Once you understand the goal, grade the trajectory
as it relates to achieving that goal.

Grade the following trajectory:

<trajectory>
{outputs}
</trajectory>

Write the key observations that decide the grade as short lines in <evidence> tags,
then output PASS or FAIL in <result> tags.


아래 케이스마다 위 기준으로 판정하라. 케이스마다 <case id=...> 로 감싸서 답하라.

<case id="C056">
<trajectory>
input: 금융소비자보호법에서 설명의무는 몇 조에 있어?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "금융소비자보호법에서 설명의무에 관한 규정이 명시된 조문 번호를 알려주세요.", "retrieved": [{"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 금융소비자보호법에서 설명의무에 관한 규정이 명시된 조문 번호는 **제19조**입니다.
</trajectory>
</case>

<case id="C057">
<trajectory>
input: 고객 주민등록번호 수집해도 되는 경우가 언제야?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "고객의 주민등록번호를 수집할 수 있는 정당한 사유와 법적 근거가 인정되는 경우는 언제인지에 관한 규정을 확인하고자 합니다.", "retrieved": [{"source": "개인정보 질의응답 모음집.txt", "score": null}, {"source": "개인정보 보호 법령 및 지침, 고시 해설서(2020.12).txt", "score": null}, {"source": "개인정보 처리 통합 안내서(2025.7.).txt", "score": null}, {"source": "개인정보 처리방침 작성지침(2025.4.).txt", "score": null}, {"source": "개인정보 처리방침 작성지침(2025.4.).txt", "score": null}, {"source": "개인정보 처리방침 작성지침(2025.4.).txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에 따르면, 고객의 주민등록번호를 수집할 수 있는 정당한 사유와 법적 근거는 다음과 같이 규정되어 있습니다.

### 1. 법적 근거(주민등록번호 처리의 허용 요건)
- **법률·대통령령·국회규칙·대법원규칙·헌법재판소규칙·중앙선거관리위원회규칙 및 감사원 규칙**에서 구체적으로 주민등록번호의 처리를 요구하거나 허용한 경우  
  (예: 유실물법 시행령에서 습득물 신고서에 주민등록번호 기재를 요구하는 경우 등)

- **정보주체 또는 제3자의 급박한 생명, 신체, 재산의 이익을 위하여 명백히 필요하다고 인정되는 경우**

- **주민등록번호 처리가 불가피한 경우로서 개인정보보호위원회가 고시로 정하는 경우**

### 2. 동의 요건
- 위와 같은 예외사유에 해당하는 경우에는 정보주체의 동의를 별도로 받지 않아도 주민등록번호를 처리할 수 있습니다.
- 다만, 어떤 법적 근거에 따라 주민등록번호를 처리하는지 정보주체에게 알리는 것이 바람직합니다.

### 3. 예시
- **법령에 근거한 경우**:  
  예를 들어, 경찰서에 습득물을 제출할 때 습득물 신고서에 주민등록번호를 기재하도록 한 경우(유실물법 시행령).
- **실명확인 등 법령에서 구체적으로 요구하는 경우**:  
  전자금융거래법에 따라 접근매체 발급을 위한 실명확인 시 신분증 진위확인에 주민등록번호 처리가 포함되는 경우 등.

### 4. 처리 목적의 최소화
- 주민등록번호 등 고유식별정보는 반드시 필요한 최소한의 범위 내에서만 수집·이용해야 하며, 그 필요성에 대한 입증 책임은 개인정보처리자에게 있습니다.

### 5. 안전조치
- 주민등록번호를 전자적으로 보관하는 경우에는 암호화 등 안전성 확보 조치를 반드시 해야 합니다.

---

**요약**  
고객의 주민등록번호를 수집할 수 있는 정당한 사유와 법적 근거는  
- 법률 등에서 구체적으로 요구하거나 허용한 경우,  
- 급박한 생명·신체·재산의 이익을 위해 명백히 필요한 경우,  
- 개인정보보호위원회 고시로 정한 불가피한 경우  
에 한정되며, 이 경우 별도의 동의 없이도 수집이 가능합니다.  
그 외에는 원칙적으로 동의를 받아야 하며, 반드시 최소한의 범위 내에서만 처리해야 합니다.
</trajectory>
</case>

<case id="C058">
<trajectory>
input: 개인정보보호법에서 말하는 개인정보의 정의가 뭐야?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "개인정보보호법에서 규정하는 개인정보의 정의에 대해 설명한 조항을 제시해 주세요.", "retrieved": [{"source": "개인정보 질의응답 모음집.txt", "score": null}, {"source": "개인정보 보호 법령 및 지침, 고시 해설서(2020.12).txt", "score": null}, {"source": "개인정보 처리 통합 안내서(2025.7.).txt", "score": null}, {"source": "개인정보 질의응답 모음집.txt", "score": null}, {"source": "(전 분야 마이데이터) 개인정보 전송요구권 제도 안내서(2025.4.).txt", "score": null}, {"source": "개인정보 처리 통합 안내서(2025.7.).txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에 따르면, 개인정보보호법에서 규정하는 개인정보의 정의는 다음과 같습니다.

---

### 제2조(정의)

이 법에서 사용하는 용어의 뜻은 다음과 같다.

1. “개인정보”란 살아 있는 개인에 관한 정보로서 다음 각 목의 어느 하나에 해당하는 정보를 말한다.
   - 가. 성명, 주민등록번호 및 영상 등을 통하여 개인을 알아볼 수 있는 정보나, 해당 정보만으로는 특정 개인을 알아볼 수 없더라도 다른 정보와 쉽게 결합하여 알아볼 수 있는 정보. 이 경우 쉽게 결합할 수 있는지 여부는 다른 정보의 입수 가능성 등 개인을 알아보는 데 소요되는 시간, 비용, 기술 등을 합리적으로 고려하여야 한다.
   - 다. 가목 또는 나목을 제1호의2에 따라 가명처리함으로써 원래의 상태로 복원하기 위한 추가 정보의 사용·결합 없이는 특정 개인을 알아볼 수 없는 정보(이하 “가명정보”라 한다)

---

따라서, 개인정보보호법 제2조가 개인정보의 정의를 규정하고 있습니다.
</trajectory>
</case>

<case id="C059">
<trajectory>
input: 대출 중도상환수수료는 언제 받을 수 있어?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "대출의 중도상환수수료는 대출자가 대출금을 조기 상환하는 경우 금융기관이 수취하는지, 그리고 그 수취 시점이 언제인지에 관한 규정을 확인하고 싶습니다.", "retrieved": [{"source": "금융소비자보호에관한법률(법률)(제21065호)(20260102)_발췌.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "NH농협은행_전자금융서비스이용약관.txt", "score": null}, {"source": "전자금융감독규정.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에 따르면, 대출의 중도상환수수료는 "금융소비자가 대출만기일이 도래하기 전 대출금의 전부 또는 일부를 상환하는 경우에 부과하는 수수료"로 정의되어 있습니다(제19조 제1항 라목 1)).  
즉, **대출자가 대출금을 만기 전에 조기 상환(중도상환)할 때 금융기관이 수취**하는 수수료입니다.

수취 시점에 대해서는 "대출만기일이 도래하기 전 대출금의 전부 또는 일부를 상환하는 경우에 부과"한다고만 규정되어 있으며, 구체적으로 상환과 동시에 즉시 수취하는지, 아니면 별도의 시점에 수취하는지에 대한 명확한 규정은 문서에서 확인할 수 없습니다.

**정리:**  
- 대출의 중도상환수수료는 대출자가 대출금을 만기 전에 조기 상환할 때 금융기관이 수취합니다.
- 수취 시점에 대한 구체적 규정(예: 상환과 동시인지 등)은 문서에서 확인할 수 없습니다.
</trajectory>
</case>

<case id="C060">
<trajectory>
input: 영업점에 CCTV 설치하면 안내판 달아야 해?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "영업점에 폐쇄회로텔레비전(CCTV)을 설치하는 경우, 관련 법령에 따라 안내판을 설치해야 하는지에 관한 규정을 확인하고 싶습니다.", "retrieved": [{"source": "개인정보 보호 법령 및 지침, 고시 해설서(2020.12).txt", "score": null}, {"source": "개인정보 보호 법령 및 지침, 고시 해설서(2020.12).txt", "score": null}, {"source": "개인정보 보호 법령 및 지침, 고시 해설서(2020.12).txt", "score": null}, {"source": "개인정보 보호 법령 및 지침, 고시 해설서(2020.12).txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에 따르면, 영업점(사업장 등)과 같이 공개된 장소에 영상정보처리기기(CCTV)를 설치하는 경우에는 안내판을 설치해야 합니다.

구체적으로,
- "건물 안에 다수의 영상정보처리기기를 설치하는 경우에는 출입구 등 잘 보이는 곳에 해당 시설 또는 장소 전체가 영상정보처리기기 설치지역임을 표시하는 안내판을 설치할 수 있다(영 제24조제1항 단서)."
- "안내판은 촬영범위 내에서 정보주체가 알아보기 쉬운 장소에 누구라도 용이하게 판독될 수 있게 설치되어야 하고, 이를 충족하였다면 그 범위 내에서 안내판의 크기나 설치위치는 영상정보처리기기 운영자가 자율적으로 정할 수 있다(표준지침 제39조제2항)."

즉, 영업점에 CCTV를 설치하는 경우 관련 법령에 따라 안내판을 설치해야 하며, 안내판은 정보주체(고객 등)가 쉽게 알아볼 수 있는 위치에 설치되어야 합니다. 안내판의 크기나 설치 위치는 운영자가 자율적으로 정할 수 있습니다.

따라서, 영업점에 CCTV를 설치할 때는 안내판 설치 의무가 있습니다.
</trajectory>
</case>
