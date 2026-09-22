<case id="E006">
<evidence>Follow-up asks for Hana Bank from the previous 6-month deposit request.
Routed to product_recommendation, then called recommend_deposit_products with save_term_months=6 (carried over) and bank_name_filter="하나".
Tool returned 1 result without error. Disclosure guardrail ran and the disclaimer appears in the output.
Four steps, logical and efficient; the answer matches the tool result.</evidence>
<result>PASS</result>
</case>

<case id="E007">
<evidence>The user asks to apply the same 650 credit score to business loans.
Routed to product_recommendation and called recommend_business_loan_products with credit_score=650 carried over from history.
Tool returned 3 results. Numeric self-check guardrail ran, then the agent finalized.
Direct progression with no wasted steps; the output lists the 3 products for the 601~700 band.</evidence>
<result>PASS</result>
</case>

<case id="E008">
<evidence>The elliptical follow-up "전세대출은?" comes after a Nonghyup mortgage question.
Routed to product_recommendation and called recommend_jeonse_loan_products with bank_name_filter="농협" carried over.
Tool returned 3 results without error. Guardrail ran, then the agent finalized.
Context was resolved correctly and the path is minimal; the output matches the query.</evidence>
<result>PASS</result>
</case>

<case id="E009">
<evidence>Topic switched from deposit recommendations to exchange rates.
Routed correctly to exchange_rate and called inquire_exchange_rate, which returned 1 result without error.
Guardrail ran, then the agent finalized. The output gives the USD/KRW rate with its reference date.
Clean switch with no leftover deposit context misapplied.</evidence>
<result>PASS</result>
</case>

<case id="E010">
<evidence>Topic switched to how to obtain consent for personal-data collection.
Routed to policy_qa. build_context rewrote the query to include the credit-loan marketing context from history and retrieved 6 relevant regulatory documents (Credit Information Act, privacy Q&amp;A, privacy guidelines).
Guardrail ran, then the agent finalized. The answer is grounded in the retrieved sources and cites them.
The progression is logical and efficient.</evidence>
<result>PASS</result>
</case>
