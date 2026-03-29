# Quick Start - Test Locally in 3 Commands

## Copy & Paste This:

```bash
# 1. Install dependencies
pip3 install feedparser openai anthropic python-dotenv

# 2. Create .env file (copy example)
cp .env.example .env

# 3. Edit .env and add your Groq API key
nano .env
```

**In nano, change this line:**
```
GROQ_API_KEY=gsk_your_key_here
```

**To your actual key from [console.groq.com](https://console.groq.com):**
```
GROQ_API_KEY=gsk_YourActualKeyHere123456789
```

Save with `Ctrl+O`, then `Enter`, then exit with `Ctrl+X`.

## Run the Test:

```bash
# Option 1: Use the test script
./test_local.sh

# Option 2: Run directly
python3 scripts/fetch_content.py
```

## Expected Output:

```
🤖 Using AI provider: GROQ
Fetching RSS feeds...
  → swimming: https://swimswam.com/feed/
    Summarizing: Article Title...
    (... more articles ...)
✅ Generated HTML article: articles/sports/weekly-digest-2026-03-29.html
   Total insights: 8
✅ Updated articles-config.json with new digest
🎉 Content generation complete!
```

## View Results:

```bash
# Open the generated article in browser
open articles/sports/weekly-digest-$(date +%Y-%m-%d).html
```

---

**That's it!** If it works locally, it'll work in GitHub Actions. 🎉

Full details: [LOCAL_TESTING.md](LOCAL_TESTING.md)
