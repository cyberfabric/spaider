"""Domain models for the Overwork Alert tool."""

from __future__ import annotations

import dataclasses
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
from typing import Any


class TrackerStatus(str, Enum):
    """Tracker runtime status."""

    RUNNING = "running"
    PAUSED = "paused"


@dataclass(frozen=True)
class Config:
    """Effective configuration used by the daemon and CLI."""

    limit_seconds: int = 10800
    idle_threshold_seconds: int = 300
    repeat_interval_seconds: int = 1800
    tick_interval_seconds: int = 5
    max_tick_delta_seconds: int = 10
    control_socket_path: str = "/tmp/overwork-alert.sock"


@dataclass
class TrackerState:
    """In-memory daemon session state."""

    status: TrackerStatus = TrackerStatus.RUNNING
    active_time_seconds: int = 0
    last_tick_at: float | None = None
    over_limit_since: float | None = None
    last_reminder_at: float | None = None

    def to_dict(self, *, config: Config) -> dict[str, Any]:
        """Serialize minimal status payload for CLI responses."""

        def _ts(ts: float | None) -> str:
            if ts is None:
                return ""
            return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()

        return {
            "status": self.status.value,
            "active_time_seconds": int(self.active_time_seconds),
            "limit_seconds": int(config.limit_seconds),
            "over_limit_since": _ts(self.over_limit_since),
            "last_reminder_at": _ts(self.last_reminder_at),
        }


def clone_state(state: TrackerState) -> TrackerState:
    """Return a shallow copy of a tracker state."""
    return dataclasses.replace(state)
