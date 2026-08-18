# Capability model

## Invariant

`Tool Capability != Operational Permission != Role Authority`

This repository owns **technical GitHub primitives** only. A consuming repository owns the policy deciding whether a primitive may be used.

## P0 — read model

### Project discovery
- user Projects v2 listing/search with cursor pagination
- organization Projects v2 listing/search with cursor pagination
- existing get-by-number queries retained for compatibility

### Project fields
- field ID, name, GraphQL concrete type, and `dataType`
- single-select options
- multi-select options
- iteration configuration and iterations
- cursor pagination

### Project items
- Project item ID/type/archive state
- Issue / Pull Request / Draft Issue identity
- repository and Issue/PR number where applicable
- common Project field values
- organization Issue-field values when surfaced through a Project item
- cursor pagination for items and a dedicated paginated item-field-values query

### Sub-issues
- get parent Issue
- list Sub-issues

### Content node resolution
No duplicate API call is introduced: `getIssue().node_id` and `getPullRequest().node_id` are the canonical `contentId` values for `addProjectV2ItemById`.

## P0 — mutations

- add Project item (existing)
- remove Project item
- update Project item field value through `ProjectV2FieldValue`
- clear Project item field value
- create Project custom field
- delete Project custom field
- add native Sub-issue relation
- remove native Sub-issue relation

Structural mutations require independent authorization from the consuming workflow.

## P1

- list Project views (read-only capability included in 2.1.0)
- organization Issue Field metadata/options (read-only capability included because Issue Fields and Project custom fields are distinct concepts)

View mutations remain intentionally unexposed in this increment even though GitHub now provides them.

## Additional capability added after implementation discovery

`POST /user/repos` (`createRepository`) is included because repository creation was a concrete capability gap encountered while trying to bootstrap this canonical repository. Repository deletion remains unexposed.

## Out of scope

- Architecture Web policy enforcement
- automatic creation of `Priority` or `Workflow Depth`
- applying governance PR #2 to Project #3
- merge authority
- arbitrary GraphQL
