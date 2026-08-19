#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from manifest_schema import check_manifest_shape


class ManifestShapeTests(unittest.TestCase):
    def test_rejects_nested_capability_flag(self):
        data = {
            "schema_version": 1,
            "manifest_scope": "version-controlled-deployment-inputs",
            "runtime": {
                "instructions": "gpt/instructions.md",
                "description": "gpt/description.md",
                "conversation_starters": "gpt/conversation-starters.md",
            },
            "knowledge": {
                "method": {
                    "submodule": "software-engineering-method",
                    "deployment": "custom-gpt-knowledge",
                }
            },
            "capabilities": {
                "status": "unspecified",
                "note": "external",
                "web_search": True,
            },
            "actions": {
                "github": {
                    "schema": "actions/github/openapi.yaml",
                    "capability_model": "actions/github/capabilities.md",
                    "authentication": {
                        "owner": "external",
                        "secrets_in_repository": False,
                    },
                }
            },
        }
        errors = []
        check_manifest_shape(data, "", errors)
        self.assertTrue(
            any("capabilities" in error and "web_search" in error for error in errors)
        )

    def test_rejects_nested_authentication_field(self):
        errors = []
        check_manifest_shape(
            {"owner": "external", "secrets_in_repository": False, "token": "x"},
            "actions.github.authentication",
            errors,
        )
        self.assertTrue(any("token" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
