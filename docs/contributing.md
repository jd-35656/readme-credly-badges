# Contributing

Thanks for your interest in contributing! We welcome bug reports, feature requests, and code improvements.

* Report bugs or request features on the [Issues page](https://github.com/jd-35656/readme-credly-badges/issues).
* Submit pull requests to propose changes.

## Development Setup

### 1. Clone and Install Tools

```bash
git clone https://github.com/jd-35656/readme-credly-badges.git
cd readme-credly-badges
pipx install nox
```

### 2. Create Development Environment

```bash
nox -s develop-3.13
```

### 3. Activate / Deactivate Environment

```bash
source .nox/develop-3.13/bin/activate
# work inside environment
deactivate
```

### 4. Use Other Python Versions

```bash
nox -l                  # List supported Python versions
nox -s develop-3.11     # Create env for Python 3.11
```

### 5. IDE Setup (VS Code)

* Open the project folder.
* Select interpreter: `Ctrl+Shift+P` → “Python: Select Interpreter” → `.nox/develop-3.13/bin/python`
* Recommended extensions: Python, Pylance, Ruff.

### 6. Verify Setup

Run tests and checks:

```bash
nox           # Runs all sessions (tests + lint + typecheck)
nox -s tests
nox -s lint
nox -s typecheck
```

## Changelog Entries

Add a changelog file in `changelog.d/` named as:

```txt
<number>.<type>.md
```

Allowed types: `added`, `changed`, `deprecated`, `removed`, `fixed`, `security`.

Examples:

* `123.added.rst` — Add JSON validation
* `456.fixed.rst` — Fix template loading

---

## Testing

### Available Sessions

List all test-related sessions with:

```bash
nox -l
```

Typical sessions include:

* `develop-3.x` — Create development environment
* `tests-3.x` — Run tests with coverage
* `lint` — Code formatting and linting
* `typecheck` — Type checking (e.g., with mypy)
* `check` — Run lint + typecheck together

### Running Tests

Run tests on all supported Python versions:

```bash
nox -s tests
```

Or for a specific Python version (e.g., 3.13):

```bash
nox -s tests-3.13
```

Run default sessions (tests + lint + typecheck):

```bash
nox
```

### Code Quality Checks

Run linting only:

```bash
nox -s lint
```

Run type checking only:

```bash
nox -s typecheck
```

Run both lint and typecheck:

```bash
nox -s check
```

### Test Coverage

* Tests automatically generate coverage reports.
* Minimum coverage required: **90%**
* Current coverage: **100%**

---

## Releasing

### Quick Release Guide

#### Using GitHub Actions

1. Go to **GitHub Actions** → **Create Release** workflow.
2. Click **Run workflow**, select release type, and run.

#### Or Use PR Labels

* Add one label to the merged PR to trigger an automatic release:

  * `release:patch`
  * `release:minor`
  * `release:major`

> **Note:** The following pre-requisites apply **only** for PR label-triggered releases:

* All CI checks pass.
* Changelog fragments exist **OR** `no-changelog` label is applied.
* Main branch is clean.

### Release Types

* `release:patch` — Bug fixes (e.g., v1.0.0 → v1.0.1)
* `release:minor` — New features (e.g., v1.0.0 → v1.1.0)
* `release:major` — Breaking changes (e.g., v1.0.0 → v2.0.0)

### What Happens Automatically

* Version bump based on release type.
* Changelog generated from fragments (`changelog.d/`).
* Git commit & tag created.
* GitHub release created with notes.
* Package built and uploaded to PyPI.
* Documentation deployed.
