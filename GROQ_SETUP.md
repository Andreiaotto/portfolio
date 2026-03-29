# Groq Integration - Quick Start

## ✨ Why Groq?

Groq is now the **default and recommended** AI provider for your automation because:

- ⚡ **Lightning Fast:** ~10x faster than Claude or GPT (inference in ~1 second)
- 💰 **FREE:** Generous free tier (30 requests/min, 6000/day = perfect for weekly content)
- 🎯 **High Quality:** Llama 3.3 70B rivals GPT-4 and Claude Opus
- 🔓 **No Wait:** No API waitlists or approval needed

## 🚨 CRITICAL: Security First

**You shared your API key publicly in the chat.** Anyone who saw it can use your Groq account.

### Immediate Action Required:

1. Go to [console.groq.com](https://console.groq.com)
2. Click on **API Keys** in left sidebar
3. Find the key starting with `gsk_HeRr2jnmPK3...`
4. Click **Delete** or **Revoke**
5. Click **Create API Key** to generate a new one
6. Copy the new key (starts with `gsk_...`)
7. **Never share it publicly again**

## ⚙️ Setup in 3 Steps

### Step 1: Add API Key to GitHub Secrets

1. Go to your GitHub repo: `https://github.com/Andreiaotto/portfolio`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GROQ_API_KEY`
5. Value: Your **NEW** API key (the regenerated one)
6. Click **Add secret**

### Step 2: (Optional) Set Provider

The default is already `groq`, but to be explicit:

1. Still in GitHub Secrets, click **New repository secret**
2. Name: `AI_PROVIDER`
3. Value: `groq`
4. Click **Add secret**

### Step 3: Test the Workflow

1. Go to **Actions** tab in your repo
2. Click **Weekly Content Update** workflow
3. Click **Run workflow** button
4. Select branch: `main`
5. Click **Run workflow**

Watch the logs to see:
```
🤖 Using AI provider: GROQ
Fetching RSS feeds...
  → swimming: https://swimswam.com/feed/
    Summarizing: Article Title...
✅ Generated HTML article: articles/sports/weekly-digest-2026-03-29.html
```

## 🎛️ Groq Configuration

### Available Models (in order of quality)

Edit line 85 in `scripts/fetch_content.py`:

```python
# Current default - Best overall
model="llama-3.3-70b-versatile"

# Alternative options:
# "llama-3.1-70b-versatile"  - Previous gen, still excellent
# "mixtral-8x7b-32768"       - Good for longer context (32k tokens)
# "gemma2-9b-it"             - Smaller, even faster
```

### Rate Limits (Free Tier)

- **Requests per minute:** 30
- **Requests per day:** 6,000
- **Your usage:** 8 articles per week = ~8 requests = well within limits

### Cost Comparison

| Provider | Monthly Cost | Speed | Quality |
|----------|-------------|-------|---------|
| **Groq** | **FREE** | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| Anthropic Claude | ~$2 | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| OpenAI GPT-4o | ~$0.30 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| OpenAI GPT-4o-mini | ~$0.02 | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |

## 🔄 Switching Providers

If you want to try Claude or OpenAI later:

### Switch to Anthropic Claude:
```bash
# Add these secrets:
ANTHROPIC_API_KEY=sk-ant-...
AI_PROVIDER=anthropic
```

### Switch to OpenAI:
```bash
# Add these secrets:
OPENAI_API_KEY=sk-...
AI_PROVIDER=openai
```

## 🐛 Troubleshooting

### Error: "Invalid API key"
- Did you regenerate the key after sharing it publicly?
- Did you copy the entire key including `gsk_` prefix?
- Check the secret name is exactly `GROQ_API_KEY` (case-sensitive)

### Error: "Rate limit exceeded"
- Unlikely with your usage (8 requests/week vs 6000/day limit)
- If it happens, wait 1 minute and retry

### Content quality not matching your style
- Edit the prompt in `scripts/fetch_content.py` line 58-81
- Add more specific instructions about your writing voice
- Test with different models (see configuration above)

## 📊 Monitoring Usage

Check your Groq usage dashboard:
1. Go to [console.groq.com](https://console.groq.com)
2. Click **Usage** in left sidebar
3. See requests per day, average latency, etc.

## ✅ Verification Checklist

Before first run:

- [ ] Old API key deleted from Groq console
- [ ] New API key generated
- [ ] `GROQ_API_KEY` added to GitHub Secrets
- [ ] Workflow manually triggered from Actions tab
- [ ] PR created successfully
- [ ] HTML article generated in correct format
- [ ] `articles-config.json` updated
- [ ] Content quality meets your standards

## 🎉 What's Different Now?

With Groq:
1. ✅ **No cost** - free tier is perfect for weekly automation
2. ✅ **Lightning fast** - workflow completes in ~30 seconds instead of 2-3 minutes
3. ✅ **High quality** - Llama 3.3 70B is on par with GPT-4 and Claude
4. ✅ **No waiting** - no API approval needed, start immediately

Your automation will:
- Run every Monday at 7am UTC
- Fetch 8 articles (2 per feed × 4 feeds)
- Generate HTML in your style
- Create PR for review
- Take ~30 seconds total

## 📝 Next Steps

1. **NOW:** Regenerate your Groq API key (the shared one is compromised)
2. Add `GROQ_API_KEY` to GitHub Secrets
3. Test with manual workflow trigger
4. Review the PR it creates
5. Merge to publish
6. Let it run automatically every Monday

---

**Questions?** Check [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) for full details or review the [script code](scripts/fetch_content.py).
