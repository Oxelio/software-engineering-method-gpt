#!/usr/bin/env python3
"""Validate the repository-owned Custom GPT deployment-input manifest."""

from __future__ import annotations

import configparser
from pathlib import Path
import subprocess
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:
    print(
        "Missing development dependency. "
        "Install dependencies with `python -m pip install -r requirements-dev.txt`.",
        file=sys.stderr,
    )
    print(f"Import error: {exc}", file=sys.stderr)
    raise SystemExit(2)

from manifest_schema import check_manifest_shape


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CONFIGURATION_PATH = REPOSITORY_ROOT / "gpt" / "configuration.yaml"
GITMODULES_PATH = REPOSITORY_ROOT / ".gitmodules"

EXPECTED_SCHEMA_VERSION = 1
EXPECTED_MANIFEST_SCOPE = "version-controlled-deployment-inputs"
EXPECTED_METHOD_DEPLOYMENT = "custom-gpt-knowledge"


def load_mapping(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{label} root must be a mapping")
    return data


def mapping_at(
    parent: dict[str, Any],
    key: str,
    field: str,
    errors: list[str],
) -> dict[str, Any] | None:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{field} must be a mapping")
        return None
    return value


def repository_file_reference(
    value: Any,
    field: str,
    errors: list[str],
) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty repository-relative path")
        return None

    relative_path = Path(value)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        errors.append(f"{field} must stay within the repository: {value}")
        return None

    target = REPOSITORY_ROOT / relative_path
    if not target.is_file():
        errors.append(f"{field} does not reference a file: {value}")
        return None

    return target


def validate_runtime(configuration: dict[str, Any], errors: list[str]) -> int:
    runtime = mapping_at(configuration, "runtime", "runtime", errors)
    if runtime is None:
        return 0

    count = 0
    for key in ("instructions", "description", "conversation_starters"):
        if repository_file_reference(runtime.get(key), f"runtime.{key}", errors):
            count += 1
    return count


def load_gitmodules(errors: list[str]) -> configparser.ConfigParser | None:
    if not GITMODULES_PATH.is_file():
        errors.append(f".gitmodules not found: {GITMODULES_PATH}")
        return None

    parser = configparser.ConfigParser()
    try:
        parser.read(GITMODULES_PATH, encoding="utf-8")
    except configparser.Error as exc:
        errors.append(f"cannot parse .gitmodules: {exc}")
        return None
    return parser


def validate_gitlink(path: str, errors: list[str]) -> None:
    result = subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), "ls-files", "--stage", "--", path],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "git ls-files failed"
        errors.append(f"cannot inspect Method gitlink at {path}: {detail}")
        return

    entries = [line for line in result.stdout.splitlines() if line.strip()]
    if len(entries) != 1:
        errors.append(f"Method submodule path is not a unique tracked gitlink: {path}")
        return

    parts = entries[0].split(maxsplit=3)
    if len(parts) != 4:
        errors.append(f"cannot parse git index entry for Method submodule: {entries[0]}")
        return

    mode, object_id, stage, tracked_path = parts
    if mode != "160000":
        errors.append(
            f"Method submodule path must be tracked as a gitlink (mode 160000): {path}"
        )
    if stage != "0":
        errors.append(f"Method submodule path must have a stage-0 gitlink entry: {path}")
    if tracked_path != path:
        errors.append(
            f"Method gitlink path mismatch: expected {path}, git index reports {tracked_path}"
        )
    if len(object_id) != 40:
        errors.append(f"Method gitlink object id is not a full commit id: {object_id}")


def validate_method_binding(
    configuration: dict[str, Any],
    errors: list[str],
) -> str | None:
    knowledge = mapping_at(configuration, "knowledge", "knowledge", errors)
    if knowledge is None:
        return None

    method = mapping_at(knowledge, "method", "knowledge.method", errors)
    if method is None:
        return None

    check_manifest_shape(method, "knowledge.method", errors)

    submodule_name = method.get("submodule")
    if not isinstance(submodule_name, str) or not submodule_name.strip():
        errors.append("knowledge.method.submodule must be a non-empty submodule name")
        return None

    deployment = method.get("deployment")
    if deployment != EXPECTED_METHOD_DEPLOYMENT:
        errors.append(
            "knowledge.method.deployment must be exactly "
            f"{EXPECTED_METHOD_DEPLOYMENT!r}; it means the pinned Method content is "
            "supplied to the Custom GPT through the platform Knowledge mechanism"
        )

    parser = load_gitmodules(errors)
    if parser is None:
        return submodule_name

    section = f'submodule "{submodule_name}"'
    if not parser.has_section(section):
        errors.append(
            "knowledge.method.submodule does not resolve to a .gitmodules entry: "
            f"{submodule_name}"
        )
        return submodule_name

    path = parser.get(section, "path", fallback="").strip()
    repository = parser.get(section, "url", fallback="").strip()
    if not path:
        errors.append(f"{section} must define path")
    if not repository:
        errors.append(f"{section} must define url")
    if path:
        validate_gitlink(path, errors)

    return submodule_name


def validate_capabilities(configuration: dict[str, Any], errors: list[str]) -> None:
    capabilities = mapping_at(configuration, "capabilities", "capabilities", errors)
    if capabilities is None:
        return

    status = capabilities.get("status")
    if status != "unspecified":
        errors.append(
            "capabilities.status must remain 'unspecified' until an authoritative "
            "repository source defines platform capability flags"
        )

    note = capabilities.get("note")
    if not isinstance(note, str) or not note.strip():
        errors.append("capabilities.note must explain why platform flags are unspecified")


def validate_actions(configuration: dict[str, Any], errors: list[str]) -> int:
    actions = mapping_at(configuration, "actions", "actions", errors)
    if actions is None:
        return 0

    github = mapping_at(actions, "github", "actions.github", errors)
    if github is None:
        return 0

    count = 0
    for key in ("schema", "capability_model"):
        if repository_file_reference(github.get(key), f"actions.github.{key}", errors):
            count += 1

    authentication = mapping_at(
        github,
        "authentication",
        "actions.github.authentication",
        errors,
    )
    if authentication is not None:
        if authentication.get("owner") != "external":
            errors.append(
                "actions.github.authentication.owner must be exactly 'external'"
            )
        if authentication.get("secrets_in_repository") is not False:
            errors.append(
                "actions.github.authentication.secrets_in_repository must be false"
            )

    return count


def print_errors(errors: list[str]) -> None:
    if not errors:
        return

    print("GPT configuration validation FAILED")
    for error in errors:
        print(f"- {error}")


def main() -> int:
    errors: list[str] = []

    try:
        configuration = load_mapping(CONFIGURATION_PATH, "GPT configuration")
    except (FileNotFoundError, ValueError, yaml.YAMLError) as exc:
        print("GPT configuration validation FAILED")
        print(f"- {exc}")
        return 1

    check_manifest_shape(configuration, "", errors)

    if configuration.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        errors.append(f"schema_version must be exactly {EXPECTED_SCHEMA_VERSION}")

    if configuration.get("manifest_scope") != EXPECTED_MANIFEST_SCOPE:
        errors.append(
            "manifest_scope must be exactly "
            f"{EXPECTED_MANIFEST_SCOPE!r}; this manifest intentionally represents "
            "only version-controlled deployment inputs, not a complete platform export"
        )

    file_reference_count = validate_runtime(configuration, errors)
    method_submodule = validate_method_binding(configuration, errors)
    validate_capabilities(configuration, errors)
    file_reference_count += validate_actions(configuration, errors)

    if errors:
        print_errors(errors)
        return 1

    print(
        "GPT configuration validation OK: "
        f"{file_reference_count} file references, "
        f"Method submodule {method_submodule!r}, "
        f"scope {EXPECTED_MANIFEST_SCOPE!r}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
