"""Safe subprocess boundary around the active Python interpreter's pip."""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from .models import PackageUpdate, UpdateResult


class PipError(RuntimeError):
    """Raised when pip exits unsuccessfully or returns invalid output."""


class PipClient:
    """Inspect and update packages using ``sys.executable -m pip``."""

    def __init__(self, python: str | Path | None = None) -> None:
        self.python = str(python or sys.executable)

    def _run(self, arguments: Sequence[str]) -> subprocess.CompletedProcess[str]:
        command = [self.python, "-m", "pip", *arguments]
        return subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
        )

    def outdated(self) -> list[PackageUpdate]:
        """Return outdated packages reported by pip."""

        result = self._run(["list", "--outdated", "--format=json"])
        if result.returncode:
            raise PipError(result.stderr.strip() or "pip list failed")
        try:
            packages = json.loads(result.stdout)
            return [
                PackageUpdate(
                    name=item["name"],
                    current=item["version"],
                    latest=item["latest_version"],
                    package_type=item.get("latest_filetype", "wheel"),
                )
                for item in packages
            ]
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            raise PipError("pip returned an unexpected package list") from error

    def update(self, package: PackageUpdate) -> UpdateResult:
        """Attempt to update one package without invoking a shell."""

        result = self._run(["install", "--upgrade", package.name])
        message = result.stderr.strip() if result.returncode else result.stdout.strip()
        return UpdateResult(package, result.returncode == 0, message)

    def update_pip(self) -> bool:
        """Update pip itself and report whether the command succeeded."""

        return self._run(["install", "--upgrade", "pip"]).returncode == 0

    def purge_cache(self) -> bool:
        """Purge pip's download cache."""

        return self._run(["cache", "purge"]).returncode == 0
