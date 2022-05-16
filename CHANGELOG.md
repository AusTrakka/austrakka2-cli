# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

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
