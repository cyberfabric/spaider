from __future__ import annotations

import plistlib
from pathlib import Path

from overwork_alert.launchagent import build_plist_bytes


def test_build_plist_bytes_contains_expected_fields(tmp_path: Path) -> None:
    payload = plistlib.loads(build_plist_bytes(label="com.example.test", src_dir=tmp_path))

    assert payload["Label"] == "com.example.test"
    assert payload["RunAtLoad"] is True
    assert payload["KeepAlive"] is True
    assert "ProgramArguments" in payload
    assert payload["ProgramArguments"][1:3] == ["-m", "overwork_alert"]
    assert payload["EnvironmentVariables"]["PYTHONPATH"] == str(tmp_path)
