# GitHub-Native Automation Stack Setup

This portfolio uses a fully GitHub-native automation stack for weekly content updates. No external services required.

## 🎯 How It Works

```
GitHub Action (cron schedule)
  ↓
Fetch RSS feeds
  ↓
Call AI API (Groq, Anthropic Claude, or OpenAI GPT) for summarization
  ↓
Generate HTML articles (matching your existing site format)
  ↓
Update articles-config.json automatically
  ↓
Open PR with new content
  ↓
You review + merge = published
```

## ✅ Format Compatibility

**IMPORTANT:** The automation generates HTML fragments that match your existing article structure perfectly:
- Articles are saved to `articles/sports/weekly-digest-YYYY-MM-DD.html`
- Uses the same HTML formatting as your existing articles (h1, h2, h3, blockquotes, ul/li)
- Automatically updates `articles-config.json` to register new articles
- Loads via your existing `article-loader.js` system
- No changes needed to your website structure

## ✅ Setup Instructions

### 1. Choose Your AI Provider and Add API Key

You have three options:

#### Option A: **Groq** (✨ Recommended - Fast & Free!)
- **Best for:** Lightning-fast generation with excellent quality
- **Cost:** **FREE** tier available (generous limits: 30 requests/min, 6000 requests/day)
- **Speed:** ~10x faster than other providers
- **Model:** Llama 3.3 70B (very high quality)
- **Setup:**
  1. Get API key from [console.groq.com](https://console.groq.com)
  2. Go to GitHub repo → **Settings** → **Secrets and variables** → **Actions**
  3. Add secret: `GROQ_API_KEY` with value starting with `gsk_...`
  4. (Optional) Add secret: `AI_PROVIDER` with value `groq` (this is now the default)

#### Option B: **Anthropic Claude** (Best for quality)
- **Best for:** Highest-quality, most nuanced content
- **Cost:** ~$2/month for 4-8 weekly digests (using Claude Opus)
- **Setup:**
  1. Get API key from [console.anthropic.com](https://console.anthropic.com/)
  2. Go to GitHub repo → **Settings** → **Secrets and variables** → **Actions**
  3. Add secret: `ANTHROPIC_API_KEY` with value starting with `sk-ant-...`
  4. Add secret: `AI_PROVIDER` with value `anthropic`

#### Option C: **OpenAI GPT** (Alternative)
- **Best for:** Reliable, well-known provider
- **Cost:** ~$0.02-2/month using GPT-4o-mini or GPT-4o
- **Setup:**
  1. Get API key from [platform.openai.com](https://platform.openai.com/)
  2. Go to GitHub repo → **Settings** → **Secrets and variables** → **Actions**
  3. Add secret: `OPENAI_API_KEY` with value starting with `sk-...`
  4. Add secret: `AI_PROVIDER` with value `openai`

**Note:** The script defaults to **Groq** (free and fast!). It auto-detects which provider to use.

### 2. Verify Workflow Configuration

The workflow is already configured at [.github/workflows/content-update.yml](.github/workflows/content-update.yml)

**Default schedule:** Every Monday at 7am UTC

To change the schedule, edit the cron expression:
```yaml
schedule:
  - cron: '0 7 * * 1'  # minute hour day month weekday
```

Examples:
- `0 7 * * 1` - Every Monday at 7am UTC
- `0 9 * * 3` - Every Wednesday at 9am UTC
- `0 12 * * *` - Every day at noon UTC
- `0 6 * * 1,4` - Every Monday and Thursday at 6am UTC

### 3. Test the Workflow

**Manual trigger:**
1. Go to **Actions** tab in your GitHub repository
2. Click **Weekly Content Update** workflow
3. Click **Run workflow** dropdown
4. Select branch (usually `main`)
5. Click **Run workflow**

This will:
- Fetch latest articles from RSS feeds
- Transform them into reflective insights matching your writing style
- Generate a properly formatted HTML article
- Update your articles-config.json
- Create a PR with the new content

### 4. Review and Merge

When a PR is created:
1. Review the generated summaries
2. Check tone matches your style
3. Verify links work
4. Merge when satisfied
5. Content is published automatically (if using GitHub Pages)

## 🎛️ Customization Options

### Change RSS Feeds

Edit [scripts/fetch_content.py](scripts/fetch_content.py):

```python
FEEDS = {
    "swimming": "https://swimswam.com/feed/",
    "women_health": "https://feeds.feedburner.com/nih-womens-health",
    "nutrition": "https://examine.com/feed/",
    "sports_science": "https://bjsm.bmj.com/rss/current.xml",
}
```

### Adjust Content Tone

Edit the system prompt in the `summarize()` function:

```python
content = f"""You are writing for andreiaotto.com — a portfolio focused on elite swimming, women's health, sports science, and nutrition.

Summarize this {topic} article in 3 sentences, first person perspective, evidence-based tone, no hype or promotional language.

Article content:
{text}"""
```

### Change Number of Articles

In `fetch_content.py`, around line 150:

```python
for entry in feed.entries[:2]:  # Change from 2 to desired number
```

### Change Output Location

In `fetch_content.py`, around line 230:

```python
output_dir = Path("articles/sports")  # Change category if desired
# Also update line 240 to change the category in articles-config.json
update_articles_config(week, "sports")  # Change "sports" to your preferred category
```

### Switch AI Provider

Three ways to switch providers:

1. **Via GitHub Secret**: Set `AI_PROVIDER` to `groq`, `openai`, or `anthropic`
2. **Via Environment Variable**: In workflow file, change `AI_PROVIDER: 'groq'`
3. **Via Script**: Edit line 15 in `fetch_content.py`:
   ```python
   AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")  # Change default
   ```

### Available Groq Models

If you want to change the Groq model, edit line 85 in `fetch_content.py`:

```python
model="llama-3.3-70b-versatile",  # Current default - best quality
# Alternatives:
# "llama-3.1-70b-versatile"  - Previous generation, still excellent
# "mixtral-8x7b-32768"       - Good for longer context
# "gemma2-9b-it"             - Smaller, faster model
```

## 📊 What You Control

| Decision | Where to Change | Current Value |
|----------|----------------|---------------|
| AI Provider | `AI_PROVIDER` secret or env var | `groq` (default) |
| Which feeds | `FEEDS` dict in script | SwimSwam, NIH, Examine, BJSM |
| Tone/voice | System prompt in `summarize()` | First person, reflective, evidence-based |
| Frequency | `cron` in workflow | Monday 7am UTC |
| Articles per feed | `feed.entries[:2]` | Top 2 per feed (8 total) |
| Output location | `output_dir` path | `articles/sports/` |
| Output format | `generate_html_article()` | HTML fragments (site-compatible) |
| AI model | `model` parameter | `llama-3.3-70b-versatile` (Groq), `claude-opus-4-6`, or `gpt-4o` |
| Content length | `max_tokens` parameter | 800 tokens (~600 words) |

## 🔒 Security

- API keys are stored securely in GitHub Secrets
- Secrets are never logged or exposed in PR content
- Each PR branch is isolated and can be reviewed before merging
- Full audit trail via Git history

## 🐛 Troubleshooting

### Workflow not running on schedule

- **Cause:** Scheduled workflows may be disabled on inactive repos
- **Fix:** Manually trigger once to reactivate, or push a commit

### API key errors

- **Error:** `Authentication error: Invalid API key`
- **Fix:** Verify your API key secret (`GROQ_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`) is correctly set in GitHub Secrets
- **Fix:** Make sure `AI_PROVIDER` matches which key you added
- **Groq-specific:** If you see "invalid key", regenerate your key at [console.groq.com](https://console.groq.com)

### Feed parsing errors

- **Error:** `Error fetching {topic}: ...`
- **Fix:** Check if RSS feed URL is still valid, update FEEDS dict if needed

### PR not created

- **Check:** GitHub Actions logs in the Actions tab
- **Common issues:**
  - No new content (all feeds empty)
  - Permissions issue (need write access)
  - Branch already exists from previous run

## 📝 Next Steps

1. ✅ **IMPORTANT: Regenerate your Groq API key** (the one shared earlier is now public - delete it immediately at [console.groq.com](https://console.groq.com) and create a new one)
2. ✅ Add `GROQ_API_KEY` to GitHub Secrets with your NEW key
3. ✅ (Optional) Add `AI_PROVIDER` secret with value `groq` (or leave blank, it's the default)
4. ✅ Test with manual workflow trigger from Actions tab
5. ✅ Review first generated PR (check HTML format, tone, integration)
6. ✅ Adjust feeds/tone/frequency as needed
7. ✅ Merge and let automation run weekly

## 🎉 Benefits

✅ **PR = human review gate** — you approve before publish
✅ **Git history = audit trail** — every content decision tracked
✅ **No external infrastructure** — pure GitHub + AI API
✅ **Secrets management** — built-in via GitHub
✅ **Format compatibility** — generates HTML matching existing articles
✅ **Auto-integration** — updates articles-config.json automatically
✅ **Lightning-fast & FREE** — Groq is free and ~10x faster than alternatives
✅ **Merge = deploy** — if using GitHub Pages, it's instant

---

*Questions or issues? Review the [workflow file](.github/workflows/content-update.yml) or [script](scripts/fetch_content.py).*
