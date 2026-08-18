# GPT configuration

This directory contains the version-controlled configuration of the **Software Engineering Method** Custom GPT.

It contains GPT-specific runtime behavior and presentation only. The canonical Software Engineering Method remains in `Oxelio/software-engineering-method` and is consumed through the root-level `software-engineering-method/` submodule.

## Files

### `instructions.md`

Normative GPT-runtime instructions: how the GPT should apply the Method, resolve project context, reason about authority, and use tool capabilities.

This file may restate a Method invariant when that invariant must directly constrain runtime behavior, but it must not become an independent copy of the Method documentation.

### `description.md`

Version-controlled display name, short description, and positioning text for the Custom GPT.

### `conversation-starters.md`

Version-controlled conversation starters intended for the Custom GPT configuration.

## Method reference

Detailed Software Engineering Method definitions remain canonical in:

```text
software-engineering-method/
```

The GPT may use selected canonical Method documents as reference material, but this repository does not maintain a duplicated or generated Method snapshot by default.

If a deployment constraint later requires packaging or aggregation, add that mechanism as an explicit build/deployment concern without changing the canonical ownership of the Method.

## Authority model

Do not treat all sources as a single precedence stack: they own different kinds of truth.

- **Project Current Truth** owns project-specific facts that are currently effective.
- **Project Method Profile and governance** own project-specific tailoring, policy, and permissions.
- **Canonical Software Engineering Method** owns generic workflow and governance semantics.
- **GPT runtime instructions** constrain how this agent applies those sources; they do not replace their authoritative content.
- **Tool capabilities** describe what can technically be executed; they confer neither permission nor authority.

A draft proposal must not silently replace Current Truth. A Tool Capability must never be interpreted as Operational Permission or Role Authority.
