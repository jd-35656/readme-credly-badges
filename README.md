# 🛡️ readme-credly-badges

[![Latest Release](https://img.shields.io/github/release/jd-35656/readme-credly-badges.svg?style=flat-square)](https://github.com/jd-35656/readme-credly-badges/releases)
[![License](https://img.shields.io/github/license/jd-35656/readme-credly-badges?style=flat-square)](LICENSE)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-readme--credly--badges-blue?logo=github&style=flat-square)](https://github.com/marketplace/actions/readme-credly-badges)

A GitHub Action that automatically updates your `README.md` (or any markdown file) with your [Credly](https://www.credly.com/) badge details — no manual edits required!

---

## 📸 Example Output

![Credly Sample Badges Image](assets/badge-sample.png)

---

## 🚀 Quickstart

### 1. Mark the Badge Area

Add the following comment markers to your `README.md` (or any markdown file) where you want the Credly badges to appear:

```md
<!-- START CREDLY BADGES -->
<!-- END CREDLY BADGES -->
```

The Action will replace everything between these markers with your latest badges.

---

### 2. Create the GitHub Workflow

Create a workflow file at `.github/workflows/update-badges.yaml`:

```yaml
name: Update Credly Badges

on:
  schedule:
    - cron: '0 0 * * *' # Runs daily at 00:00 UTC
  workflow_dispatch: # Optional: allows manual trigger

permissions:
  contents: write # Required if using the default GITHUB_TOKEN

jobs:
  update-readme:
    name: Update README with Credly Badges
    runs-on: ubuntu-latest

    steps:
      - name: Update Badges in README
        uses: jd-35656/readme-credly-badges@v1
        with:
          credly_username: 'your-credly-username'
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

> 🔐 **Note:**
> If you're using a **Personal Access Token** (e.g., `secrets.MY_PAT`), ensure it has the `contents:write` scope. In this case, the `permissions:` block is not necessary.
>
> Likewise, if you've explicitly enabled **write access for the default `GITHUB_TOKEN`** in your repository’s **Actions → General → Workflow permissions** settings, you may safely omit the `permissions:` block as well.

---

## ⚙️ Configuration Options

| Input Name        | Description                                    | Default                          | Required |
| ----------------- | ---------------------------------------------- | -------------------------------- | -------- |
| `credly_username` | Your Credly username                           | `${{ github.actor }}`            | ❌       |
| `badge_size`      | Badge image size (e.g., `150x150`, `680x680`)  | `150x150`                        | ❌       |
| `badge_sort_by`   | Sort order: `issued`, `updated`, or `accepted` | `issued`                         | ❌       |
| `github_api_url`  | GitHub API URL (for GitHub Enterprise use)     | `https://api.github.com`         | ❌       |
| `github_token`    | Token with write access to the repo            | `${{ github.token }}`            | ✅       |
| `github_repo`     | Target GitHub repository                       | `${{ github.repository }}`       | ❌       |
| `github_branch`   | Branch where the target file is located        | `main`                           | ❌       |
| `readme_file`     | Path to the markdown file to update            | `README.md`                      | ❌       |
| `commit_message`  | Custom commit message                          | `Updated README with new badges` | ❌       |

---

## 🧪 Full Example

```yaml
name: Update Credly Badges

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-readme:
    name: Update README with Credly Badges
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

## ✅ Features

- ✅ Automatically fetches your public Credly badges
- ✅ Filters out revoked or incomplete badges
- ✅ Embeds clickable badge images directly into markdown
- ✅ Supports:

  - Manual workflow dispatch
  - Scheduled cron jobs
  - GitHub Enterprise
  - Any markdown file (not just `README.md`)

- ✅ No Credly API key or login required

---

## 📄 License

MIT © [jd-35656](https://github.com/jd-35656)
