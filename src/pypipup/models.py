"""Value objects used by pypipup."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PackageUpdate:
    """An available package update reported by pip."""

    name: str
    current: str
    latest: str
    package_type: str = "wheel"


@dataclass(frozen=True)
class UpdateResult:
    """The result of one attempted package update."""

    package: PackageUpdate
    succeeded: bool
    message: str = ""
