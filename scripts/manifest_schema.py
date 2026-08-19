#!/usr/bin/env python3
"""Shared closed-schema contract for the GPT deployment manifest."""

from __future__ import annotations

from typing import Any


MANIFEST_SCHEMA: dict[str, set[str]] = {
    "": {
        "schema_version",
        "manifest_scope",
        "runtime",
        "knowledge",
        "capabilities",
        "actions",
    },
    "runtime": {"instructions", "description", "conversation_starters"},
    "knowledge": {"method"},
    "knowledge.method": {"submodule", "deployment"},
    "capabilities": {"status", "note"},
    "actions": {"github"},
    "actions.github": {"schema", "capability_model", "authentication"},
    "actions.github.authentication": {"owner", "secrets_in_repository"},
}


def check_manifest_shape(
    mapping: Any,
    path: str,
    errors: list[str],
) -> None:
    """Validate mapping types and reject fields outside the closed manifest schema."""

    label = path or "configuration"
    if not isinstance(mapping, dict):
        errors.append(f"{label} must be a mapping")
        return

    allowed = MANIFEST_SCHEMA.get(path)
    if allowed is None:
        raise ValueError(f"manifest schema does not define path: {path}")

    unknown = sorted(set(mapping) - allowed)
    if unknown:
        errors.append(
            f"{label} contains unsupported fields: {', '.join(unknown)}"
        )

    for key, value in mapping.items():
        child = f"{path}.{key}" if path else key
        if child in MANIFEST_SCHEMA:
            check_manifest_shape(value, child, errors)
