"""macOS idle time sampling via `ioreg` (best-effort)."""

from __future__ import annotations

import logging
import re
import subprocess

logger = logging.getLogger(__name__)

_IDLE_RE = re.compile(r"\"HIDIdleTime\"\s*=\s*(\d+)")


def get_idle_seconds() -> int | None:
    """Return current idle seconds, or None if the sample is unavailable."""
    try:
        proc = subprocess.run(
            ["ioreg", "-c", "IOHIDSystem"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError:
        logger.warning("Failed to invoke ioreg", exc_info=True)
        return None

    if proc.returncode != 0:
        logger.warning("ioreg returned non-zero exit code: %s", proc.returncode)
        return None

    m = _IDLE_RE.search(proc.stdout)
    if not m:
        return None

    try:
        idle_ns = int(m.group(1))
    except ValueError:
        return None

    return idle_ns // 1_000_000_000
