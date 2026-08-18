# GitHub capability model

## Invariant

`Tool Capability != Operational Permission != Role Authority`

The GitHub Action owns **technical GitHub primitives** only.

The canonical Software Engineering Method defines general governance semantics. A consuming project defines its adopted Project Method Profile, project-specific governance, and Operational Permissions. Role Authority must be resolved independently from the existence of an API operation.

## P0 — read model

### Project discovery

- user Projects v2 listing/search with cursor pagination;
- organization Projects v2 listing/search with cursor pagination;
- existing get-by-number queries retained for compatibility.

### Project fields

- field ID, name, GraphQL concrete type, and `dataType`;
- single-select options;
- multi-select options;
- iteration configuration and iterations;
- cursor pagination.

### Project items

- Project item ID/type/archive state;
- Issue / Pull Request / Draft Issue identity;
- repository and Issue/PR number where applicable;
- common Project field values;
- organization Issue-field values when surfaced through a Project item;
- cursor pagination for items and a dedicated paginated item-field-values query.

### Sub-issues

- get parent Issue;
- list Sub-issues.

### Content node resolution

No duplicate API call is introduced: `getIssue().node_id` and `getPullRequest().node_id` are the canonical `contentId` values for `addProjectV2ItemById`.

## P0 — mutations

- add Project item (existing);
- remove Project item;
- update Project item field value through `ProjectV2FieldValue`;
- clear Project item field value;
- create Project custom field;
- delete Project custom field;
- add native Sub-issue relation;
- remove native Sub-issue relation.

Structural mutations require authorization independent from Tool Capability. They must be justified by the applicable Method/project context, permitted by the project's Operational Permissions, and executed within the acting role's authority.

## P1

- list Project views (read-only capability included in 2.1.0);
- organization Issue Field metadata/options (read-only capability included because Issue Fields and Project custom fields are distinct concepts).

View mutations remain intentionally unexposed in this increment even though the API may provide them.

## Additional capability added after implementation discovery

`POST /user/repos` (`createRepository`) is included because repository creation was identified as a required GitHub capability during repository bootstrap work. Repository deletion remains unexposed.

## Out of scope

The Action does not own or enforce:

- Architecture Web policy;
- automatic creation of project-specific fields such as `Priority` or `Workflow Depth`;
- adoption of a governance pull request into a live GitHub Project;
- merge authority;
- arbitrary GraphQL;
- generic Software Engineering Method definitions.

Those concerns belong to the canonical Method and/or the consuming project's governance, depending on whether they are generic or project-specific.
