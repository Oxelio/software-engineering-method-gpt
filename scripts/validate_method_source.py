#!/usr/bin/env python3
"""Deployment-time validation for the private canonical Method submodule."""

from pathlib import Path
import configparser
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIGURATION = ROOT / "gpt" / "configuration.yaml"
GITMODULES = ROOT / ".gitmodules"


def git(*args):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def configured_method_submodule() -> str | None:
    try:
        configuration = yaml.safe_load(CONFIGURATION.read_text(encoding="utf-8"))
        submodule = configuration["knowledge"]["method"]["submodule"]
    except (OSError, TypeError, KeyError, yaml.YAMLError) as exc:
        print(f"Cannot resolve configured Method submodule: {exc}", file=sys.stderr)
        return None

    if not isinstance(submodule, str) or not submodule.strip():
        print(
            "knowledge.method.submodule must be a non-empty submodule name",
            file=sys.stderr,
        )
        return None
    return submodule.strip()


def main():
    submodule_name = configured_method_submodule()
    if submodule_name is None:
        return 1

    parser = configparser.ConfigParser()
    try:
        parser.read(GITMODULES, encoding="utf-8")
    except configparser.Error as exc:
        print(f"Cannot parse .gitmodules: {exc}", file=sys.stderr)
        return 1

    section = f'submodule "{submodule_name}"'
    if not parser.has_section(section):
        print(
            "Configured Method submodule does not resolve to a .gitmodules entry: "
            f"{submodule_name}",
            file=sys.stderr,
        )
        return 1

    path = parser.get(section, "path", fallback="").strip()
    if not path:
        print(f"{section} must define path", file=sys.stderr)
        return 1

    expected = git("ls-tree", "HEAD", "--", path)
    parts = expected.stdout.split()
    if expected.returncode or len(parts) < 3 or parts[0] != "160000":
        print("Cannot resolve pinned Method gitlink", file=sys.stderr)
        return 1
    expected_sha = parts[2]

    update = git("submodule", "update", "--init", "--checkout", "--", path)
    if update.returncode:
        print(
            "Method fetch failed: deployment validation requires read access to "
            "the private canonical Method repository.",
            file=sys.stderr,
        )
        if update.stderr.strip():
            print(update.stderr.strip(), file=sys.stderr)
        return 1

    actual = git("-C", path, "rev-parse", "HEAD")
    actual_sha = actual.stdout.strip()
    if actual.returncode or actual_sha != expected_sha:
        print(
            f"Method checkout mismatch: expected {expected_sha}, "
            f"got {actual_sha or '<unresolved>'}",
            file=sys.stderr,
        )
        return 1

    print(f"Method deployment source validation OK: {path}@{actual_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
