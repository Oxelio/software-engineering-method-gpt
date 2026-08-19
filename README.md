# Software Engineering Method GPT

Version-controlled source for the **Software Engineering Method** Custom GPT.

This repository owns the GPT-specific configuration, runtime instructions, technical actions, validation tooling, and acceptance-test assets. It does **not** own the canonical Software Engineering Method itself and it does **not** own project-specific governance.

> **Tool Capability != Operational Permission != Role Authority**

A technical operation being available to the GPT never implies that the GPT is authorized to execute it in a particular project.

## Current truth

The repository currently contains the Custom GPT definition, supporting GitHub Action contract, and a pinned Git submodule at:

```text
software-engineering-method/
```

The canonical Method remains owned by `Oxelio/software-engineering-method`. This repository owns only the decision to consume a specific pinned Method revision: `.gitmodules` records the submodule path/repository mapping and the root gitlink records the exact adopted revision.

The submodule source can be used to prepare Method knowledge for GPT deployment. Any deployment-specific packaging remains a deployment artifact and does not become a second owner of Method rules.

## Sources of truth

| Concern | Source of truth |
| --- | --- |
| General Software Engineering Method | `Oxelio/software-engineering-method` |
| Method revision adopted by this repository | root `software-engineering-method` gitlink |
| Custom GPT runtime behavioral contract | `gpt/instructions.md` |
| Custom GPT display name, short description, and positioning | `gpt/description.md` |
| Version-controlled deployment configuration | `gpt/configuration.yaml` |
| Conversation starters | `gpt/conversation-starters.md` |
| GitHub technical capability | `actions/github/` |
| Project-specific Method Profile and governance | the consuming project repository |
| Project-specific Operational Permissions | the consuming project repository |

These sources own different kinds of truth. The pinned submodule supplies canonical Method material from its external owner; this repository must not turn that material into a competing canonical Method copy.

## Current repository architecture

```text
software-engineering-method-gpt/
├── README.md
├── .gitignore
├── .gitmodules
├── requirements-dev.txt
│
├── software-engineering-method/        # pinned Git submodule
│
├── gpt/
│   ├── README.md
│   ├── configuration.yaml
│   ├── instructions.md
│   ├── description.md
│   └── conversation-starters.md
│
├── actions/
│   └── github/
│       ├── README.md
│       ├── capabilities.md
│       └── openapi.yaml
│
├── scripts/
│   ├── README.md
│   └── validate_openapi.py
│
├── tests/
│   ├── fixtures/
│   │   └── architecture-web.yaml
│   └── github-action-acceptance.md
│
└── .github/
    └── workflows/
        └── validate.yml
```

## Responsibility boundaries

### This repository owns

- Custom GPT runtime instructions and GPT-specific behavior;
- version-controlled GPT deployment/configuration metadata;
- the GPT display metadata and conversation starters;
- the pinned Method revision adopted by this GPT repository;
- GitHub Action/OpenAPI capability definitions;
- GPT-specific validation tooling;
- GPT-specific acceptance-test assets.

### This repository does not own

- the canonical Software Engineering Method;
- generic definitions of Work, Work State, WIP, Continuous Flow, Architecture Review, Role Authority, or Operational Permission;
- project-specific Method Profiles;
- project-specific governance or Current Truth;
- project-specific authorization decisions.

## Method integration

The canonical Method is consumed as a pinned Git submodule at:

```text
software-engineering-method/
```

The root `.gitmodules` file owns the submodule path/repository mapping. The root gitlink owns the exact Method revision currently adopted by this repository.

The dependency direction is:

```text
Oxelio/software-engineering-method
              │
              │ canonical Method
              ▼
Oxelio/software-engineering-method-gpt
              │
              ├── pinned Method source
              ├── GPT runtime configuration
              ├── deployment knowledge packaging
              └── Tool capabilities
```

Consuming projects such as `Oxelio/Architecture-Web` consume the Method independently. They do not depend on this GPT repository in order to obtain the Method.

Updating the submodule is an intentional dependency change: review the target Method revision, update the gitlink, and refresh any deployment knowledge package that must track it.

## GPT configuration

The version-controlled GPT configuration lives under [`gpt/`](gpt/README.md).

[`gpt/configuration.yaml`](gpt/configuration.yaml) is the repository-owned deployment configuration manifest. It references the runtime files, current Method source, and GitHub Action schema without duplicating presentation values owned elsewhere.

[`gpt/description.md`](gpt/description.md) is the authoritative repository owner of the Custom GPT display name, short description, and positioning text.

[`gpt/instructions.md`](gpt/instructions.md) is the **runtime behavioral contract** for the Custom GPT. It constrains how the agent applies authoritative sources, resolves context and authority, handles conflicts, and uses tools. It is not a second canonical copy of the Software Engineering Method.

Detailed generic Method definitions remain owned by `Oxelio/software-engineering-method` and are consumed here through the pinned submodule. When Method material is supplied to the deployed GPT, deployment packaging must preserve that ownership rather than converting the package into a new normative source.

## GitHub Action

The GitHub integration is a **Tool Capability** of the Custom GPT. Its contract is located at:

```text
actions/github/openapi.yaml
```

Current contract version: **2.1.0**.

The Action intentionally exposes a bounded set of GitHub REST and Projects v2 GraphQL operations. It does not define authorization policy. See:

- [`actions/github/README.md`](actions/github/README.md)
- [`actions/github/capabilities.md`](actions/github/capabilities.md)
- [`tests/github-action-acceptance.md`](tests/github-action-acceptance.md)

## Local validation

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Validate the OpenAPI contract:

```bash
python scripts/validate_openapi.py
```

Validation has two distinct layers:

1. standard OpenAPI validation against the OpenAPI specification;
2. repository-specific invariants such as exact OpenAPI version, unique `operationId` values, local references, and the bounded GraphQL allowlist.

The same validation runs in GitHub Actions through `.github/workflows/validate.yml`.

## Change workflow

Keep changes scoped to the responsibility that owns them:

1. change generic Method rules in `Oxelio/software-engineering-method`;
2. update the root `software-engineering-method` gitlink intentionally when this GPT repository should adopt a different canonical Method revision;
3. change `gpt/` only for GPT-specific runtime behavior, presentation, or deployment configuration;
4. change `actions/github/` only for technical GitHub capabilities;
5. change project-specific governance in the consuming project repository;
6. validate the OpenAPI contract and relevant acceptance tests before updating the deployed Custom GPT;
7. refresh deployment knowledge derived from the Method whenever the adopted submodule revision changes.
