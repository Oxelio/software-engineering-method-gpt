#!/usr/bin/env python3
"""Focused regression tests for the GPT deployment manifest validator."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_configuration.py"
SPEC = importlib.util.spec_from_file_location("validate_configuration", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class MethodBindingValidationTests(unittest.TestCase):
    def test_rejects_gitmodules_owned_mapping_fields(self) -> None:
        configuration = {
            "knowledge": {
                "method": {
                    "submodule": "software-engineering-method",
                    "deployment": "custom-gpt-knowledge",
                    "path": "software-engineering-method",
                    "url": "https://example.invalid/software-engineering-method.git",
                    "repository": "duplicate-owner",
                }
            }
        }
        errors: list[str] = []

        with mock.patch.object(validator, "load_gitmodules", return_value=None):
            validator.validate_method_binding(configuration, errors)

        self.assertTrue(any("path" in error for error in errors))
        self.assertTrue(any("url" in error for error in errors))
        self.assertTrue(any("repository" in error for error in errors))

    def test_rejects_unknown_method_deployment_mode(self) -> None:
        configuration = {
            "knowledge": {
                "method": {
                    "submodule": "software-engineering-method",
                    "deployment": "some-other-mode",
                }
            }
        }
        errors: list[str] = []

        with mock.patch.object(validator, "load_gitmodules", return_value=None):
            validator.validate_method_binding(configuration, errors)

        self.assertTrue(
            any("deployment must be exactly" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
