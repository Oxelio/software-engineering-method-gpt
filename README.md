# GitHub Repository Orchestrator

Canonical source for the OpenAPI contract used by the GitHub Custom GPT action.

## Purpose

This repository versions the technical capabilities exposed to ChatGPT for GitHub repository and delivery-workflow orchestration. It deliberately separates API capability from project governance.

> **Tool Capability != Operational Permission != Role Authority**

A mutation being present in this contract never means an agent is authorized to perform it in a specific project.

## Current contract

- OpenAPI: `openapi/github-repository-orchestrator.openapi.yaml`
- Contract version: **2.1.0**
- GitHub REST server: `https://api.github.com`
- GraphQL: `/graphql`, restricted to an explicit allowlist of exact operations

## 2.1.0 highlights

- create a repository for the authenticated user (no repository deletion capability)
- discover Projects v2 for user and organization owners without knowing the project number
- inspect Project fields with data type, select options, and iteration configuration
- list Project items and their field values, with cursor pagination
- generic Project field-value update plus explicit clear
- create/delete Project custom fields
- remove a Project item
- read Project views
- native GitHub Sub-issues: parent/list/add/remove
- read organization Issue Field metadata/options separately from Project custom fields
- preserve Issue/PR `node_id` as the standard Projects v2 `contentId` resolution path

## Safety boundary

The contract intentionally does **not** expose:

- arbitrary GraphQL
- repository deletion
- pull-request merge
- destructive Project deletion
- Project view mutations in this increment

Project-specific governance (for example, whether a Work may move from `Preparing` to `Ready`) belongs to the consuming project, not to this connector contract.

## Consumer currently driving the capability set

`Oxelio/Architecture-Web` is a consumer and validation target, not the owner of this connector contract. Its governance PR and GitHub Project must not be modified merely to test connector contract capabilities.

## Deployment to a Custom GPT

1. Validate the YAML locally.
2. In the GPT editor, open **Actions**.
3. Replace/import the action schema from `openapi/github-repository-orchestrator.openapi.yaml`.
4. Keep the existing GitHub authentication configuration.
5. Test read-only operations first.
6. Use disposable Issues for structural mutation tests.

See `docs/capabilities.md` and `docs/validation.md`.
