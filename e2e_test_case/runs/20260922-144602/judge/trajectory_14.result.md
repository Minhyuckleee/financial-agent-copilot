<case id="C066">
<evidence>
Follow-up asks for 24-month term; routed to product_recommendation.
Single recommend_deposit_products call with save_term_months=24, no error, 3 results.
disclosure_missing guardrail fired and final output carries the disclosure line.
Logical, efficient progression to the goal.
</evidence>
<result>PASS</result>
</case>

<case id="C067">
<evidence>
Follow-up changes credit score from 700 to 850; routed to product_recommendation.
Single recommend_credit_loan_products call with credit_score=850, 3 results, no error.
Guardrails (disclosure, numeric check) run, then finalize; output lists rates for the 801~900 band with disclosure.
Clear, efficient single-pass trajectory.
</evidence>
<result>PASS</result>
</case>

<case id="C068">
<evidence>
Re-query request for USD rate; routed to exchange_rate.
One inquire_exchange_rate call, 1 result, no error.
Final output gives refreshed rate with reference date.
Minimal, logical steps.
</evidence>
<result>PASS</result>
</case>

<case id="C069">
<evidence>
Follow-up narrows prior jeonse loan list to Kookmin Bank; routed to product_recommendation.
recommend_jeonse_loan_products called with bank_name_filter="국민", 2 results, no error.
numeric_self_check run, then finalize; output lists only KB products.
Direct and efficient.
</evidence>
<result>PASS</result>
</case>

<case id="C070">
<evidence>
Follow-up about requesting a copy of the deposit terms; routed to policy_qa.
build_context rewrites the query using history context and retrieves mostly 예금거래기본약관.txt chunks.
Guardrail then finalize; answer grounded in quoted clause on 교부 청구.
Coherent retrieval-then-answer progression, no wasted steps.
</evidence>
<result>PASS</result>
</case>
