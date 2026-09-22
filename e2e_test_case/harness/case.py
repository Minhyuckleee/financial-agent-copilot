"""e2e 평가 케이스와 결정론 채점.

결정론은 agent 의 **행동**만 본다 — 어느 route 로 갔나, 어떤 tool 을 어떤 인자로 불렀나.
답변 문장은 보지 않는다. 문장을 문자열로 채점하면 표현이 다른 정답이 실패로 찍힌다
(기존 평가셋의 라벨 오류 원인). 의미 판정은 judge 몫이다.
"""
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

#: edge 로 분류하려면 이 중 하나를 붙여야 한다. 못 붙이면 core 다.
#: 난이도를 "자주 틀리는 것" 으로 정의하면 순환논리가 되므로 입력 특성으로만 정의한다.
TAGS = {
    "ellipsis_followup",      # "왜 그래요?" — 맥락이 빠진 후속 발화 (Tier0)
    "condition_carryover",    # "그 은행으로" — 이전 턴 조건을 이어받아야 한다
    "topic_switch",           # 예금 → 신용대출. 이전 tool 을 고수하면 안 된다
    "unsupported_condition",  # 18개월 — API 에 없는 조건 (Tier2)
    "tool_unavailable",       # 적금·엔화 — 이 agent 의 tool 이 다루지 않는다
    "tool_confusion",         # 전세 vs 주담대, 신용 vs 개인사업자
    "corpus_boundary",        # 사내규정 코퍼스 밖의 규정 (청크 원문에서 없음을 확인한 것만)
    "customer_data",          # 고객 계좌·심사 정보 — 이 agent 는 접근하지 않는다
}

ROUTES = {"product_recommendation", "exchange_rate", "policy_qa", "out_of_scope"}


class Turn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    사용자: str
    에이전트: str


class Case(BaseModel):
    # 모르는 키를 조용히 무시하면 오타 난 케이스가 영원히 통과한다
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    id: str
    question: str = Field(alias="질문")
    history: list[Turn] = Field(default_factory=list, alias="이력")

    # 분류 — 채점하지 않는다. 리포트를 쪼개는 데만 쓴다
    # tier 는 파일에 적지 않는다. core/ · edge/ 중 어느 폴더에 있는지로 정해진다
    tier: str = "core"
    question_type: str = Field(default="답한다", alias="유형")
    tags: list[str] = Field(default_factory=list, alias="태그")

    # 결정론이 읽는다
    expected_route: list[str] = Field(default_factory=list, alias="기대route")
    required_tools: list[str] = Field(default_factory=list, alias="필수도구")
    forbidden_tools: list[str] = Field(default_factory=list, alias="금지도구")
    no_tools: bool = Field(default=False, alias="도구없음")
    expected_args: dict[str, dict] = Field(default_factory=dict, alias="기대인자")
    forbidden_args: dict[str, list[str]] = Field(default_factory=dict, alias="금지인자")

    # 답변 judge 가 읽는다 — 정답 문장이 아니라 체크리스트
    expected_behavior: list[str] = Field(default_factory=list, alias="기대동작")

    note: str | None = Field(default=None, alias="메모")

    @model_validator(mode="after")
    def _check(self):
        if unknown := [t for t in self.tags if t not in TAGS]:
            raise ValueError(f"{self.id}: 모르는 태그 {unknown}")
        if self.tier == "edge" and not self.tags:
            raise ValueError(f"{self.id}: edge 인데 태그가 없다. 이유를 못 대면 core 다")
        if self.tier == "core" and self.tags:
            raise ValueError(f"{self.id}: core 에 태그가 있다. 태그가 붙으면 edge 폴더로 옮긴다")
        if bad := [r for r in self.expected_route if r not in ROUTES]:
            raise ValueError(f"{self.id}: 모르는 route {bad}")
        return self


def load_case(path) -> Case:
    """카드 한 장. 파일 이름이 id 이고, 부모 폴더가 tier 다."""
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if raw.get("id") and raw["id"] != path.stem:
        raise ValueError(f"{path}: 파일 이름({path.stem})과 id({raw['id']})가 다르다")
    tier = path.parent.name
    if tier not in ("core", "edge"):
        raise ValueError(f"{path}: core/ 나 edge/ 안에 있어야 한다")
    return Case(**{"id": path.stem, **raw, "tier": tier})


def load_cases(root) -> list[Case]:
    """root/core/*.yaml · root/edge/*.yaml 전부. 파일 이름 순."""
    root = Path(root)
    return [load_case(p) for tier in ("core", "edge")
            for p in sorted((root / tier).glob("*.yaml"))]


class CaseResult(BaseModel):
    case_id: str
    passed: bool
    reasons: list[str] = Field(default_factory=list)


def _arg_matches(expected, actual) -> bool:
    """`{포함: 국민}` 이면 부분 일치. 그 밖은 정확 일치.

    은행명을 정확 일치로 비교하면 "국민" · "국민은행" · "KB국민은행" 중 하나만 정답이 된다.
    어느 쪽이든 tool 은 같은 결과를 내므로 정상 동작이 실패로 찍힌다.
    """
    if isinstance(expected, dict) and "포함" in expected:
        return actual is not None and str(expected["포함"]) in str(actual)
    return actual == expected


def score(case: Case, trace: dict) -> CaseResult:
    """trace 는 run.py 가 만든 실행 기록. 답변 문장은 보지 않는다.

    - 필수도구·금지도구·도구없음은 **대화 전체의 호출 집합**으로 본다.
    - 기대인자는 **그 tool 의 첫 호출**만 본다. Tier2 재해석은 일부러 조건을 바꾸는
      동작이라 마지막 호출로 보면 "18개월 → 12개월" 케이스가 늘 실패한다.
      사용자가 말한 조건을 처음에 제대로 넣었는지가 여기서 재는 것이다.
    - 금지인자는 **모든 호출**에서 본다. 지어낸 조건은 재시도에서도 안 된다.
    """
    calls = trace["tool_calls"]
    called = {c["name"] for c in calls}
    reasons = []

    if case.expected_route and trace["route"] not in case.expected_route:
        reasons.append(f"route: 기대 {case.expected_route} · 실제 {trace['route']}")

    if case.no_tools and called:
        reasons.append(f"tool 을 부르면 안 되는데 불렀다: {sorted(called)}")
    if missing := [t for t in case.required_tools if t not in called]:
        reasons.append(f"필수 tool 을 안 불렀다: {missing}")
    if hit := [t for t in case.forbidden_tools if t in called]:
        reasons.append(f"금지 tool 을 불렀다: {hit}")

    first_args: dict[str, dict] = {}
    for c in calls:
        first_args.setdefault(c["name"], c.get("args") or {})
    for tool, expected in case.expected_args.items():
        if tool not in first_args:
            continue  # 안 부른 것은 필수도구가 잡는다. 여기서 이중으로 세지 않는다
        for k, v in expected.items():
            actual = first_args[tool].get(k)
            if not _arg_matches(v, actual):
                reasons.append(f"{tool}.{k} (첫 호출): 기대 {v!r} · 실제 {actual!r}")

    for tool, banned in case.forbidden_args.items():
        for c in calls:
            if c["name"] != tool:
                continue
            args = c.get("args") or {}
            if made_up := [k for k in banned if args.get(k) not in (None, "")]:
                reasons.append(f"{tool} 에 말하지 않은 조건을 넣었다: "
                               f"{ {k: args[k] for k in made_up} }")

    return CaseResult(case_id=case.id, passed=not reasons, reasons=reasons)
