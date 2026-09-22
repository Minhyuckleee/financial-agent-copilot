<case id="E021">
<evidence>
- The user asked for mortgage (주담대) rates only, and the agent routed to product_recommendation.
- It called recommend_mortgage_loan_products, which matches the product type, and got 3 results.
- The guardrail passed cleanly. The final answer lists the 3 mortgage products with rates and says jeonse loans were left out.
- The path is direct and efficient, with no wasted steps.
</evidence>
<result>PASS</result>
</case>

<case id="E022">
<evidence>
- The user is a sole proprietor asking about loans. The agent routed to product_recommendation and called recommend_business_loan_products, the right tool for this user type.
- It passed credit_score=700 even though the user never gave one. This is an assumed default, but the answer states the 601-700 band it used.
- The guardrail raised numeric_self_check and the flow went on to finalize. The numbers in the answer match the scoped band.
- The path is a single tool call, logical and efficient.
</evidence>
<result>PASS</result>
</case>

<case id="E023">
<evidence>
- The user asked for monthly-rent deposit loan (월세 보증금 대출) rates. This is a loan-rate question in the same domain as the other loan cases, and a rent/jeonse loan tool exists (see E021).
- The router sent it to out_of_scope, even though its own rewritten query is a clear loan-rate request.
- No tool was tried and no nearby product (for example rent or jeonse loans) was looked up.
- The final answer is a generic refusal with no useful information. The routing step made the goal unreachable.
</evidence>
<result>FAIL</result>
</case>

<case id="E024">
<evidence>
- The user explicitly wants a personal credit loan despite running a business. The agent routed to product_recommendation and called recommend_credit_loan_products, which follows that stated intent.
- The tool returned 3 results. The guardrail flagged disclosure_missing, and the final answer includes a disclosure line, so the flag was handled.
- The answer lists 3 products with rates for the stated credit band.
- The progression is clear and efficient.
</evidence>
<result>PASS</result>
</case>

<case id="E025">
<evidence>
- This is a policy question about when the right to request a lower loan rate (금리인하요구권) applies. The agent routed to policy_qa and built context with a sensible rewritten query.
- Retrieval returned only the online explanation-duty guideline and the Credit Information Act, neither of which is the core source for this right, and there were no scores.
- The agent did not retry or reformulate, but it answered honestly that the documents do not cover the topic and did not make anything up.
- The steps are logically consistent, and the outcome correctly reports that the information could not be found. A retry is optional under the rubric.
</evidence>
<result>PASS</result>
</case>
