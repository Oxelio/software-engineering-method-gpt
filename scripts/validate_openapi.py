#!/usr/bin/env python3
"""Validate the GitHub Action OpenAPI contract and repository invariants."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

try:
    import yaml
    from openapi_spec_validator import validate as validate_openapi_spec
except ImportError as exc:
    print(
        "Missing development dependency. "
        "Install dependencies with `python -m pip install -r requirements-dev.txt`.",
        file=sys.stderr,
    )
    print(f"Import error: {exc}", file=sys.stderr)
    raise SystemExit(2)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OPENAPI_PATH = REPOSITORY_ROOT / "actions" / "github" / "openapi.yaml"
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}


def load_spec(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"OpenAPI contract not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("OpenAPI document root must be a mapping")
    return data


def validate_standard_openapi(spec: dict[str, Any], errors: list[str]) -> None:
    """Validate the document against the OpenAPI specification."""

    try:
        validate_openapi_spec(spec)
    except Exception as exc:  # validator exposes version-specific exception types
        errors.append(str(exc))


def validate_contract_shape(spec: dict[str, Any], errors: list[str]) -> None:
    """Validate repository-owned contract requirements beyond generic OpenAPI."""

    if spec.get("openapi") != "3.1.0":
        errors.append("openapi must be exactly 3.1.0 for the Custom GPT Action")

    for key in ("info", "servers", "paths", "components"):
        if key not in spec:
            errors.append(f"missing required repository contract key: {key}")


def validate_operation_ids(spec: dict[str, Any], errors: list[str]) -> int:
    operation_ids: list[str] = []

    for path, item in spec.get("paths", {}).items():
        if not isinstance(item, dict):
            continue

        for method, operation in item.items():
            if method.lower() not in HTTP_METHODS:
                continue
            if not isinstance(operation, dict):
                errors.append(f"invalid operation object: {method.upper()} {path}")
                continue

            operation_id = operation.get("operationId")
            if not operation_id:
                errors.append(f"missing operationId: {method.upper()} {path}")
            else:
                operation_ids.append(operation_id)

    if len(operation_ids) != len(set(operation_ids)):
        errors.append("operationId values are not unique")

    return len(operation_ids)


def resolve_local_ref(spec: dict[str, Any], ref: str) -> bool:
    if not ref.startswith("#/"):
        return True

    current: Any = spec
    try:
        for part in ref[2:].split("/"):
            decoded = part.replace("~1", "/").replace("~0", "~")
            current = current[decoded]
    except (KeyError, TypeError):
        return False

    return True


def validate_refs(spec: dict[str, Any], errors: list[str]) -> None:
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            ref = value.get("$ref")
            if isinstance(ref, str) and not resolve_local_ref(spec, ref):
                errors.append(f"unresolved local ref: {ref}")
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(spec)


def validate_graphql_allowlist(spec: dict[str, Any], errors: list[str]) -> int:
    try:
        graphql_post = spec["paths"]["/graphql"]["post"]
        request_ref = graphql_post["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        request_schema_name = request_ref.split("/")[-1]
        request_schema = spec["components"]["schemas"][request_schema_name]
        query_schema = request_schema["properties"]["query"]
        allowlist = query_schema.get("enum", [])
    except (KeyError, TypeError, AttributeError) as exc:
        errors.append(f"cannot validate GraphQL allowlist: {exc}")
        return 0

    if not allowlist:
        errors.append("GraphQL query must remain a non-empty enum allowlist")
        return 0

    for query in allowlist:
        if not isinstance(query, str) or not (
            query.startswith("query(") or query.startswith("mutation(")
        ):
            errors.append("invalid GraphQL allowlist entry")
            break

    return len(allowlist)


def print_error_group(title: str, errors: list[str]) -> None:
    if not errors:
        return

    print(f"{title}:")
    for error in errors:
        print(f"- {error}")


def main() -> int:
    standard_errors: list[str] = []
    invariant_errors: list[str] = []

    try:
        spec = load_spec(OPENAPI_PATH)
    except (FileNotFoundError, ValueError, yaml.YAMLError) as exc:
        print("OpenAPI validation FAILED")
        print("Document loading:")
        print(f"- {exc}")
        return 1

    validate_standard_openapi(spec, standard_errors)

    validate_contract_shape(spec, invariant_errors)
    operation_count = validate_operation_ids(spec, invariant_errors)
    validate_refs(spec, invariant_errors)
    graphql_operation_count = validate_graphql_allowlist(spec, invariant_errors)

    if standard_errors or invariant_errors:
        print("OpenAPI validation FAILED")
        print_error_group("Standard OpenAPI validation", standard_errors)
        print_error_group("Repository-specific GitHub Action invariants", invariant_errors)
        return 1

    print("Standard OpenAPI validation OK")
    print(
        "Repository-specific GitHub Action invariants OK: "
        f"{operation_count} operations, "
        f"{graphql_operation_count} allowlisted GraphQL operations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
