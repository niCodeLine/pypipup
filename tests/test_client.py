import subprocess
from unittest.mock import patch

import pytest

from pypipup import PackageUpdate, PipClient, PipError


@patch("pypipup.client.subprocess.run")
def test_outdated_uses_the_current_interpreter_without_a_shell(run):
    run.return_value = subprocess.CompletedProcess(
        [],
        0,
        '[{"name":"demo","version":"1.0","latest_version":"2.0"}]',
        "",
    )
    client = PipClient("/path/to/python")

    assert client.outdated() == [PackageUpdate("demo", "1.0", "2.0")]
    command = run.call_args.args[0]
    assert command == [
        "/path/to/python",
        "-m",
        "pip",
        "list",
        "--outdated",
        "--format=json",
    ]
    assert run.call_args.kwargs["check"] is False


@patch("pypipup.client.subprocess.run")
def test_invalid_output_becomes_a_clear_domain_error(run):
    run.return_value = subprocess.CompletedProcess([], 0, "not-json", "")

    with pytest.raises(PipError, match="unexpected"):
        PipClient().outdated()


@patch("pypipup.client.subprocess.run")
def test_update_reports_failure_without_raising(run):
    run.return_value = subprocess.CompletedProcess([], 1, "", "network unavailable")

    result = PipClient().update(PackageUpdate("demo", "1", "2"))

    assert result.succeeded is False
    assert result.message == "network unavailable"
