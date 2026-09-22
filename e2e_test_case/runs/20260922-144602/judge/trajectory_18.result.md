<case id="E016">
<evidence>
- Follow-up "기한 지나면요?" is resolved against history into a self-contained query about what happens after the correction-request period expires.
- Routed to policy_qa, the right route for a regulation question.
- build_context pulls the 전자금융거래법 and 전자금융감독규정 documents, which are relevant sources.
- Guardrail passes, then finalize. The answer uses the retrieved 제8조 content and says plainly that no expiry rule could be found.
- The steps run in a straight line with no redundant calls.
</evidence>
<result>PASS</result>
</case>

<case id="E017">
<evidence>
- A savings product recommendation request is routed to out_of_scope, which fits an agent that does not make product recommendations.
- route -> answer_out_of_scope -> finalize: the shortest correct path.
- The rewrite adds "어떤 은행의", but it does not change the intent or the route.
- The final output is a polite out-of-scope decline.
</evidence>
<result>PASS</result>
</case>

<case id="E018">
<evidence>
- A request for a live JPY exchange rate needs real-time market data, so out_of_scope is a reasonable route.
- route -> answer_out_of_scope -> finalize: minimal and logical.
- The final output is a consistent decline.
</evidence>
<result>PASS</result>
</case>

<case id="E019">
<evidence>
- A fund recommendation based on recent returns is investment advice, so out_of_scope is correct.
- route -> answer_out_of_scope -> finalize, with no unnecessary tool calls.
- The final output is a consistent decline.
</evidence>
<result>PASS</result>
</case>

<case id="E020">
<evidence>
- A credit card product recommendation is routed to out_of_scope, which matches the handling of the other recommendation requests.
- route -> answer_out_of_scope -> finalize: efficient.
- The final output is a consistent decline.
</evidence>
<result>PASS</result>
</case>
