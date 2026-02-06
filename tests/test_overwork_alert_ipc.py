from __future__ import annotations

import os
import tempfile
import time

from overwork_alert.ipc import ControlRequest, ControlServer, send_request


def test_ipc_request_response_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as td:
        socket_path = os.path.join(td, "overwork.sock")

        def handler(req: ControlRequest) -> dict:
            if req.cmd == "status":
                return {"ok": True, "state": {"status": "running"}}
            return {"ok": False, "error": "invalid_command"}

        server = ControlServer(socket_path=socket_path, request_handler=handler)
        server.start()
        try:
            # Give the server thread a moment to start.
            time.sleep(0.05)
            resp = send_request(socket_path=socket_path, payload={"cmd": "status"}, timeout_seconds=1.0)
            assert resp["ok"] is True
            assert resp["state"]["status"] == "running"
        finally:
            server.stop()
