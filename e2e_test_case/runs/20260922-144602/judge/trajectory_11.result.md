<case id="C051">
<evidence>
- route_query sends the regulation question to policy_qa, which fits.
- build_context rewrites the query around network-separation standards and pulls both the regulation and its commentary.
- guardrail -> finalize is a short linear 4-step path. There are no redundant calls.
- The final answer covers the principle, the definition, exceptions and the related provisions, and it matches the question.
</evidence>
<result>PASS</result>
</case>

<case id="C052">
<evidence>
- policy_qa routing is right. The rewritten query keeps the target (password management standard in the commentary).
- Retrieval hits mostly the commentary file, which is the source the question names.
- The 4 steps run in order with no wasted retries.
- The final answer pulls password points from the retrieved section and cites Article 32, so it follows from the context.
</evidence>
<result>PASS</result>
</case>

<case id="C053">
<evidence>
- policy_qa routing is right. The rewritten query targets termination procedure.
- All 5 retrieved chunks come from the NH e-banking terms, the document the user named.
- The steps are linear and efficient.
- The final answer cites Article 13 with the termination methods, so it answers the question.
</evidence>
<result>PASS</result>
</case>

<case id="C054">
<evidence>
- policy_qa routing is right. The rewritten query targets how to meet the duty to explain when selling online.
- Retrieval comes entirely from the online explanation-duty guideline, which is the relevant source.
- There are 4 steps with no redundancy.
- The final answer lays out scope, priority items, presentation method and consumer-rights notice, so it follows from the context.
</evidence>
<result>PASS</result>
</case>

<case id="C055">
<evidence>
- policy_qa routing is right. The rewritten query targets what must be explained to the customer.
- Retrieval mixes the general and online explanation-duty guidelines, both relevant.
- The path is linear and efficient.
- The final answer lists the important items by product type, plus the explanation-document and online rules, so it addresses the question.
</evidence>
<result>PASS</result>
</case>
