# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

# [0.16.0] - 2022-09-29
### Added
- `fieldtype value add`
- `fieldtype value remove`
- `fieldtype update`

### Changed
- `user update -gr` user server-side role name validation.

# [0.15.0] - 2022-09-27
### Added
- `project field add` to add fields that a project should see.
- `project field remove` to remove fields that a project should see.
- `project field list` to list fields that a project should see.

# [0.14.0] - 2022-09-15
### Changed
- `proforma list` restricted to only proformas shared with the user
- `analysis add` no longer need filter-str

### Added
- `proforma share` command to share a proforma with a given group
- `proforma unshare` command to unshare a proforma with a given group
- `analysis definition list` command

# [0.13.5] - 2022-09-12
### Fixed
- `user list` fixed table row truncation and formatting.

# [0.13.4] - 2022-09-07
### Changed
- `user update` to use user id instead of email
- `user list` fixed formatting for an easier read

# [0.13.3] - 2022-09-06
### Fixed
- `proforma list` and `proforma show` commands fixed to handle suggested species correctly
- `proforma add` fixed to set the newly-created project to active

# [0.13.2] - 2022-09-02
### Fixed
- The `seq add -t fastq` command now explicitly requires the sample-to-file CSV, and does not expect the user to specify OwnerOrg or Species, since these must already have been provided in a minimal metadata upload

## [0.13.1] - 2022-08-29
### Added
- Added `group assign` command
- Added `group unassign` command

- Fixed build pipeline breakage due to pipenv lock -r option deprecation

## [0.12.2] - 2022-08-11
### Fixed
- Fixed `user add` and `user update` commands crash due to backend API change.

## [0.12.1] - 2022-08-11
### Fixed
- Fixed a bug where the group table formatting drops the organisation column after normalization, even though it is there only some of the time. This used to cause a crash.

## [0.12.0] - 2022-08-10
### Added
- Added `group list` command
- Added `group add` command
- Added `group update` command

### Changed
- Normalized output of tables that contain json data, turning nested object properties into columns.

## [0.11.0] - 2022-08-03
### Changed
- `org update` now accepts an organisation abbreviation.

## [0.10.1] - 2022-08-03
### Fixed
- Fixed a bug where the `description` option was hidden on `fieldtype add`.

## [0.10.0] - 2022-07-21
### Added
- Added `user add` command.
- Added `user update` command.
- Added `species add` command.
- Added `species update` command.
- Added `analysis definition add` command.
- Added `analysis definition update` command.
- Added `analysis instance list` command.

## [0.9.0] - 2022-07-18
### Added
- Added `fieldtype add` command.

## [0.8.0] - 2022-07-08
### Added
- Added `org add` command.
- Added `org update` command.
- Added support for enabling and disabling pro formas.
- Added support for fields minWidth.

## [0.7.0] - 2022-06-27
### Added
- Added `proforma list` command.
- Added `proforma add` command.
- Added `proforma show` command.
- Added `field list` command.
- Added `field add` command.
- Added `field update` command.
- Added `project add` command.
- Added `species add` command.

### Changed
- `metadata add` using unique key for Proforma.

### Removed
- Removed `species` from `metadata add`.

### Fixed
- Linting for print statements.

## [0.6.0] - 2022-05-16
### Added
- `seq get` command for retrieval of FASTQ/FASTA sequences.

### Changed
- `tree add` command now uses Analysis abbreviation.
- `metadata add` command now uses Species abbreviation.

## [0.5.3] - 2022-05-10
### Fixed
- Fixed broken build.

## [0.5.2] - 2022-05-10
### Changes
- CI/CD upgrades.

## [0.5.1] - 2022-05-04
### Changes
- CI/CD upgrades.

## [0.5.0] - 2022-04-20
### Fixed
- Unauthorised calls are not displayed correctly.

### Changed
- Uploading a tree no longer requires a Species ID.

## [0.4.1] - 2022-04-01
### Fixed
- Response indentation was not uniform.
- Call to updated tree upload endpoint

## [0.4.0] - 2022-03-30
### Changed
- Added fastq submission endpoint.

## [0.3.0] - 2022-03-15
### Changed
- Updated to use sequence submission endpoint.
- Changes to how API responses are printed.

## [0.2.1] - 2022-03-09
### Changed
- Metadata commands to use updated endpoint.

## [0.2.0] - 2022-03-07
### Added
- Sequence submission command.

### Changed
- Moved metadata commands from `submission` to `metadata`.

## [0.1.5] - 2022-03-07
### Fixed
- A bug where `species list` would include Analysis Definition information.

## [0.1.4] - 2022-02-28
### Fixed
- A bug that would cause failed tree uploads.

## [0.1.3] - 2022-02-01
### Fixed
- No longer sending empty request body with GET requests; this would cause rejections from the application firewall.

## [0.1.2] - 2022-01-12
### Added
- Added project and org commands sections.

## [0.1.1] - 2021-12-14
### Fixed
- Imports were broken.

## [0.1.0] - 2021-11-30
### Added
- Command to create Static Table analyses.
### Changed
- Project structure for components.

## [0.0.4] - 2021-11-09
### Changed
- Project structure for components.

### Added
- Updated readme with project structure information.

## [0.0.3] - 2021-11-09
### Fixed
- Fixed imports.

## [0.0.2] - 2021-11-08
### Fixed
- Fixed build.

## [0.0.1] - 2021-10-25
- Initial release.

<!-- Links -->
[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html

<!-- Versions -->
[0.0.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.0.1
[0.0.2]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.0.2
[0.0.3]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.0.3
[0.0.4]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.0.4
[0.1.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.1.0
[0.1.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.1.1
[0.1.2]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.1.2
[0.1.3]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.1.3
[0.1.4]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.1.4
[0.1.5]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.1.5
[0.2.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.2.0
[0.2.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.2.1
[0.3.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.3.0
[0.4.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.4.0
[0.4.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.4.1
[0.5.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.5.0
[0.5.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.5.1
[0.5.2]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.5.2
[0.5.3]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.5.3
[0.6.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.6.0
[0.7.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.7.0
[0.8.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.8.0
[0.9.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.9.0
[0.10.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.10.0
[0.10.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.10.1
[0.11.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.11.0
