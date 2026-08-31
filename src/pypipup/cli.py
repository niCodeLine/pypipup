"""Command-line interface for pypipup."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from .client import PipClient, PipError
from .models import PackageUpdate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pypipup",
        description="Review outdated packages before updating them.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="install available updates (the default is a read-only preview)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="skip the confirmation prompt; only valid with --apply",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PACKAGE",
        help="exclude a package; may be passed more than once",
    )
    parser.add_argument(
        "--update-pip",
        action="store_true",
        help="update pip itself before checking packages",
    )
    parser.add_argument(
        "--purge-cache",
        action="store_true",
        help="purge pip's cache after successful updates",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the preview as JSON (cannot be combined with --apply)",
    )
    return parser


def _selected(
    packages: Sequence[PackageUpdate], excluded: Sequence[str]
) -> list[PackageUpdate]:
    ignored = {name.casefold() for name in excluded}
    return [package for package in packages if package.name.casefold() not in ignored]


def _print_preview(packages: Sequence[PackageUpdate]) -> None:
    if not packages:
        print("Everything is up to date.")
        return
    width = max(len(package.name) for package in packages)
    print(f"{len(packages)} update(s) available:\n")
    for package in packages:
        print(f"  {package.name:<{width}}  {package.current} → {package.latest}")


def main(argv: Sequence[str] | None = None, client: PipClient | None = None) -> int:
    """Run the CLI and return a process exit code."""

    parser = build_parser()
    args = parser.parse_args(argv)
    if args.yes and not args.apply:
        parser.error("--yes requires --apply")
    if args.json and args.apply:
        parser.error("--json cannot be combined with --apply")

    pip = client or PipClient()
    try:
        if args.update_pip and not pip.update_pip():
            print("Could not update pip.")
            return 1
        packages = _selected(pip.outdated(), args.exclude)
    except PipError as error:
        print(f"Could not inspect this environment: {error}")
        return 1

    if args.json:
        print(
            json.dumps(
                [
                    {
                        "name": package.name,
                        "current": package.current,
                        "latest": package.latest,
                    }
                    for package in packages
                ],
                indent=2,
            )
        )
        return 0

    _print_preview(packages)
    if not args.apply or not packages:
        return 0

    if not args.yes:
        answer = input("\nApply these updates? [y/N] ").strip().casefold()
        if answer not in {"y", "yes"}:
            print("No changes made.")
            return 0

    results = [pip.update(package) for package in packages]
    succeeded = sum(result.succeeded for result in results)
    failed = [result.package.name for result in results if not result.succeeded]
    print(f"\nUpdated {succeeded}/{len(results)} packages.")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    if args.purge_cache and not failed and not pip.purge_cache():
        print("Updates succeeded, but pip's cache could not be purged.")
        return 1
    return 1 if failed else 0
