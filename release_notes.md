## [v1.2.0](https://github.com/jd-35656/readme-credly-badges/tree/v1.2.0) - 2025-09-19

### Removed

- - Deprecated GitHub workflows (changelog, release, tests)
  - Old markdown issue templates (bug_report.md, feature_request.md)
  - Documentation files: CODE_OF_CONDUCT.md, CONTRIBUTING.md, SECURITY.md
  - Old changelog fragments in changelog.d/

  ([#33](https://github.com/jd-35656/readme-credly-badges/issues/33))

### Added

- - New GitHub Actions workflows for CI, release, labels, and stale issue management
  - YAML-based issue templates replacing old markdown versions
  - Labels configuration and CODEOWNERS file

  ([#33](https://github.com/jd-35656/readme-credly-badges/issues/33))

### Changed

- - Updated README with latest repo and workflow information
  - Updated main changelog file to reflect current repository state
  - Modified .github/PULL_REQUEST_TEMPLATE.md and dependabot.yml

  ([#33](https://github.com/jd-35656/readme-credly-badges/issues/33))
- - Removed `changelog` job from the `all-green` workflow check to avoid pipeline failures when changelog updates are skipped. ([#34](https://github.com/jd-35656/readme-credly-badges/issues/34))


