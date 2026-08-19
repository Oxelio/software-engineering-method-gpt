# Software Engineering Method GPT

Version-controlled source for the **Software Engineering Method Custom GPT**.

This repository contains the files used to configure the Custom GPT, its GitHub Action contract, and the version of the Software Engineering Method currently used as GPT knowledge.

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

## GPT configuration

The Custom GPT configuration is stored in [`gpt/`](gpt/).

It contains:

- [`instructions.md`](gpt/instructions.md): Custom GPT instructions;
- [`description.md`](gpt/description.md): GPT name, description, and positioning;
- [`conversation-starters.md`](gpt/conversation-starters.md): conversation starters displayed to users.

These files are the version-controlled representation of the corresponding fields configured in the Custom GPT.

Platform-managed settings that are not represented by these files remain configured directly in ChatGPT.

## Software Engineering Method

The canonical Software Engineering Method is maintained in:

```text
Oxelio/software-engineering-method
```

This repository consumes it as a pinned Git submodule:

```text
software-engineering-method/
```

The submodule revision defines which version of the Method this repository adopts as the knowledge source for the Custom GPT.

Generic Software Engineering Method rules must therefore be changed in the Method repository, not duplicated here.

## GitHub Action

The Custom GPT GitHub integration is defined by:

```text
actions/github/openapi.yaml
```

This OpenAPI document defines the technical operations exposed to the GPT.

It describes what the GitHub Action can technically perform. It does not by itself grant the GPT permission to execute an operation in a specific project.

Project-specific permissions and governance remain the responsibility of the project being operated on.

## Validation

GitHub Actions validates:

```text
actions/github/openapi.yaml
```

The purpose of this validation is only to ensure that the GitHub Action contract remains a valid OpenAPI document.

## Updating the GPT

When changing the Custom GPT:

1. update the relevant files under `gpt/`;
2. update `actions/github/openapi.yaml` when GitHub capabilities change;
3. update the `software-engineering-method` submodule when the GPT should use a newer Method revision;
4. reflect the changed configuration in the Custom GPT in ChatGPT.

The repository intentionally remains minimal: files should only be added when they represent an actual part of the Custom GPT configuration or are required to validate it.