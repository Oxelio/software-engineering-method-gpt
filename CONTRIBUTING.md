# Contribution and validation policy

## Commit messages

Pull-request titles and every commit introduced by a pull request MUST use a
Conventional Commit header:

`<type>(<optional-scope>): <description>`

Allowed types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
`build`, `ci`, `chore`, and `revert`. Breaking changes may use `!` before `:`.

`.github/workflows/governance.yml` enforces this policy on pull requests.

## Method submodule validation boundary

`.gitmodules` owns the Method submodule path/repository mapping. The root
`software-engineering-method` gitlink owns the exact adopted revision. Merge-time
validation checks that these owners are structurally coherent without requiring
cross-repository credentials.

Because the canonical Method repository is private, fetchability is a
deployment/release concern. Before packaging or publishing the Custom GPT,
execute the following in an environment that already has read access to the
canonical Method repository:

`python scripts/validate_method_source.py`

This command initializes the submodule and verifies that the checked-out Method
revision exactly matches the gitlink pinned by this repository. The repository
does not own or provision the required credential.

## Custom GPT deployment validation

Repository validation proves the version-controlled deployment inputs, not the
effective state of the external Custom GPT platform. Before declaring a
deployment effective, validate the assembled GPT in the target platform,
including that the pinned Method content is present through Knowledge and that
the runtime instructions behave against that knowledge as intended.
