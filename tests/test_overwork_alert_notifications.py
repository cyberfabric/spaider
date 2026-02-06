from __future__ import annotations

from overwork_alert.notification_policy import apply_notification_policy, should_notify
from overwork_alert.models import Config, TrackerState, TrackerStatus


def test_should_notify_false_when_not_running() -> None:
    config = Config()
    state = TrackerState(status=TrackerStatus.PAUSED, active_time_seconds=999999, last_tick_at=0.0)

    assert should_notify(state=state, config=config, idle_seconds=0, now=10.0) is False


def test_should_notify_false_when_idle_unavailable() -> None:
    config = Config()
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=999999, last_tick_at=0.0)

    assert should_notify(state=state, config=config, idle_seconds=None, now=10.0) is False


def test_should_notify_false_when_idle_over_threshold() -> None:
    config = Config(idle_threshold_seconds=300)
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=999999, last_tick_at=0.0)

    assert should_notify(state=state, config=config, idle_seconds=300, now=10.0) is False


def test_should_notify_false_when_under_limit() -> None:
    config = Config(limit_seconds=100)
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=100, last_tick_at=0.0)

    assert should_notify(state=state, config=config, idle_seconds=0, now=10.0) is False


def test_should_notify_true_for_first_alert() -> None:
    config = Config(limit_seconds=100)
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=101, last_tick_at=0.0)

    assert should_notify(state=state, config=config, idle_seconds=0, now=10.0) is True


def test_should_notify_true_for_repeat_after_interval() -> None:
    config = Config(limit_seconds=100, repeat_interval_seconds=30)
    state = TrackerState(
        status=TrackerStatus.RUNNING,
        active_time_seconds=101,
        last_tick_at=0.0,
        over_limit_since=10.0,
        last_reminder_at=10.0,
    )

    assert should_notify(state=state, config=config, idle_seconds=0, now=40.0) is True


def test_apply_notification_policy_sets_over_limit_since_and_last_reminder() -> None:
    config = Config(limit_seconds=100)
    state = TrackerState(status=TrackerStatus.RUNNING, active_time_seconds=101, last_tick_at=0.0)

    out = apply_notification_policy(state=state, config=config, idle_seconds=0, now=10.0)

    assert out.over_limit_since == 10.0
    assert out.last_reminder_at == 10.0
