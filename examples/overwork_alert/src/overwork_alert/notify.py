"""macOS Notification Center integration via `osascript` (best-effort)."""

from __future__ import annotations

import logging
import subprocess

logger = logging.getLogger(__name__)


def _applescript_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def send_notification(*, title: str, message: str) -> bool:
    """Send a macOS notification. Returns True on success."""
    script = f"display notification {_applescript_quote(message)} with title {_applescript_quote(title)}"
    try:
        proc = subprocess.run(
            ["osascript", "-e", script],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        logger.warning("Failed to invoke osascript", exc_info=True)
        return False

    return proc.returncode == 0
