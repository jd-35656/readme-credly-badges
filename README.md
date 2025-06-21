# 🛡️ readme-credly-badges

A GitHub Action that automatically updates your repository's `README.md` or
any other markdown file with [Credly](https://www.credly.com/) badge details —
no manual editing required.

---

## 📸 Sample Output

![Credly Sample Badges Image](assets/badge-sample.png)

---

## ✍️ How to Add Credly Badges to Your README

### 1. Add Badge Markers to Your Markdown

Insert the following comment block in your `README.md` or any other markdown
file where you want the badges to appear:

```md
<!-- START CREDLY BADGES -->
<!-- END CREDLY BADGES -->
```

The GitHub Action will replace the content between these markers with
up-to-date badge information.

### 2. Add the GitHub Action Workflow

#### 🚀 Quickstart Workflow

Create a workflow file at `.github/workflows/update-badges.yaml` with this
minimal setup:

```yaml
name: Update Credly Badges

on:
  schedule:
    - cron: '0 0 * * *' # Runs daily at 00:00 UTC

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - name: Update Badges in README
        uses: jd-35656/readme-credly-badges@v1
```

#### ⚙️ Action Inputs

<!-- markdownlint-disable MD013 -->

| Input Name        | Description                                             | Default                          | Required |
| ----------------- | ------------------------------------------------------- | -------------------------------- | -------- |
| `credly_username` | Your Credly username                                    | `<username>`                     | ❌       |
| `badge_size`      | Badge image size (e.g., `150x150`, `680x680`)           | `150x150`                        | ❌       |
| `badge_sort_by`   | Arrange badge order (`issued`, `updated` or `accepted`) | `issued`                         | ❌       |
| `github_api_url`  | GitHub API URL (for GitHub Enterprise use)              | `https://api.github.com`         | ❌       |
| `github_token`    | GitHub token with write access to the repo              | `{github.token}`                 | ✅       |
| `github_repo`     | GitHub repository to update                             | `<username>/<repo>`              | ❌       |
| `github_branch`   | Branch where the target file is located                 | `main`                           | ❌       |
| `readme_file`     | Path to the markdown file to update                     | `README.md`                      | ❌       |
| `commit_message`  | Custom commit message for the update                    | `Updated README with new badges` | ❌       |

<!-- markdownlint-enable MD013 -->

#### 🔧 Complete Configuration Example

```yaml
name: Update Credly Badges

on:
  schedule:
    - cron: '0 0 * * *' # Runs daily at 00:00 UTC

jobs:
  update-readme:
    name: Update README with Credly badges

    runs-on: ubuntu-latest

    steps:
      - name: Update Badges in README
        uses: jd-35656/readme-credly-badges@v1
        with:
          credly_username: 'your-credly-username'
          badge_size: '150x150'
          badge_sort_by: 'issued'
          github_api_url: 'https://api.github.com'
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_repo: ${{ github.repository }}
          github_branch: 'main'
          readme_file: 'README.md'
          commit_message: 'Updated README with Credly badges'
```

---

## 🚀 Features

- Pulls badge data from [Credly](https://www.credly.com/) via their `.json`
  endpoint
- Filters out incomplete badge entries
- Auto-generates Markdown content with image and link per badge
- Supports:

  - Cron-based schedules
  - Manual dispatch
  - Push triggers

- Supports any markdown file (not just README)
- No API key or Credly auth required

---

## 📄 License

MIT © [jd-35656](https://github.com/jd-35656)
