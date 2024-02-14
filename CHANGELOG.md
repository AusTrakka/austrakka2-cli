# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

# [0.50.0] - 2024-02-14
### Added
- Added new commands to support the concept of Project Metadata.
- Added `project metadata` commands.
- Added `project field` commands.
- Added `project provision` commands.
- Added `project dataset` commands.

# [0.40.0] - 2024-02-09
### Changed
- Disabled httpx client timeout to support large file upload.

# [0.39.1] - 2023-12-05
### Changed
- Minor change to optimise the Finalisation stage of the `seq sync` command.

# [0.39.0] - 2023-11-28
### Fixed
- Unauthorised responses are correctly displayed.
- `40x` responses return an exit code of `1`.

# [0.38.0] - 2023-11-23
### Changed
- The `metadata append` command has been renamed to `metadata update`. Options 
`--is-append/--not-append` have been renamed to `--is-update/--not-update`.

# [0.37.1] - 2023-11-22
### Changed
- Fixed bug in `sync get` command where re-running the "finalise" step doesn't recognise previously "Done" checks.

# [0.37.0] - 2023-11-20
### Changed
- `analysis list` now requires a `--project`.

# [0.36.0] - 2023-11-07
### Added
- `sample groups` command.

### Changed
- `user add` and `user update` to handle AusTrakka process accounts.

# [0.35.1] - 2023-09-18
### Changed
- The `seq get` command will now accept `-s` flags to download sequences by Seq_ID.

# [0.35.0] - 2023-09-06
### Changed
- `seq add` commands will now provide a summary at the end of a bulk upload, including the number of sequences uploaded, and which sequences failed upload.
- Sequence list and download commands no longer take the deprecated --sub-query-type flag. 
A CLI update to this version will be required to support download from the updated AusTrakka server.

### Fixed
- `proforma attach` command options --file-path and --n-previous are now correctly mutually exclusive

# [0.34.0] - 2023-08-30
### Added
- `seq purge` command for admins only.
- `proforma attach` command for admins to attach xlsx templates to a given proforma.

# [0.33.0] - 2023-08-07
### Added
- `project update` command.

### Security
- Removed unused dependencies.

# [0.32.5] - 2023-07-31
### Changed
- Performance improvements for `seq sync get`

### Fixed
- Fixed bug in `seq sync get` where some deleted files were not being moved to .trash

# [0.32.4] - 2023-07-26
- `seq sync get` performance improvement and minor bug fixes.

# [0.32.3] - 2023-07-22
- Added FASTA concatenation functionality to `seq sync get`

# [0.32.2] - 2023-07-21
- Added batch size option and default CSV batching for `metadata add`

# [0.32.1] - 2023-07-19
### Changed
- Added batch size option for `seq sync get` to optimise saving of state.
- Allow metadata list command to take field names
- Refactor of process auth

# [0.32.0] - 2023-07-17
### Changed
- `seq sync get` with options to use cached hashes.
- `metadata add` will ignore blank cells by default. Previous default behaviour was to delete the cell content.

# [0.31.0] - 2023-07-10
### Changed
- Changed `seq add` to accept --skip and --force for dealing with samples which already have sequences.

# [0.30.2] - 2023-07-07
### Changed
- Updated installation and usage instructions.

# [0.30.1] - 2023-07-03
### Changed
- Upgraded package dependencies.

# [0.30.0] - 2023-06-29
### Added
- `seq sync get` to support hash-based download of sequences. Resume on failure, repair drifted files, and soft-purge files no longer shared with the project.

# [0.29.1] - 2023-05-25
### Changed
- `seq get` and `seq list` accepts optional flag to get sequences by IsActive flag rather than most recent.

# [0.29.0] - 2023-05-14
### Changed
- `seq add` now split into subcommands `seq add fastq` and `seq add fasta`, intended for Illumina FASTQ and single-contig FASTA consensus sequences respectively
- `seq add` commands now carry out a hash check to ensure correctness of upload
- `seq add fasta` requires only a FASTA file as input; FASTA IDs must match known Seq_IDs
- `seq add fasta` now uploads sequences individually to separate Seq_IDs

### Added
- plot subcommands
- Parameter `project add --org` parameter to specify requesting org for a project

# [0.28.1] - 2023-05-03
### Changed
- seq add -t fastq command now verifies file hashes after upload, comparing server hash with the local file.

# [0.28.0] - 2023-05-01
### Added
- Metadata list command.

### Removed
- seq list -a option
- seq get -a option

### Changed
- Upgraded some cryptography dependency to 39.0.1

# [0.27.3] - 2023-04-14
### Fixed
- Error sending file upload requests.

# [0.27.2] - 2023-04-05
### Added
- Optional HTTP2 support.

# [0.27.1] - 2023-03-30
### Fixed
- Error running CLI.

# [0.27.0] - 2023-03-30
### Added
- Notify users if CLI is outdated.

### Security
- Strict host verification.

# [0.26.0] - 2023-03-28
### Changed
- Changed `seq get -t fastq` command to save files with a different name format.
- Make country optional for Organisations, to match endpoint change.
- Fixed org retrieval for PUT.

# [0.25.1] - 2023-03-15
### Changed
- Changed `seq add -t fastq` command to retry once on any errors.

# [0.25.0] - 2023-03-02
### Added
- Added `proforma listgroups` command to show ProFormaEditors and AusTrakkaAdmins what group has access to a given pro forma.

# [0.24.1] - 2023-02-23
### Changed
- Updates to facilitate process auth

# [0.24.0] - 2023-02-16
### Added
- Added `sample share` and `sample unshare` commands to change sharing outside of uploads.

# [0.23.2] - 2023-02-10
### Changed
- Rename `metadata check` command to `metadata validate`

# [0.23.1] - 2023-02-06
### Changed
- Changes to CI for updating work items.

# [0.23.0] - 2023-01-19
### Changed
- Added `sample enable` command to re-enable samples which are currently disabled.
- Updated readme with installation and login instructions.
- Fixed poor error reporting when server-side infra occasionally fails.

# [0.22.0] - 2022-12-22
### Changed
- Added `metadata check` command to validate upload without commiting.
- Added `metadata append` command to append more metadata without having to specify Owner_group.

# [0.21.1] - 2022-12-19
### Changed
- Updated production pipeline to release to public PyPI index.

# [0.21.0] - 2022-12-19
### Added
- Added Analysis and Group filters for `seq get`.
- Added `seq list` command.

# [0.20.1] - 2022-12-01
### Fixed
- The `seq add` command will treat all Seq_IDs as strings and not try to deduce the CSV column type

# [0.20.0] - 2022-11-11
### Added
- Added commands to restrict fields per group.

# [0.19.0] - 2022-11-07
### Removed
- All Species related commands. Species is now managed as a regular metadata field.

# [0.18.3] - 2022-11-03
### Added
- Command for uploaders to disable samples which they have authority to manage.

### Changed
- Indent JSON output
- Added object format option
- Add format to user list command
- linting
- --state flag for org add is no longer required
- Remove species job def add and update
- Support for disabling samples

# [0.18.2] - 2022-10-07
### Changed
- More helpful messaging when user has not signed in or the token is expired.
- Drop need for org parameter when creating projects.

# [0.18.1] - 2022-10-03
### Fixed
- Broken `user list` command.

# [0.18.0] - 2022-10-03
### Changed
- `user add` now uses `object-id` as the identifier rather than email.

# [0.17.0] - 2022-09-29
### Changed
- Simplified usage of the `seq add` command.

# [0.16.0] - 2022-09-29
### Added
- Added `fieldtype value add` command.
- Added `fieldtype value remove` command.
- Added `fieldtype update` command.

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
[0.12.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.12.0
[0.12.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.12.1
[0.12.2]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.12.2
[0.13.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.13.1
[0.13.2]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.13.2
[0.13.3]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.13.3
[0.13.4]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.13.4
[0.13.5]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.13.5
[0.14.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.14.0
[0.15.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.15.0
[0.16.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.16.0
[0.17.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.17.0
[0.18.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.18.0
[0.18.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.18.1
[0.18.2]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.18.2
[0.18.3]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.18.3
[0.19.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.19.0
[0.20.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.20.0
[0.20.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.20.1
[0.21.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.21.0
[0.21.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.21.1
[0.22.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.22.0
[0.23.0]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.23.0
[0.23.1]: https://github.com/AusTrakka/austrakka2-cli/releases/tag/0.23.1
