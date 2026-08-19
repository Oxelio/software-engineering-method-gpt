# GPT configuration

This directory contains the version-controlled configuration of the **Software Engineering Method** Custom GPT.

It contains GPT-specific runtime behavior, presentation, and deployment metadata only. The canonical Software Engineering Method remains owned by `Oxelio/software-engineering-method`.

## Current truth

The canonical Method repository is currently consumed through the pinned root-level Git submodule:

```text
software-engineering-method/
```

The parent repository's `.gitmodules` file owns the submodule path/repository mapping. The gitlink at `software-engineering-method` owns the exact Method revision adopted by this GPT repository.

The submodule is an integration mechanism, not a transfer of Method ownership: generic Method semantics remain canonical in `Oxelio/software-engineering-method`.

## Files

### `configuration.yaml`

Repository-owned deployment configuration manifest.

It records the Custom GPT runtime files, current Method knowledge source, and GitHub Action schema using values already established by this repository. Platform capability flags that have no authoritative repository value are deliberately left unspecified rather than guessed.

Presentation values such as the GPT display name are not duplicated here when another repository artifact already owns them.

### `instructions.md`

Runtime behavioral contract for the deployed GPT.

It defines the agent-side invariants needed to apply authoritative Method and project sources safely: authority boundaries, human-only gates, context resolution, escalation, role limits, conflict handling, and tool-use boundaries.

It may restate a Method invariant only when that invariant must directly constrain runtime behavior. It must not become an independent canonical copy of the Method documentation.

### `description.md`

Authoritative repository owner of the version-controlled display name, short description, and positioning text for the Custom GPT.

Other repository artifacts may reference these presentation values but must not establish a competing normative value.

### `conversation-starters.md`

Version-controlled conversation starters intended for the Custom GPT configuration.

## Method knowledge flow

Detailed Software Engineering Method definitions remain canonical in:

```text
Oxelio/software-engineering-method
```

This repository consumes an intentionally pinned revision at:

```text
software-engineering-method/
```

The deployment flow is:

```text
Canonical Method
      │
      ▼
pinned software-engineering-method/ submodule
      │
      ▼
deployment knowledge package
      │
      ▼
deployed Custom GPT knowledge
```

The knowledge package is a deployment artifact, not a new authority owner. Generic Method rules remain owned by the canonical Method repository even when packaged for the GPT platform.

Updating the Method gitlink is an explicit dependency change and should be reviewed together with any deployment knowledge refresh required by the new pinned revision.

## Authority model

Do not treat all sources as a single precedence stack: they own different kinds of truth.

- **Project Current Truth** owns project-specific facts that are currently effective.
- **Project Method Profile and governance** own project-specific tailoring, policy, and permissions.
- **Canonical Software Engineering Method** owns generic workflow and governance semantics.
- **Pinned Method gitlink** owns which canonical Method revision this GPT repository currently adopts.
- **GPT runtime instructions** constrain how this agent applies those sources; they do not replace their authoritative content.
- **Tool capabilities** describe what can technically be executed; they confer neither permission nor authority.

A draft proposal must not silently replace Current Truth.

> **Tool Capability != Operational Permission != Role Authority**
