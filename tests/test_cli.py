from dataclasses import dataclass, field

from pypipup.cli import main
from pypipup.models import PackageUpdate, UpdateResult


@dataclass
class FakeClient:
    packages: list[PackageUpdate]
    updated: list[str] = field(default_factory=list)
    purged: bool = False

    def outdated(self):
        return self.packages

    def update(self, package):
        self.updated.append(package.name)
        return UpdateResult(package, True)

    def update_pip(self):
        return True

    def purge_cache(self):
        self.purged = True
        return True


def test_default_is_a_read_only_preview(capsys):
    client = FakeClient([PackageUpdate("demo", "1.0", "2.0")])

    assert main([], client) == 0
    assert client.updated == []
    assert "demo" in capsys.readouterr().out


def test_apply_can_exclude_packages_and_purge(capsys):
    client = FakeClient(
        [
            PackageUpdate("keep", "1", "2"),
            PackageUpdate("skip", "1", "2"),
        ]
    )

    assert (
        main(
            ["--apply", "--yes", "--exclude", "skip", "--purge-cache"],
            client,
        )
        == 0
    )
    assert client.updated == ["keep"]
    assert client.purged is True


def test_json_output_is_machine_readable(capsys):
    client = FakeClient([PackageUpdate("demo", "1", "2")])

    assert main(["--json"], client) == 0
    assert '"latest": "2"' in capsys.readouterr().out
