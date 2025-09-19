# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Note:** This project uses [*Towncrier*](https://towncrier.readthedocs.io/) to manage the changelog automatically. **Do not manually edit or commit changes to this file.**

<!-- towncrier release notes start -->

## [v1.2.0](https://github.com/jd-35656/readme-credly-badges/tree/v1.2.0) - 2025-09-19

### Removed

- Deprecated GitHub workflows (changelog, release, tests), old markdown issue templates (bug_report.md, feature_request.md), documentation files (CODE_OF_CONDUCT.md, CONTRIBUTING.md, SECURITY.md), and old changelog fragments in changelog.d/ ([#33](https://github.com/jd-35656/readme-credly-badges/issues/33))

### Added

- Added new GitHub Actions workflows for CI, release, labels, and stale issue management; YAML-based issue templates replacing old markdown versions; and labels configuration and CODEOWNERS file ([#33](https://github.com/jd-35656/readme-credly-badges/issues/33))

### Changed

- Updated README with latest repo and workflow information, updated main changelog file to reflect current repository state, and modified .github/PULL_REQUEST_TEMPLATE.md and dependabot.yml ([#33](https://github.com/jd-35656/readme-credly-badges/issues/33))
- Removed `changelog` job from the `all-green` workflow check to avoid pipeline failures when changelog updates are skipped. ([#34](https://github.com/jd-35656/readme-credly-badges/issues/34))

## [v1.1.0](https://github.com/jd-35656/readme-credly-badges/tree/v1.1.0) - 2025-08-13

### Added

- Created `dependabot.yml` for dependency updates

### Changed

- Updated README to fix permission issue
- Bumped `actions/checkout` from v4 to v5 in GitHub Actions

### CI

- Pre-commit configuration autoupdate

## [v1.0.1](https://github.com/jd-35656/readme-credly-badges/tree/v1.0.1) - 2025-06-21

### Added

- Community documentation

### Changed

- README updated for improved documentation

## [v1.0.0](https://github.com/jd-35656/readme-credly-badges/tree/v1.0.0) - 2025-06-21

### Added

- Add GitHub Action to automatically update README with Credly badges. ([#7](https://github.com/jd-35656/readme-credly-badges/issues/7))
