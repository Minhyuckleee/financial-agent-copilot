"""AgentState — 그래프 전체가 공유하는 상태 스키마 (전 단계가 공유)

구성
1. AgentState : 전체 상태. 0~4단계 각각이 쓰는/읽는 필드를 구획(라우팅 결과, RAG 검색결과, tool 호출결과, 에러상태, 가드레일 교정내역, 최종답변)
2. ToolError : Tier1/Tier2 예외분기가 참조하는 에러 타입 5종(fail/delay/param_invalid/empty_result/no_selection)
3. GuardrailCorrection : 가드레일 5규칙 중 뭐가 걸려서 어떻게 고쳤는지 기록

설계 : Pydantic BaseModel(런타임 검증). 노드는 state를 직접 수정하지 않고 바뀐 필드만 담은 partial dict 반환. 에러도 예외 대신 error 필드로 표현(Literal 타입 고정, 매직스트링 비교 방지)
"""
from typing import Annotated, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

RouteLabel = Literal[
    "product_recommendation",  # 상품추천
    "exchange_rate",  # 환율조회
    "policy_qa",  # 사내규정질의
    "out_of_scope",  # 범위외
]

ToolErrorType = Literal["fail", "delay", "param_invalid", "empty_result", "no_selection"]


class ToolError(BaseModel):
    """Tier1(API 레벨)/Tier2(해석 레벨) 예외분기가 참조하는 상태 필드.

    type: fail=RuntimeError(재시도 가치 있음), delay=TimeoutError(포기),
    param_invalid=Pydantic 검증 실패(Tier2로 통합),
    empty_result=API 정상이나 결과 없음(Tier2),
    no_selection=API 호출 자체를 시도 안 함(LLM이 tool을 하나도 선택 안 함,
    Tier2로 통합 — tool_call.py가 조용히 `{}`만 반환하던 무신호 실패였음).
    """

    type: ToolErrorType
    message: str


class GuardrailCorrection(BaseModel):
    """가드레일 5규칙 중 하나가 감지해 자동으로 교정한 기록. 전량검사로 여러 개
    누적될 수 있다. HITL 없음 — 5규칙 전부 원본 데이터 기준 정답이 이미 있어
    자동교정 가능하다는 판단."""

    rule: Literal[
        "pii_masking",  # ①민감정보 마스킹
        "disclosure_missing",  # ②필수고지사항 누락
        "prohibited_terms",  # ③금지표현 차단
        "numeric_self_check",  # ④숫자 자체검증
        "citation_grounding",  # ⑤RAG 인용 grounding체크
    ]
    reason: str
    applied_fix: str


class AgentState(BaseModel):
    # --- 입력/이력 ---
    query: str
    history: Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)

    # --- 0. 라우팅 (Tier0) ---
    route: RouteLabel | None = None
    tier0_retry_count: int = 0  # "범위외" 분류 자체가 트리거. 상한 1.

    # --- 1. context 구성 ---
    rewritten_query: str | None = None  # 사내규정질의 한정 query rewrite 결과
    retrieved_chunks: list[dict] = Field(default_factory=list)

    # --- 2. tool call ---
    tool_name: str | None = None
    tool_params: dict | None = None
    tool_result: dict | list | None = None  # 원본 API 응답(가드레일 규칙④가 참조)
    tool_call_attempt_count: int = 0  # Tier1 fail 재시도용. 상한 2.
    tier2_retry_count: int = 0  # 파라미터 재해석 재시도용. 상한 1.
    tier2_failed_params: dict | None = None  # Tier2 최초 시도가 실패했을 때의 원본 파라미터
    # (재시도가 조건을 완화해 성공하면 원래 조건이 최종 답변에서 조용히 사라지는
    # 버그가 있었음. answer 단계가 "원래 무엇을 못 찾았는지"를 알 수 있도록 최초
    # 시도 시점 파라미터를 보존한다.)

    # --- 2. tool call 예외분기 (Tier1/Tier2) ---
    error: ToolError | None = None
    low_confidence: bool = False  # Tier2 캡 초과 등. answer 단계에서 한계 명시.

    # --- 3. 가드레일 (자동교정, HITL 없음) ---
    guardrail_corrections: list[GuardrailCorrection] = Field(default_factory=list)

    # --- 4. answer ---
    answer: str | None = None
