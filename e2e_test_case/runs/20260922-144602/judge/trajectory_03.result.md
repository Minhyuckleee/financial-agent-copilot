<case id="C011">
<evidence>
- Routed to product_recommendation, which fits a loan-rate question
- recommend_credit_loan_products called with bank_name_filter=카카오뱅크, no error, 2 results
- Disclosure guardrail ran, then finalize; answer gives both product rates plus a disclaimer
- Four steps in a clean, logical order with no waste
</evidence>
<result>PASS</result>
</case>

<case id="C012">
<evidence>
- Correct route; tool args include credit_score=750 and bank filter 신한, both taken from the query
- 2 results; the disclosure and numeric_self_check guardrails were applied
- Answer names the score band (701~800) and the rates for both products
- Efficient, logical progression
</evidence>
<result>PASS</result>
</case>

<case id="C013">
<evidence>
- Correct route; broad tool call with empty args suits a general comparison request
- 3 results returned and all 3 are compared in the answer, with the score band stated
- Disclosure guardrail ran, then finalize
- Clear progression, no wasted steps
</evidence>
<result>PASS</result>
</case>

<case id="C014">
<evidence>
- The query asks which bank has the lowest overdraft-account (마이너스통장) rate. This is a credit-loan product question inside the agent's scope (the same tool handled 마이너스한도대출 in C011/C013)
- route_query sent it to out_of_scope anyway, even after rewriting the query correctly
- No tool was called; the final answer is a refusal, so the goal was not achieved
</evidence>
<result>FAIL</result>
</case>

<case id="C015">
<evidence>
- Correct route, and the right tool (recommend_jeonse_loan_products) returned 3 results
- The guardrail ran only prohibited_terms. The disclosure check used in the other recommendation cases was missing, and the answer has no disclaimer
- The final answer mentions just one product, in a "참고로" fragment. It does not compare the 3 retrieved results or say which is lowest
- The retrieved data was not carried through to an answer that meets the request
</evidence>
<result>FAIL</result>
</case>
