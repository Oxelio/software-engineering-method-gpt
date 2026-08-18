# GitHub Action

This directory defines the bounded GitHub **Tool Capability** exposed to the Software Engineering Method GPT.

It owns technical API primitives. It does not own Method policy, project governance, Operational Permission, or Role Authority.

> **Tool Capability != Operational Permission != Role Authority**

## Files

- `openapi.yaml` — OpenAPI 3.1 contract imported by the Custom GPT Action.
- `capabilities.md` — capability model, scope, and deliberate exclusions.
- `../../tests/github-action-acceptance.md` — non-destructive acceptance-test plan.

## Contract

Current contract version: **2.1.0**.

The contract uses GitHub REST endpoints plus a bounded `/graphql` operation whose query value is restricted to an explicit allowlist of exact Projects v2 operations.

It intentionally does not expose arbitrary GraphQL.

## Responsibility boundary

The Action answers:

> Can this technical operation be performed through the available GitHub interface?

The canonical Method and consuming project answer different questions:

- Is this operation appropriate under the Method?
- Is it permitted in this project/context?
- Does the acting role have authority to decide it?

The Action must not collapse those questions into capability availability.

## Validation

From the repository root:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_openapi.py
```

Then follow the acceptance test plan in `tests/github-action-acceptance.md` using read-only operations first and disposable resources for structural mutation tests.
