#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

from manifest_schema import check_manifest_shape

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "gpt" / "configuration.yaml"


def main():
    data = yaml.safe_load(PATH.read_text(encoding="utf-8"))
    errors = []
    check_manifest_shape(data, "", errors)
    if errors:
        print("Deployment manifest shape validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Deployment manifest shape validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
