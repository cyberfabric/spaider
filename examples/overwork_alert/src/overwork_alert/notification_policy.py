"""Pure notification decision logic.

This module does not perform OS notification delivery; it only decides when to notify
and updates in-memory scheduling state.
"""

from __future__ import annotations

import time
from dataclasses import replace

from .models import Config, TrackerState, TrackerStatus


# @spaider-algo:spd-overwork-alert-spec-notifications-algo-should-notify:p1
def should_notify(*, state: TrackerState, config: Config, idle_seconds: int | None, now: float) -> bool:
    """Return True if a notification should be delivered now."""
    # @spaider-begin:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-not-running
    if state.status != TrackerStatus.RUNNING:
        return False
    # @spaider-end:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-not-running

    # @spaider-begin:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-currently-idle
    if idle_seconds is None:
        return False

    if idle_seconds >= config.idle_threshold_seconds:
        return False
    # @spaider-end:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-currently-idle

    # @spaider-begin:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-not-over-limit
    if state.active_time_seconds <= config.limit_seconds:
        return False
    # @spaider-end:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-not-over-limit

    # @spaider-begin:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-first-alert
    if state.over_limit_since is None:
        return True
    # @spaider-end:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-first-alert

    if state.last_reminder_at is None:
        return True

    # @spaider-begin:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-repeat-alert
    if (now - state.last_reminder_at) >= config.repeat_interval_seconds:
        return True
    # @spaider-end:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-repeat-alert

    # @spaider-begin:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-default-no
    return False
    # @spaider-end:spd-overwork-alert-spec-notifications-algo-should-notify:p1:inst-default-no


# @spaider-req:spd-overwork-alert-spec-notifications-req-alert-and-repeat:p1
def apply_notification_policy(
    *,
    state: TrackerState,
    config: Config,
    idle_seconds: int | None,
    now: float | None = None,
) -> TrackerState:
    """Update notification scheduling state after a notification is delivered."""
    # @spaider-state:spd-overwork-alert-spec-notifications-state-over-limit:p1
    n = time.time() if now is None else now

    if not should_notify(state=state, config=config, idle_seconds=idle_seconds, now=n):
        return state

    if state.over_limit_since is None:
        # @spaider-begin:spd-overwork-alert-spec-notifications-state-over-limit:p1:inst-transition-first
        return replace(state, over_limit_since=n, last_reminder_at=n)
        # @spaider-end:spd-overwork-alert-spec-notifications-state-over-limit:p1:inst-transition-first

    # @spaider-begin:spd-overwork-alert-spec-notifications-state-over-limit:p1:inst-transition-remind
    return replace(state, last_reminder_at=n)
    # @spaider-end:spd-overwork-alert-spec-notifications-state-over-limit:p1:inst-transition-remind
