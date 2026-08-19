# Software Engineering Method GPT

Version-controlled backup of the **Software Engineering Method Custom GPT** configuration, Method knowledge revision, and GitHub Action contract.

The Custom GPT is configured manually in ChatGPT. This repository preserves the corresponding files in Git; it is not a deployment source of truth and does not prove which configuration is currently deployed.

## Repository structure

```text
software-engineering-method-gpt/
├── README.md
├── .gitmodules
│
├── software-engineering-method/
│
├── gpt/
│   ├── README.md
│   ├── instructions.md
│   ├── description.md
│   └── conversation-starters.md
│
├── actions/
│   └── github/
│       └── openapi.yaml
│
└── .github/
    └── workflows/
        └── validate.yml
```

## GPT configuration backup

The files under [`gpt/`](gpt/) back up the corresponding Custom GPT fields:

- [`instructions.md`](gpt/instructions.md): Custom GPT instructions;
- [`description.md`](gpt/description.md): GPT name, description, and positioning;
- [`conversation-starters.md`](gpt/conversation-starters.md): conversation starters displayed to users.

Platform-managed settings that are not represented by these files remain configured directly in ChatGPT.

## Software Engineering Method

The canonical Software Engineering Method is maintained in:

```text
Oxelio/software-engineering-method
```

This repository references it as a pinned Git submodule:

```text
software-engineering-method/
```

The pinned revision records the Method version associated with this repository backup and used as GPT knowledge when the backup is kept in sync with ChatGPT.

Generic Software Engineering Method rules belong in the Method repository rather than being maintained as a second canonical copy here.

## GitHub Action

The Custom GPT GitHub integration contract is stored in:

```text
actions/github/openapi.yaml
```

The OpenAPI document defines the technical operations exposed by the GitHub Action. Tool availability does not by itself grant authority to decide or perform a project change; applicable project governance and Role Authority still apply.

## Validation

GitHub Actions validates:

```text
actions/github/openapi.yaml
```

The validation only checks that the GitHub Action contract remains a valid OpenAPI document.

## Keeping the backup current

When the Custom GPT changes:

1. update the matching files under `gpt/`;
2. update `actions/github/openapi.yaml` when the GitHub Action contract changes;
3. update the `software-engineering-method` submodule when the GPT knowledge revision changes.

The repository intentionally remains minimal. Add files only when they represent part of the backed-up Custom GPT configuration, its Method knowledge reference, its GitHub Action contract, or the validation required for that contract.
