"""LaunchAgent install/uninstall for Overwork Alert (user-level only)."""

from __future__ import annotations

import plistlib
import subprocess
import sys
from pathlib import Path

from .config import DEFAULT_CONFIG_PATH


# @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-choose-label
DEFAULT_LABEL = "com.spaider.overwork-alert"
# @spaider-end:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-choose-label


def get_launchagent_plist_path(label: str = DEFAULT_LABEL) -> Path:
    """Return the expected LaunchAgent plist path for the given label."""
    return Path.home() / "Library" / "LaunchAgents" / f"{label}.plist"


# @spaider-algo:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1
def build_plist_bytes(*, label: str, src_dir: Path) -> bytes:
    """Build plist content for the user LaunchAgent."""
    env = {"PYTHONPATH": str(src_dir)}

    # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-set-args
    program_args = [
        sys.executable,
        "-m",
        "overwork_alert",
        "start",
        "--config",
        str(DEFAULT_CONFIG_PATH),
    ]
    # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-set-args

    payload = {
        "Label": label,
        "ProgramArguments": program_args,
        # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-set-options
        "RunAtLoad": True,
        "KeepAlive": True,
        # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-set-options
        # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-set-throttle
        "ThrottleInterval": 10,
        # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-set-throttle
        "EnvironmentVariables": env,
        "StandardOutPath": str(Path.home() / "Library" / "Logs" / "overwork-alert.log"),
        "StandardErrorPath": str(Path.home() / "Library" / "Logs" / "overwork-alert.err.log"),
    }

    # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-return-plist
    return plistlib.dumps(payload)
    # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-algo-build-plist:p1:inst-return-plist


def _launchctl(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["launchctl", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


# @spaider-flow:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1
def install(*, src_dir: Path, label: str = DEFAULT_LABEL) -> None:
    """Install (or update) the LaunchAgent plist and load it via launchctl."""
    # @spaider-req:spd-overwork-alert-spec-launchagent-autostart-req-install-and-run:p1
    # @spaider-state:spd-overwork-alert-spec-launchagent-autostart-state-installation:p1
    plist_path = get_launchagent_plist_path(label)
    plist_path.parent.mkdir(parents=True, exist_ok=True)

    # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-build-plist
    desired = build_plist_bytes(label=label, src_dir=src_dir)
    # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-build-plist

    # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-install-idempotent
    if plist_path.exists():
        try:
            existing = plist_path.read_bytes()
        except OSError:
            existing = b""
        should_write = existing != desired
    else:
        should_write = True
    # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-install-idempotent

    if should_write:
        try:
            # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-write-plist
            plist_path.write_bytes(desired)
            # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-write-plist
        except OSError as e:
            # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-write-plist-error
            raise RuntimeError("Failed to write plist") from e
            # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-write-plist-error

    _launchctl("unload", str(plist_path))

    # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-launchctl-load
    proc = _launchctl("load", str(plist_path))
    # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-launchctl-load
    if proc.returncode != 0:
        # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-launchctl-load-error
        raise RuntimeError(f"launchctl load failed: {proc.stderr.strip()}")
        # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-launchctl-load-error

    # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-state-installation:p1:inst-transition-installed
    return
    # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-state-installation:p1:inst-transition-installed


# @spaider-flow:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1
def uninstall(*, label: str = DEFAULT_LABEL) -> None:
    """Unload and remove the user LaunchAgent plist (idempotent)."""
    plist_path = get_launchagent_plist_path(label)

    if not plist_path.exists():
        # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-uninstall-idempotent
        return
        # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-uninstall-idempotent

    # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-launchctl-unload
    proc = _launchctl("unload", str(plist_path))
    # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-launchctl-unload
    if proc.returncode != 0:
        # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-launchctl-unload-warn
        pass
        # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-launchctl-unload-warn

    try:
        # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-delete-plist
        plist_path.unlink()
        # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-delete-plist
    except OSError as e:
        # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-delete-plist-error
        raise RuntimeError("Failed to delete plist") from e
        # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-delete-plist-error

    # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-state-installation:p1:inst-transition-removed
    return
    # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-state-installation:p1:inst-transition-removed
