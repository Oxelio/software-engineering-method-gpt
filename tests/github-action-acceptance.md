# GitHub Action Acceptance Test Plan

This plan validates the GitHub Tool Capability exposed to the **Software Engineering Method** GPT.

It validates technical behavior only. It must not change consuming-project governance, adopt draft policy, or mutate real project Work merely to prove that a capability exists.

## 1. Static validation

Run from the repository root:

```bash
python scripts/validate_openapi.py
```

The validator reports two separate result groups:

- standard OpenAPI validation;
- repository-specific GitHub Action invariants.

The repository-specific checks enforce the exact Action contract requirements, including the bounded GraphQL allowlist. They are not presented as generic OpenAPI rules.

## 2. Temporary acceptance fixture

Acceptance testing currently uses `tests/fixtures/architecture-web.yaml` as a **temporary test fixture**.

The values in that file identify a convenient live read-only validation context. They are not Software Engineering Method rules, GPT configuration defaults, or reusable project-governance requirements.

If the fixture no longer matches Current Truth, update or replace the fixture. Never force the live project back to fixture values merely to make a test pass.

## 3. Custom GPT acceptance tests

After importing `actions/github/openapi.yaml` into the Software Engineering Method GPT, test in the following order.

### 3.1 Authentication / baseline

- `getCurrentUser`;
- `getRepository` using the repository identified by the temporary fixture.

### 3.2 Project discovery — read only

Resolve the fixture Project by owner and title rather than by hard-coding its number as the discovery mechanism.

Project number and node ID in the fixture are validation expectations only. They may be used to verify discovery results after the Project is resolved by authoritative identifiers.

### 3.3 Project fields — read only

Inspect actual field IDs, types, options, and configurations.

Do **not** create `Priority`, `Workflow Depth`, or any other field merely because a draft governance proposal mentions it.

### 3.4 Project items — read only

List Project items and validate Issue/PR identity plus field values.

### 3.5 Sub-issues — disposable test Issues only

Validate add/read/remove using disposable Issues and verify that the test leaves no residual parent relation.

### 3.6 Structural Project mutations — disposable context only

Validate add/remove item, clear/set field value, and create/delete a temporary Project custom field only when the operation is explicitly authorized for a disposable test context.

## 4. Forbidden acceptance-test shortcuts

- do not mutate a resource marked as forbidden in the temporary fixture;
- do not treat fixture-linked draft proposals as Current Truth;
- do not reconfigure the fixture Project as a side effect of connector testing;
- do not use real Work destructively;
- do not interpret the presence of an OpenAPI mutation as permission to invoke it;
- do not bypass the bounded GraphQL allowlist to test an unsupported operation.

## 5. Acceptance result

Record separately:

- capability verified;
- capability unavailable or defective;
- test blocked by missing Operational Permission;
- test blocked by insufficient Role Authority;
- test intentionally not executed because no disposable context was available.

This separation prevents an authorization limitation from being misreported as a technical API failure, and prevents technical availability from being misreported as authorization.
