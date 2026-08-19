# Repository scripts

## `validate_configuration.py`

Validates the repository-owned Custom GPT deployment manifest and the repository references it contains.

### Dependencies

```bash
python -m pip install -r requirements-dev.txt
```

### Run

From the repository root:

```bash
python scripts/validate_configuration.py
```

The validation checks repository-specific deployment invariants:

- `gpt/configuration.yaml` parses as a mapping with schema version `1`;
- runtime and GitHub Action file references resolve to repository files;
- `knowledge.method.submodule` resolves through `.gitmodules`;
- the resolved Method path is tracked as a Git gitlink (`160000`);
- the manifest does not duplicate `.gitmodules`-owned Method repository/path fields;
- GitHub Action authentication metadata has the expected basic shape.

The submodule repository/path mapping remains owned by `.gitmodules`, and the adopted Method revision remains owned by the root gitlink. This validator checks those owners; it does not duplicate their values.

## `validate_openapi.py`

Validates `actions/github/openapi.yaml` without invoking GitHub or mutating any external system.

### Dependencies

```bash
python -m pip install -r requirements-dev.txt
```

### Run

From the repository root:

```bash
python scripts/validate_openapi.py
```

The script deliberately separates two validation layers.

### Standard OpenAPI validation

`openapi-spec-validator` validates the document against the OpenAPI specification, including OpenAPI 3.1 semantics.

### Repository-specific GitHub Action invariants

Additional checks enforce constraints owned by this repository:

- exact OpenAPI version `3.1.0` for the Custom GPT Action;
- required contract sections;
- unique operation IDs;
- local `$ref` resolution;
- the bounded GraphQL query allowlist.

This distinction prevents repository-specific policy from being mistaken for generic OpenAPI compliance.

Keep this directory focused on repository-maintenance tooling. Add new scripts only when there is a concrete automated workflow to support.
