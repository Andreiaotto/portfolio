# Local Testing Guide

## Quick Setup (2 minutes)

### 1. Install Python Dependencies

```bash
cd /Users/ottoand/Library/CloudStorage/OneDrive-adidas/Documents/Adidas/Work/otto-portfolio/portfolio

# Install required packages
pip3 install feedparser openai anthropic python-dotenv
```

### 2. Create .env File

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual API key
# You can use nano, vim, or any text editor:
nano .env
```

**In the `.env` file, add your Groq API key:**

```bash
GROQ_API_KEY=gsk_your_actual_key_from_github_secrets
AI_PROVIDER=groq
```

> **Important:** Get your actual key from [console.groq.com](https://console.groq.com) → API Keys → Copy the same key you added to GitHub Secrets.

### 3. Run the Script

```bash
# Make sure you're in the project directory
cd /Users/ottoand/Library/CloudStorage/OneDrive-adidas/Documents/Adidas/Work/otto-portfolio/portfolio

# Run the content generation script
python3 scripts/fetch_content.py
```

## What to Expect

When you run the script, you should see:

```
🤖 Using AI provider: GROQ
Fetching RSS feeds...
  → swimming: https://swimswam.com/feed/
    Summarizing: Article Title...
  → women_health: https://feeds.feedburner.com/nih-womens-health
    Summarizing: Article Title...
  → nutrition: https://examine.com/feed/
    Summarizing: Article Title...
  → sports_science: https://bjsm.bmj.com/rss/current.xml
    Summarizing: Article Title...

✅ Generated HTML article: articles/sports/weekly-digest-2026-03-29.html
   Total insights: 8

✅ Updated articles-config.json with new digest

🎉 Content generation complete!
   → Review the PR, then merge to publish
```

### Expected Output Files

After running successfully:
- **New HTML article:** `articles/sports/weekly-digest-2026-03-29.html`
- **Updated config:** `articles-config.json` (new entry added)

## Viewing the Generated Content

### Option 1: View HTML directly
```bash
# Open in browser
open articles/sports/weekly-digest-2026-03-29.html
```

### Option 2: View via your local site
If you have a local web server running, navigate to:
```
http://localhost:8000/article-template.html?category=sports&article=weekly-digest-2026-03-29
```

### Option 3: Check the raw HTML
```bash
# View in terminal
cat articles/sports/weekly-digest-2026-03-29.html
```

## Troubleshooting

### Error: "No module named 'feedparser'"
```bash
pip3 install feedparser openai anthropic
```

### Error: "GROQ_API_KEY not found"
- Make sure `.env` file exists in project root
- Check the key is on a line: `GROQ_API_KEY=gsk_...`
- No spaces around the `=` sign
- No quotes around the key value

### Error: "Invalid API key"
- Your API key might be wrong
- Go to [console.groq.com](https://console.groq.com) and verify your key
- Copy the exact key (starts with `gsk_`)
- Make sure it's the NEW key (after you deleted the old one)

### Error: "Failed to load articles configuration"
- This is normal on first run
- The script will create the entries it needs

### Script runs but generates low-quality content
- Try adjusting the prompt in `scripts/fetch_content.py` (lines 58-81)
- Or switch to a different AI provider (Claude for highest quality)

## Testing Different Providers

### Test with Groq (current default)
```bash
# In .env file:
GROQ_API_KEY=gsk_your_key
AI_PROVIDER=groq
```

### Test with Anthropic Claude
```bash
# In .env file:
ANTHROPIC_API_KEY=sk-ant-your_key
AI_PROVIDER=anthropic
```

### Test with OpenAI
```bash
# In .env file:
OPENAI_API_KEY=sk-your_key
AI_PROVIDER=openai
```

## Cleaning Up Test Files

After testing, you can remove generated files:

```bash
# Remove test article (optional)
rm articles/sports/weekly-digest-*.html

# Restore articles-config.json (if you want)
git checkout articles-config.json
```

## Running Locally vs GitHub Actions

| Aspect | Local Testing | GitHub Actions |
|--------|--------------|----------------|
| **API Key Source** | `.env` file | GitHub Secrets |
| **Timing** | Manual (run anytime) | Automated (Monday 7am UTC) |
| **PR Creation** | No PR created | Automatically creates PR |
| **Environment** | Your machine | Ubuntu runner |
| **Purpose** | Testing/debugging | Production automation |

## Best Practice Workflow

1. **Test locally first** - Run script, check output quality
2. **Adjust if needed** - Tweak prompts, feeds, settings
3. **Commit changes** - Push to GitHub
4. **Test in GitHub Actions** - Manual workflow trigger
5. **Enable automation** - Let it run weekly

## Security Note

**Never commit your `.env` file!**

The `.gitignore` is already configured to exclude it, but double-check:

```bash
# Verify .env is ignored
git status

# You should NOT see .env in the list
```

---

**Ready to test?** Run `python3 scripts/fetch_content.py` and see your content generated locally!
