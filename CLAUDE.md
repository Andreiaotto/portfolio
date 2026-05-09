# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static personal portfolio site hosted on GitHub Pages, with a Python automation layer that fetches RSS feeds, summarizes them via AI, and opens PRs with new HTML articles weekly.

No build step. No framework. No package manager for the frontend.

## Running & testing

Install Python dependencies:
```
pip install feedparser openai anthropic python-dotenv
```

Test content generation locally:
```
./test_local.sh
# or directly:
python3 scripts/fetch_content.py
```

Requires a `.env` file with at least one AI provider key. See `.env.example`. Groq is the default and has a free tier.

## Architecture

### Frontend (static)
- `index.html` — home page
- `article-template.html` — shell used to render every article
- `article-loader.js` — client-side routing via URL params (`?category=X&article=Y`); loads article HTML fragments into the template
- `home-nav.js` — builds the navbar dynamically from `articles-config.json`
- `articles-config.json` — master registry; every article must be registered here with `{ title, file, date, summary, category }`

### Content
Articles live in `/articles/{category}/` as standalone HTML fragments (not full documents). The six categories are: Technology, Sports, Finance, Health, Living Abroad, Dogs.

### Automation (`scripts/fetch_content.py`)
- Parses RSS feeds (SwimSwam, NIH Women's Health, NIH Nutrition, BJSM)
- Summarizes each item with Groq/OpenAI/Anthropic (~800 tokens, Andreia's first-person voice)
- Writes HTML files to the appropriate `/articles/{category}/` directory
- Appends entries to `articles-config.json`
- GitHub Actions (`content-update.yml`) runs this every Monday at 07:00 UTC, then opens a PR

### Adding a new article manually
1. Write an HTML fragment in `/articles/{category}/your-article.html` — use semantic tags (`h1`–`h3`, `blockquote`, `ul/li`, `strong`, `em`, `a`); no `<html>`/`<body>` wrapper
2. Add an entry to `articles-config.json`

### Changing AI providers
Set `AI_PROVIDER` in `.env` to `groq` (default), `openai`, or `anthropic`. Groq uses `llama-3.3-70b-versatile` and is free up to 6000 req/day.

## CI/CD
`.github/workflows/content-update.yml` — weekly content automation. Needs `GROQ_API_KEY` (or equivalent) set as a GitHub Actions secret. The workflow creates a PR; it does not push directly to `main`.
