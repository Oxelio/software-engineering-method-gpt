# GitHub Action Acceptance Test Plan

This plan validates the GitHub Tool Capability exposed to the **Software Engineering Method** GPT.

It validates technical behavior only. It must not change Architecture Web governance, adopt draft policy, or mutate real project Work merely to prove that a capability exists.

## 1. Static validation

Run from the repository root:

```bash
python scripts/validate_openapi.py
```

The validator checks:

- YAML parsing;
- OpenAPI version and required top-level keys;
- unique `operationId` values;
- local `$ref` targets;
- `/graphql` remains an enum-based exact-operation allowlist;
- arbitrary GraphQL is not enabled.

## 2. Custom GPT acceptance tests

After importing `actions/github/openapi.yaml` into the Software Engineering Method GPT, test in the following order.

### 2.1 Authentication / baseline

- `getCurrentUser`;
- `getRepository` on `Oxelio/Architecture-Web`.

### 2.2 Project discovery — read only

Resolve the Architecture Web Project by owner and title rather than by hard-coding its number as the discovery mechanism.

Known validation context at the time this plan was authored:

- owner: `Oxelio`;
- title: `Architecture Web`;
- owner type: User;
- Project number: `3`;
- Project node ID: `PVT_kwHOBPzbjc4Bgts6`.

Treat these values as validation expectations, not as generic Method configuration. If Current Truth has changed, update the test fixture rather than forcing the live Project back to these values.

### 2.3 Project fields — read only

Inspect actual field IDs, types, options, and configurations.

Do **not** create `Priority`, `Workflow Depth`, or any other field merely because a draft governance proposal mentions it.

### 2.4 Project items — read only

List Project items and validate Issue/PR identity plus field values.

### 2.5 Sub-issues — disposable test Issues only

Validate add/read/remove using disposable Issues and verify that the test leaves no residual parent relation.

### 2.6 Structural Project mutations — disposable context only

Validate add/remove item, clear/set field value, and create/delete a temporary Project custom field only when the operation is explicitly authorized for a disposable test context.

## 3. Forbidden acceptance-test shortcuts

- do not merge `Oxelio/Architecture-Web` PR #2;
- do not treat that draft PR as Current Truth;
- do not reconfigure the Architecture Web Project as a side effect of connector testing;
- do not use a real Work destructively;
- do not interpret the presence of an OpenAPI mutation as permission to invoke it;
- do not bypass the bounded GraphQL allowlist to test an unsupported operation.

## 4. Acceptance result

Record separately:

- capability verified;
- capability unavailable or defective;
- test blocked by missing Operational Permission;
- test blocked by insufficient Role Authority;
- test intentionally not executed because no disposable context was available.

This separation prevents an authorization limitation from being misreported as a technical API failure, and prevents technical availability from being misreported as authorization.
