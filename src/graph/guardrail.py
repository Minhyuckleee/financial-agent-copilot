"""3단계 가드레일 — 누적 state로 답변 생성 후 5규칙 자동교정

규칙
1. PII 마스킹 : 주민번호/카드번호/계좌번호 숫자 앞 두자리만 남기고 마스킹
2. 필수고지사항 자동삽입 : 답변 끝에 필수 고지 문구 추가
3. 금지표현/과장 차단 : (a) 사전 문자열 매칭 (prohibited_terms.json의 terms list) + (b) LLM structured output 을 통해 금지표현/과장 차단
4. 숫자/수치 자체검증 : 실제 숫자 및 수치와 답변 속 수치를 대조하여 실제 값으로 대체 
5. citation grounding (RAG 인용 근거 대조) : 답변 문구가 실제 retrieved 된 chunk에서 나왔는지 체크

"""
import json
import re
from pathlib import Path

from pydantic import BaseModel

from graph.llm import get_llm
from graph.state import AgentState, GuardrailCorrection

_GUARDRAIL_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "guardrail"
_NUMERIC_TOLERANCE_DECIMALS = 4  # 규칙④ 숫자 비교 시 소수점 4자리까지 일치 확인

_PII_PATTERNS = [
    (re.compile(r"\d{6}-[1-4]\d{6}"), "주민등록번호"),
    (re.compile(r"\d{4}-\d{4}-\d{4}-\d{4}"), "카드번호"),
    (re.compile(r"\d{2,6}-\d{2,6}-\d{2,8}"), "계좌번호"),
]

_cache: dict | None = None


def _load_prohibited_terms() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads((_GUARDRAIL_DIR / "prohibited_terms.json").read_text(encoding="utf-8"))
    return _cache


def _template_exchange_rate_answer(tool_result: dict | list | None) -> str:
    if not tool_result:
        return "환율 정보를 조회하지 못했습니다."
    base_date = tool_result["base_date"]
    # "YYYY-MM-DD"(대시)로 포맷하면 규칙①의 계좌번호 정규식(\d{2,6}-\d{2,6}-\d{2,8})과
    # 우연히 매칭돼 날짜가 마스킹되는 버그가 있었다(실측으로 발견) — 점 구분자로 회피.
    formatted_date = f"{base_date[:4]}.{base_date[4:6]}.{base_date[6:8]}"
    return f"현재 {tool_result['currency_pair']} 환율은 {tool_result['rate']}원입니다. (기준일: {formatted_date})"


def _draft_answer(state: AgentState) -> str:
    llm = get_llm()
    if state.route == "out_of_scope":
        return "죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다."
    if state.route == "exchange_rate":
        return _template_exchange_rate_answer(state.tool_result)
    if state.route == "policy_qa":
        context = "\n\n".join(c["content"] for c in state.retrieved_chunks) or "(검색된 문서 없음)"
        question = state.rewritten_query or state.query
        prompt = (
            "아래 문서를 참고해 질문에 답하세요. 문서에서 답을 확인할 수 없으면 "
            "지어내지 말고 확인할 수 없다고 정직하게 답하세요.\n\n"
            f"문서:\n{context}\n\n질문: {question}"
        )
        return llm.invoke(prompt).content.strip()
    prompt = (
        f"다음 tool 조회 결과를 바탕으로 사용자 질문에 자연어로 답하세요. "
        f"결과에 없는 숫자를 지어내지 마세요.\n\n"
        f"질문: {state.query}\ntool 조회 결과: {state.tool_result}"
    )
    if state.tier2_retry_count > 0 and state.tier2_failed_params:
        # Tier2 재시도가 조건을 완화해 성공하면 원래 조건(예: 특정 은행명)이 최종
        # 답변에서 조용히 사라져 상담직원이 이 결과를 원래 조건에 맞는 것으로 오인할
        # 위험이 있었음(테스트에서 발견) — 무엇이 바뀌었는지 명시하도록 지시를 추가한다.
        prompt += (
            f"\n\n참고: 처음엔 {state.tier2_failed_params} 조건으로 조회했으나 결과가 "
            f"없어 조건을 완화해 {state.tool_params}로 다시 조회했습니다. 두 조건에 "
            f"차이가 있다면(예: 특정 은행명이 빠졌다면) 원래 조건으로는 결과가 없었고 "
            f"조건을 넓혀 안내한다는 사실을 답변에 명시하세요."
        )
    return llm.invoke(prompt).content.strip()


def _mask_pii(text: str) -> tuple[str, list[GuardrailCorrection]]:
    corrections = []
    for pattern, label in _PII_PATTERNS:
        def _mask(m: re.Match) -> str:
            digits_only = re.sub(r"\D", "", m.group())
            return digits_only[:2] + "*" * (len(digits_only) - 2)

        new_text, n = pattern.subn(_mask, text)
        if n:
            corrections.append(
                GuardrailCorrection(rule="pii_masking", reason=f"{label} 패턴 {n}건 발견", applied_fix="마스킹 처리")
            )
            text = new_text
    return text, corrections


def _insert_disclosure(text: str, tool_name: str | None) -> tuple[str, list[GuardrailCorrection]]:
    data = _load_prohibited_terms()
    disclosure = data["required_disclosure"]
    if tool_name not in disclosure["applies_to_tools"]:
        return text, []
    if any(term in text for term in disclosure["required_any_terms"]):
        return text, []
    return text + disclosure["insertion_text"], [
        GuardrailCorrection(
            rule="disclosure_missing", reason="필수고지사항 누락", applied_fix="고지문구 자동삽입"
        )
    ]


class _SemanticProhibitedCheck(BaseModel):
    contains_prohibited_claim: bool
    matched_phrase: str | None = None


def _remove_sentence_containing(text: str, phrase: str) -> str:
    """문구만 지우면 "이 ." 처럼 문법이 깨진 문장이 남는다 — 그 문구가 속한 문장
    전체를 지운다. 문장 경계는 마침표/느낌표/물음표 뒤 공백·줄바꿈 기준."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    kept = [s for s in sentences if phrase not in s]
    result = " ".join(kept)
    return re.sub(r"\s+", " ", result).strip()


def _block_prohibited_terms(text: str) -> tuple[str, list[GuardrailCorrection]]:
    data = _load_prohibited_terms()
    corrections = []
    for rule in data["rules"]:
        for term in rule["terms"]:
            if term in text:
                text = _remove_sentence_containing(text, term)
                corrections.append(
                    GuardrailCorrection(
                        rule="prohibited_terms",
                        reason=f"금지표현 '{term}' 발견({rule['category']})",
                        applied_fix="해당 문구가 포함된 문장 제거",
                    )
                )

    llm = get_llm().with_structured_output(_SemanticProhibitedCheck)
    all_reasons = "; ".join(r["reason"] for r in data["rules"])
    prompt = (
        "다음은 은행 상담직원이 고객에게 전달할 답변입니다. 아래 금지 유형에 해당하는 "
        "'표현'이 있는지만 판단하세요 — 사전에 있는 단어와 정확히 일치하지 않아도, 같은 "
        "의미를 돌려 말한 짧은 문구가 있으면 그 문구만 찾으세요.\n\n"
        "금지 유형(전부 상품의 손실·수익·순위에 대한 과장/단정 표현입니다. 시세·금리·환율 같은 "
        "사실을 있는 그대로 진술하는 것은 절대 해당하지 않습니다):\n"
        f"{all_reasons}\n\n"
        "위 유형에 해당하는 표현이 없으면 contains_prohibited_claim=false, matched_phrase=null로 "
        "답하세요. 있으면 matched_phrase에 답변 원문 그대로의 짧은 문구(전체 문장이 아니라 "
        "문제되는 단어/구절만)를 넣으세요.\n\n"
        f"답변: {text}"
    )
    result: _SemanticProhibitedCheck = llm.invoke(prompt)
    # 예전엔 matched_phrase 길이가 전체 텍스트의 60% 미만이어야 안전하다고 봤는데,
    # 테스트에서 실측해보니 LLM은 짧은 한 문장짜리 위반을 정확히 찾아내도
    # (contains_prohibited_claim=True) 그 문장 자체가 이미
    # 전체의 60%를 넘는 경우가 흔해 정당한 탐지가 매번 걸러졌음(미탐 10/16). 근거
    # 없이 자의적이던 비율 제한을 없애고, _remove_sentence_containing 자체가
    # "문장 단위로만 삭제"라는 실질적 안전장치를 이미 갖고 있으므로 그걸로 충분하다고
    # 판단(여러 문장에 걸친 phrase는 어차피 한 문장 안에서 못 찾아 no-op됨).
    is_safe_span = result.matched_phrase and result.matched_phrase in text
    if result.contains_prohibited_claim and is_safe_span:
        text = _remove_sentence_containing(text, result.matched_phrase)
        corrections.append(
            GuardrailCorrection(
                rule="prohibited_terms",
                reason=f"금지표현과 의미상 동일한 표현 '{result.matched_phrase}' 발견(semantic 탐지)",
                applied_fix="해당 문구가 포함된 문장 제거",
            )
        )
    return text, corrections


def _flatten_numbers(obj) -> list[float]:
    numbers: list[float] = []
    if isinstance(obj, bool):
        return numbers
    if isinstance(obj, (int, float)):
        numbers.append(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            numbers.extend(_flatten_numbers(v))
    elif isinstance(obj, list):
        for v in obj:
            numbers.extend(_flatten_numbers(v))
    return numbers


_EXCHANGE_RATE_REPORTED_PATTERN = re.compile(r"환율은\s*([\d,]+\.?\d*)원")


def _extract_reported_number(text: str, route: str | None) -> float | None:
    """exchange_rate는 `_template_exchange_rate_answer`가 만든 고정 포맷이라 정규식으로
    100% 신뢰 가능 — LLM 호출 없이 추출한다. product_recommendation은
    `_check_product_rates`가 별도 처리하므로 이 함수는 exchange_rate 전용이다."""
    if route != "exchange_rate":
        return None
    match = _EXCHANGE_RATE_REPORTED_PATTERN.search(text)
    return float(match.group(1).replace(",", "")) if match else None


_RATE_PATTERN = re.compile(r"(\d+\.?\d*)\s*%")


def _check_product_rates(text: str, tool_result: list[dict]) -> tuple[str, list[GuardrailCorrection]]:
    if not tool_result:
        return text, []

    mentions = []
    for entry in tool_result:
        bank = entry.get("bank_name")
        pos = text.find(bank) if bank else -1
        if pos != -1:
            mentions.append((pos, bank, entry))
    mentions.sort(key=lambda m: m[0])

    corrections: list[GuardrailCorrection] = []
    edits: list[tuple[int, int, str]] = []
    for i, (pos, bank, entry) in enumerate(mentions):
        segment_end = mentions[i + 1][0] if i + 1 < len(mentions) else len(text)
        rate_match = _RATE_PATTERN.search(text, pos, segment_end)
        if not rate_match:
            continue

        reported = float(rate_match.group(1))
        actual_values = _flatten_numbers(entry)
        if not actual_values:
            continue
        if any(round(reported, _NUMERIC_TOLERANCE_DECIMALS) == round(a, _NUMERIC_TOLERANCE_DECIMALS) for a in actual_values):
            continue

        closest = min(actual_values, key=lambda a: abs(a - reported))
        edits.append((rate_match.start(1), rate_match.end(1), str(closest)))
        corrections.append(
            GuardrailCorrection(
                rule="numeric_self_check",
                reason=f"{bank} 금리 답변({reported})이 원본 데이터({closest})와 불일치",
                applied_fix=f"{closest}로 교체",
            )
        )

    for start, end, replacement in sorted(edits, key=lambda e: e[0], reverse=True):
        text = text[:start] + replacement + text[end:]

    return text, corrections


def _self_check_numbers(text: str, tool_result, route: str | None = None) -> tuple[str, list[GuardrailCorrection]]:
    if tool_result is None:
        return text, []

    if route == "product_recommendation":
        return _check_product_rates(text, tool_result)

    reported_value = _extract_reported_number(text, route)
    if reported_value is None:
        return text, []

    actual_values = _flatten_numbers(tool_result)
    if not actual_values:
        return text, []

    reported = round(reported_value, _NUMERIC_TOLERANCE_DECIMALS)
    if any(reported == round(actual, _NUMERIC_TOLERANCE_DECIMALS) for actual in actual_values):
        return text, []

    closest_actual = min(actual_values, key=lambda a: abs(a - reported_value))
    corrected = text.replace(str(reported_value), str(closest_actual))
    return corrected, [
        GuardrailCorrection(
            rule="numeric_self_check",
            reason=f"답변 수치({reported_value})가 원본 데이터({closest_actual})와 불일치",
            applied_fix=f"{closest_actual}로 교체",
        )
    ]


class _CitationCheck(BaseModel):
    has_citation_claim: bool
    claimed_phrase: str | None = None
    grounded: bool | None = None


def _check_grounding_llm(text: str, retrieved_chunks: list[dict]) -> _CitationCheck:
    """claim 추출과 entailment 판정을 한 콜에 같이 한다 — 임베딩 코사인은 숫자·조항번호·
    긍정/부정 하나만 바뀐 미세조작(가장 위험한 실패유형)을 실측에서 못 잡아서(negative
    5개 파일럿, positive 구간과 심하게 겹침) 폐기하고 LLM이 직접 chunk 내용과 대조해
    판정하는 방식으로 전환. claim 추출만 하던 콜을 그대로 확장했을 뿐이라 콜 수는
    안 늘어난다("불필요한 API 호출 최소화" 제약 유지)."""
    llm = get_llm().with_structured_output(_CitationCheck)
    chunks_text = "\n\n---\n\n".join(c["content"] for c in retrieved_chunks)
    prompt = (
        "다음은 사내규정질의에 대한 답변과, 그 답변을 생성할 때 검색된 문서입니다.\n\n"
        "1. 답변이 문서 내용을 근거로 구체적 사실을 서술한 부분이 있으면 그 문구(전체 "
        "문장이 아니라 핵심 사실관계 구절)를 claimed_phrase에 답변 원문 그대로 넣고 "
        "has_citation_claim=true로 답하세요. 그 서술에 조항번호·법령명 등 근거표시가 "
        "괄호 등으로 붙어 있으면 반드시 그것까지 claimed_phrase에 포함하세요(조항번호만 "
        "따로 조작됐을 수 있어 빠지면 안 됩니다). 그런 서술이 없으면(모른다는 답변, "
        "일반적 안내 등) has_citation_claim=false, grounded는 null로 답하세요.\n"
        "2. claim이 있으면, 아래 문서가 그 claim을 실제로 뒷받침하는지 grounded에 "
        "true/false로 답하세요. 주제가 같다고 자동으로 grounded=true가 아닙니다 — "
        "숫자·기간·조항번호·기관명이 문서와 정확히 일치하는지, 결론(가능/불가능, 해야 "
        "함/안 해도 됨)이 문서와 같은 방향인지까지 대조하세요. 이 중 하나라도 문서와 "
        "다르면 grounded=false로 판정하세요.\n\n"
        f"문서:\n{chunks_text}\n\n답변: {text}"
    )
    return llm.invoke(prompt)


def _check_citation_grounding(text: str, retrieved_chunks: list[dict]) -> tuple[str, list[GuardrailCorrection]]:
    if not retrieved_chunks:
        return text, []

    result = _check_grounding_llm(text, retrieved_chunks)
    if not result.has_citation_claim or not result.claimed_phrase or result.claimed_phrase not in text:
        return text, []
    if result.grounded is not False:
        return text, []

    sources = ", ".join(sorted({c["source"] for c in retrieved_chunks}))
    corrected = _remove_sentence_containing(text, result.claimed_phrase)
    corrected = f"{corrected} (참고 문서: {sources})".strip()
    return corrected, [
        GuardrailCorrection(
            rule="citation_grounding",
            reason=f"인용 주장 '{result.claimed_phrase}'이 검색 문서로 뒷받침되지 않음(LLM entailment 판정)",
            applied_fix="해당 문구가 포함된 문장 제거, 참고 문서명만 유지",
        )
    ]


def run_guardrail(state: AgentState) -> dict:
    text = state.answer if state.answer is not None else _draft_answer(state)
    all_corrections: list[GuardrailCorrection] = []

    text, corrections = _mask_pii(text)
    all_corrections.extend(corrections)

    text, corrections = _insert_disclosure(text, state.tool_name)
    all_corrections.extend(corrections)

    text, corrections = _block_prohibited_terms(text)
    all_corrections.extend(corrections)

    text, corrections = _self_check_numbers(text, state.tool_result, state.route)
    all_corrections.extend(corrections)

    text, corrections = _check_citation_grounding(text, state.retrieved_chunks)
    all_corrections.extend(corrections)

    return {"answer": text, "guardrail_corrections": all_corrections}
