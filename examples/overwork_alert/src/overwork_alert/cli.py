"""CLI entrypoint for Overwork Alert."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import DEFAULT_CONFIG_PATH, load_config
from .daemon import run_daemon
from .ipc import ControlChannelError, send_request
from .launchagent import install as install_autostart
from .launchagent import uninstall as uninstall_autostart


def _add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)


def _load_socket_path(config_path: Path) -> str:
    return load_config(config_path).control_socket_path


def main(argv: list[str] | None = None) -> int:
    """Run the CLI. Returns a process exit code."""
    # @spaider-req:spd-overwork-alert-spec-cli-control-req-reset-and-controls:p1
    parser = argparse.ArgumentParser(prog="overwork-alert")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_start = sub.add_parser("start")
    _add_common_args(p_start)

    for name in ["status", "pause", "resume", "reset", "stop"]:
        p = sub.add_parser(name)
        _add_common_args(p)

    p_install = sub.add_parser("install-autostart")
    _add_common_args(p_install)

    p_uninstall = sub.add_parser("uninstall-autostart")
    _add_common_args(p_uninstall)

    args = parser.parse_args(argv)

    if args.cmd == "start":
        run_daemon(config_path=args.config)
        return 0

    if args.cmd in {"install-autostart", "uninstall-autostart"}:
        src_dir = Path(__file__).resolve().parents[1]
        try:
            if args.cmd == "install-autostart":
                # @spaider-flow:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1
                # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-run-install
                install_autostart(src_dir=src_dir)
                # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-install:p1:inst-run-install
                print("Autostart installed")
            else:
                # @spaider-flow:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1
                # @spaider-begin:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-run-uninstall
                uninstall_autostart()
                # @spaider-end:spd-overwork-alert-spec-launchagent-autostart-flow-uninstall:p1:inst-run-uninstall
                print("Autostart uninstalled")
            return 0
        except Exception as e:
            print(str(e), file=sys.stderr)
            return 2

    socket_path = _load_socket_path(args.config)

    try:
        if args.cmd == "status":
            # @spaider-flow:spd-overwork-alert-spec-cli-control-flow-status:p1
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-run-status
            payload = {"cmd": "status"}
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-run-status
        elif args.cmd == "pause":
            # @spaider-flow:spd-overwork-alert-spec-cli-control-flow-pause:p1
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-pause:p1:inst-run-pause
            payload = {"cmd": "pause"}
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-pause:p1:inst-run-pause
        elif args.cmd == "resume":
            # @spaider-flow:spd-overwork-alert-spec-cli-control-flow-resume:p1
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-resume:p1:inst-run-resume
            payload = {"cmd": "resume"}
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-resume:p1:inst-run-resume
        elif args.cmd == "reset":
            # @spaider-flow:spd-overwork-alert-spec-cli-control-flow-reset:p1
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-reset:p1:inst-run-reset
            payload = {"cmd": "reset"}
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-reset:p1:inst-run-reset
        elif args.cmd == "stop":
            # @spaider-flow:spd-overwork-alert-spec-cli-control-flow-stop:p1
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-stop:p1:inst-run-stop
            payload = {"cmd": "stop"}
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-stop:p1:inst-run-stop
        else:
            payload = {"cmd": args.cmd}

        if args.cmd == "status":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-send-status-request
            resp = send_request(socket_path=socket_path, payload=payload, timeout_seconds=2.0)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-send-status-request
        elif args.cmd == "pause":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-pause:p1:inst-send-pause-request
            resp = send_request(socket_path=socket_path, payload=payload, timeout_seconds=2.0)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-pause:p1:inst-send-pause-request
        elif args.cmd == "resume":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-resume:p1:inst-send-resume-request
            resp = send_request(socket_path=socket_path, payload=payload, timeout_seconds=2.0)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-resume:p1:inst-send-resume-request
        elif args.cmd == "reset":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-reset:p1:inst-send-reset-request
            resp = send_request(socket_path=socket_path, payload=payload, timeout_seconds=2.0)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-reset:p1:inst-send-reset-request
        elif args.cmd == "stop":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-stop:p1:inst-send-stop-request
            resp = send_request(socket_path=socket_path, payload=payload, timeout_seconds=2.0)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-stop:p1:inst-send-stop-request
        else:
            resp = send_request(socket_path=socket_path, payload=payload, timeout_seconds=2.0)
    except ControlChannelError as e:
        if args.cmd == "status":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-status-daemon-unreachable
            print(str(e), file=sys.stderr)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-status-daemon-unreachable
            return 2
        if args.cmd == "reset":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-reset:p1:inst-reset-daemon-unreachable
            print(str(e), file=sys.stderr)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-reset:p1:inst-reset-daemon-unreachable
            return 2
        if args.cmd == "pause":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-pause:p1:inst-pause-daemon-unreachable
            print(str(e), file=sys.stderr)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-pause:p1:inst-pause-daemon-unreachable
            return 2
        if args.cmd == "resume":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-resume:p1:inst-resume-daemon-unreachable
            print(str(e), file=sys.stderr)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-resume:p1:inst-resume-daemon-unreachable
            return 2
        if args.cmd == "stop":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-stop:p1:inst-stop-daemon-unreachable
            print(str(e), file=sys.stderr)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-stop:p1:inst-stop-daemon-unreachable
            return 2
        print(str(e), file=sys.stderr)
        return 2

    if not resp.get("ok"):
        if args.cmd == "status":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-status-invalid-response
            print(resp.get("error", "error"), file=sys.stderr)
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-status-invalid-response
            return 2
        print(resp.get("error", "error"), file=sys.stderr)
        return 2

    if args.cmd == "status":
        # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-print-status
        state = resp.get("state")
        print(json.dumps(state, indent=2, sort_keys=True))
        # @spaider-end:spd-overwork-alert-spec-cli-control-flow-status:p1:inst-print-status
    else:
        if args.cmd == "reset":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-reset:p1:inst-print-confirm
            print("ok")
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-reset:p1:inst-print-confirm
        elif args.cmd == "pause":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-pause:p1:inst-print-pause-confirm
            print("ok")
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-pause:p1:inst-print-pause-confirm
        elif args.cmd == "resume":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-resume:p1:inst-print-resume-confirm
            print("ok")
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-resume:p1:inst-print-resume-confirm
        elif args.cmd == "stop":
            # @spaider-begin:spd-overwork-alert-spec-cli-control-flow-stop:p1:inst-print-stop-confirm
            print("ok")
            # @spaider-end:spd-overwork-alert-spec-cli-control-flow-stop:p1:inst-print-stop-confirm
        else:
            print("ok")

    return 0
