"""④ 예외분기 지원 — tool 클라이언트에 씌우는 fault-injection 래퍼

모드(FAULT_INJECTION 환경변수, JSON)
1. fail : 강제로 RuntimeError(Tier1 fail 경로 테스트)
2. delay : 지연 후 TimeoutError(Tier1 delay 경로 테스트)
3. fail_once : 1회차만 실패, 2회차부터 통과("재시도 후 성공" 경로 테스트, hard set 전용 — 기존 fail/delay는 "최종실패"만 검증했음)

환경변수 없으면 실제 API 그대로 통과 — 프로덕션/테스트 경로가 같은 코드베이스 공유
"""
import functools
import json
import logging
import os
import time
from typing import Callable

logger = logging.getLogger(__name__)

_fail_once_used: dict[str, bool] = {}


def reset_fail_once_state() -> None:
    """`fail_once` 모드의 "이미 한 번 실패시켰는지" 상태를 초기화한다. 평가 하네스가
    테스트케이스 하나를 실행하기 전마다 호출해야 한다 — 안 그러면 이 dict가 모듈전역
    이라 이전 케이스에서 남은 상태가 다음 케이스로 새어들어간다(실측으로 발견된
    오염 경로)."""
    _fail_once_used.clear()


def _delay_seconds() -> float:
    return float(os.environ.get("FAULT_INJECTION_DELAY_SECONDS", "1"))


def _configured_mode(tool_name: str) -> str | None:
    raw = os.environ.get("FAULT_INJECTION")
    if not raw:
        return None
    try:
        config = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("FAULT_INJECTION 값이 JSON이 아님, 무시함: %r", raw)
        return None
    return config.get(tool_name)


def with_fault_injection(tool_name: str) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            mode = _configured_mode(tool_name)
            if mode == "fail":
                logger.info("fault_injection tool=%s mode=fail", tool_name)
                raise RuntimeError(f"{tool_name} 호출 실패(fault-injection: fail 모드)")
            if mode == "delay":
                delay = _delay_seconds()
                logger.info("fault_injection tool=%s mode=delay (%ss 대기 후 timeout)", tool_name, delay)
                time.sleep(delay)
                raise TimeoutError(f"{tool_name} 응답 지연으로 timeout(fault-injection: delay 모드)")
            if mode == "fail_once":
                if not _fail_once_used.get(tool_name):
                    _fail_once_used[tool_name] = True
                    logger.info("fault_injection tool=%s mode=fail_once (최초 1회 실패)", tool_name)
                    raise RuntimeError(f"{tool_name} 호출 실패(fault-injection: fail_once 모드, 최초 1회)")
                # 한 번 실패시킨 뒤로는 이후 호출(Tier1 재시도든 Tier2 재해석이든) 전부
                # 통과시킨다 — 예전엔 매 2회차마다 상태를 되돌리는 토글이라, 같은
                # 테스트케이스 안에서 3번째 이상 호출이 생기면(예: Tier2까지 겹칠 때)
                # 거기서 또 실패를 일으켜 "1회만 실패" 의도를 깨뜨렸다.
                logger.info("fault_injection tool=%s mode=fail_once (실제 호출 통과)", tool_name)
                return fn(*args, **kwargs)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
