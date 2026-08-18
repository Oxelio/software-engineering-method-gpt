# Repository scripts

## `validate_openapi.py`

Validates `actions/github/openapi.yaml` without invoking GitHub.

### Dependency

```bash
python -m pip install -r requirements-dev.txt
```

### Run

From the repository root:

```bash
python scripts/validate_openapi.py
```

The script validates:

- YAML parsing;
- OpenAPI `3.1.0`;
- required top-level sections;
- unique operation IDs;
- local `$ref` resolution;
- the bounded GraphQL query allowlist.

Keep this directory focused on repository-maintenance tooling. Add new scripts only when there is a concrete automated workflow to support.
