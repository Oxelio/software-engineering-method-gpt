# Software Engineering Method GPT

Version-controlled source for the **Software Engineering Method** Custom GPT.

This repository owns the GPT-specific configuration, runtime instructions, technical actions, validation tooling, and acceptance-test assets. It does **not** own the canonical Software Engineering Method itself and it does **not** own project-specific governance.

> **Tool Capability != Operational Permission != Role Authority**

A technical operation being available to the GPT never implies that the GPT is authorized to execute it in a particular project.

## Sources of truth

| Concern | Source of truth |
| --- | --- |
| General Software Engineering Method | `Oxelio/software-engineering-method` |
| Custom GPT behavior and configuration | this repository, primarily `gpt/` |
| GitHub technical capability | `actions/github/` |
| Project-specific Method Profile and governance | the consuming project repository |
| Project-specific Operational Permissions | the consuming project repository |

The canonical Method is consumed by this repository through the root-level `software-engineering-method/` Git submodule. This repository does not maintain a second generated or copied Method tree.

## Repository architecture

```text
software-engineering-method-gpt/
├── README.md
├── .gitignore
├── .gitmodules                         # created when the submodule is added
├── requirements-dev.txt
│
├── software-engineering-method/        # Git submodule
│
├── gpt/
│   ├── README.md
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
└── tests/
    └── github-action-acceptance.md
```

## Responsibility boundaries

### This repository owns

- Custom GPT runtime instructions and GPT-specific behavior;
- the GPT description and conversation starters;
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

Add it from the repository root with:

```bash
git submodule add \
  https://github.com/Oxelio/software-engineering-method.git \
  software-engineering-method
```

Then commit the generated `.gitmodules` file and the submodule gitlink:

```bash
git add .gitmodules software-engineering-method
git commit -m "feat: integrate canonical software engineering method"
```

The parent repository pins an explicit Method commit. Updating the Method is therefore an intentional change rather than an implicit synchronization.

The dependency direction is:

```text
Oxelio/software-engineering-method
              │
              │ canonical Method
              ▼
Oxelio/software-engineering-method-gpt
              │
              ├── GPT runtime configuration
              └── Tool capabilities
```

Consuming projects such as `Oxelio/Architecture-Web` consume the Method independently. They do not depend on this GPT repository in order to obtain the Method.

## GPT configuration

The version-controlled GPT configuration lives under [`gpt/`](gpt/README.md).

The most important file is [`gpt/instructions.md`](gpt/instructions.md). It contains GPT-runtime behavior and orchestration constraints. Detailed Method definitions remain canonical in `software-engineering-method/` rather than being duplicated here.

When the Custom GPT needs Method reference material, use the canonical Method documents directly. Introduce a deployment-specific packaging mechanism only if a concrete platform constraint makes one necessary.

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

Install the development dependency:

```bash
python -m pip install -r requirements-dev.txt
```

Validate the OpenAPI contract:

```bash
python scripts/validate_openapi.py
```

The validator checks the OpenAPI version, required sections, unique operation IDs, local references, and the bounded GraphQL allowlist.

## Change workflow

Keep changes scoped to the responsibility that owns them:

1. change generic Method rules in `Oxelio/software-engineering-method`;
2. update the `software-engineering-method/` submodule reference when this GPT should adopt a newer Method revision;
3. change `gpt/` only for GPT-specific runtime behavior or configuration;
4. change `actions/github/` only for technical GitHub capabilities;
5. change project-specific governance in the consuming project repository;
6. validate the OpenAPI contract and relevant acceptance tests before updating the deployed Custom GPT.
