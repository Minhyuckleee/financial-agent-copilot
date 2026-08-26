"""`StateGraph.invoke()` 경계 테스트 — Tier1(API fail/delay) e2e 스모크.

`FAULT_INJECTION` 환경변수로 강제 유발. call_tool→call_tool self-loop(그래프 레벨
재시도)가 실제로 동작하는지, delay는 재시도 없이 즉시 포기하는지 전체 그래프로 확인한다.
"""
import json

from dotenv import load_dotenv

from graph.builder import build_graph
from graph.state import AgentState
from tools.fault_injection import _fail_once_used

load_dotenv()


def test_fail_once_retries_via_graph_self_loop_and_succeeds_e2e(monkeypatch):
    _fail_once_used["inquire_exchange_rate"] = False
    monkeypatch.setenv("FAULT_INJECTION", json.dumps({"inquire_exchange_rate": "fail_once"}))

    graph = build_graph()
    result = graph.invoke(AgentState(query="환율 알려줘"))

    assert result["error"] is None
    assert result["tool_call_attempt_count"] == 2
    assert "환율" in result["answer"]


def test_fail_exhausts_retry_cap_and_gives_honest_message_e2e(monkeypatch):
    monkeypatch.setenv("FAULT_INJECTION", json.dumps({"inquire_exchange_rate": "fail"}))

    graph = build_graph()
    result = graph.invoke(AgentState(query="환율 알려줘"))

    assert result["error"].type == "fail"
    assert result["tool_call_attempt_count"] == 2
    assert result["answer"] == "죄송합니다, 일시적인 시스템 오류로 조회에 실패했습니다. 잠시 후 다시 시도해주세요."


def test_delay_gives_up_immediately_without_retry_e2e(monkeypatch):
    monkeypatch.setenv("FAULT_INJECTION_DELAY_SECONDS", "0")
    monkeypatch.setenv("FAULT_INJECTION", json.dumps({"inquire_exchange_rate": "delay"}))

    graph = build_graph()
    result = graph.invoke(AgentState(query="환율 알려줘"))

    assert result["error"].type == "delay"
    assert result["tool_call_attempt_count"] == 1
    assert result["answer"] == "죄송합니다, 응답 지연으로 조회를 완료하지 못했습니다. 잠시 후 다시 시도해주세요."
