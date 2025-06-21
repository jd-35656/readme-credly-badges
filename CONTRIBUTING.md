# Contributing to `readme-credly-badges`

Thanks for your interest in contributing!
Everyone engaging with this project—through code, issues, or discussions—is expected to follow our [Code of Conduct](https://github.com/jd-35656/readme-credly-badges/blob/main/CODE_OF_CONDUCT.md).

---

## 🚀 How to Contribute

1. **Fork** the [repository](https://github.com/jd-35656/readme-credly-badges).
2. **Create a branch** from `main` (use a descriptive name like `fix-typo-in-readme`).
3. **Make your changes** and **commit** them with a clear message.
4. **Add a changelog entry** (see below).
5. **Open a pull request** to the `main` branch, referencing any related issue.

---

## 📝 Writing Changelog Entries

We use [**Towncrier**](https://pypi.org/project/towncrier/) to manage the changelog.

To add an entry:

1. Create a file in the `changelog.d/` folder.
2. Name it using the format:

   ```
   <number>.<type>.md
   ```

   - `<number>`: Issue or pull request number
   - `<type>`: One of `feature`, `bugfix`, `doc`, `removal`, or `misc`

**Examples:**

- `123.feature.md`
- `456.bugfix.md`

### Style Guidelines

- Use **imperative tone**:
  ✅ `Add support for large badges`
  ❌ `Added support for large badges`
- Keep the summary **under 80 characters** if possible.
- For longer entries, start with a **summary line**, followed by wrapped paragraphs with extra details.
- No need to mention issue numbers or your name—Towncrier handles that.

---

## 🛠 Development Guide

### Create a Developer Environment

We use [nox](https://pypi.org/project/nox/) for managing sessions:

```bash
python -m pip install --user nox
nox -s develop-3.12
```

Use the interpreter at `.nox/develop-3.12/bin/python` in your IDE if needed.

### Run Tests

List available sessions:

```bash
nox -l
```

Run unit tests (example for Python 3.12):

```bash
nox -s tests-3.12
```

Run a specific test:

```bash
nox -s tests-3.12 -- -k test_name
```

> ℹ️ You can safely ignore coverage warnings when running specific tests.

### Run Linters

We use [pre-commit](https://pre-commit.com/) for linting and formatting:

```bash
nox -s lint
```

---

## 🤖 Continuous Integration

GitHub Actions automatically runs all checks (tests, lint, etc.) on every pull request.
Make sure your PR passes CI before requesting a review.

---

## 📦 Releasing New Versions

To release a new version:

1. Trigger the **`Bump changelog before release`** workflow from the **Actions** tab.

2. Provide the version (e.g., `v1.2.3`) when prompted.

3. This creates a PR with:

   - Updated `pyproject.toml` version
   - Generated changelog file
   - `release-version` label

4. Merge the PR to `main` — this **automatically triggers the release workflow**.

**Alternatively:**

- Label any PR with `release-version` and title it like:

```text
chore(release): v1.2.3
```

---

## 🙌 Thank You

Your contributions help make `readme-credly-badges` better for everyone!
Whether it's a typo fix or a major feature—every bit counts ❤️
