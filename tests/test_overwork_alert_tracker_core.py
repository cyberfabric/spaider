from __future__ import annotations

from overwork_alert.daemon import tick_once
from overwork_alert.models import Config, TrackerState, TrackerStatus


def test_tick_once_first_tick_sets_last_tick_only() -> None:
    config = Config(tick_interval_seconds=5, max_tick_delta_seconds=10)
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=0, last_tick_at=None)

    out = tick_once(state=state, config=config, idle_seconds=0, now=100.0)

    assert out.active_time_seconds == 0
    assert out.last_tick_at == 100.0


def test_tick_once_idle_unavailable_updates_last_tick() -> None:
    config = Config()
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=10, last_tick_at=100.0)

    out = tick_once(state=state, config=config, idle_seconds=None, now=105.0)

    assert out.active_time_seconds == 10
    assert out.last_tick_at == 105.0


def test_tick_once_idle_skips_accumulation() -> None:
    config = Config(idle_threshold_seconds=300)
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=10, last_tick_at=100.0)

    out = tick_once(state=state, config=config, idle_seconds=300, now=105.0)

    assert out.active_time_seconds == 10
    assert out.last_tick_at == 105.0


def test_tick_once_paused_skips_accumulation() -> None:
    config = Config(idle_threshold_seconds=300)
    state = TrackerState(status=TrackerStatus.PAUSED, active_time_seconds=10, last_tick_at=100.0)

    out = tick_once(state=state, config=config, idle_seconds=0, now=105.0)

    assert out.active_time_seconds == 10
    assert out.last_tick_at == 105.0


def test_tick_once_clamps_large_delta() -> None:
    config = Config(tick_interval_seconds=5, max_tick_delta_seconds=10)
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=0, last_tick_at=0.0)

    out = tick_once(state=state, config=config, idle_seconds=0, now=1000.0)

    assert out.active_time_seconds == 10
    assert out.last_tick_at == 1000.0
