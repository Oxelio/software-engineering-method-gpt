# Validation plan

## Static validation

Run:

```bash
python scripts/validate_openapi.py
```

The validator checks:
- YAML parsing
- OpenAPI version and required top-level keys
- unique `operationId` values
- local `$ref` targets
- `/graphql` remains an enum-based allowlist
- arbitrary GraphQL is not enabled

## Custom GPT acceptance tests

After importing the schema into the Custom GPT, test in this order.

### 1. Authentication / baseline
- `getCurrentUser`
- `getRepository` on `Oxelio/Architecture-Web`

### 2. Project discovery — read only
Resolve:
- owner: `Oxelio`
- title: `Architecture Web`

Expected known validation context:
- owner type: User
- Project number: `3`
- Project node ID: `PVT_kwHOBPzbjc4Bgts6`

The discovery flow must find the Project without supplying number `3` first.

### 3. Project fields — read only
Inspect actual field IDs/types/options/configurations. Do **not** create `Priority` or `Workflow Depth` simply because those names exist in a governance proposal.

### 4. Project items — read only
List Project items and validate Issue/PR identity plus field values.

### 5. Sub-issues — disposable test Issues only
Validate add/read/remove and verify there is no residual parent relation.

### 6. Structural Project mutations — disposable context only
Validate add/remove item, clear/set field value, and create/delete a temporary Project custom field only when explicitly authorized for a disposable test context.

## Forbidden acceptance-test shortcuts

- do not merge `Oxelio/Architecture-Web` PR #2
- do not treat that draft PR as Current Truth
- do not reconfigure Project #3 as a side effect of connector testing
- do not use a real Work destructively
