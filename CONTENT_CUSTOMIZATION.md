# Content Customization Guide

## ✅ What Was Fixed

### 1. Open Water Swimming Focus
- **Added keyword filtering** for open water swimming articles
- **Expanded keywords:** open water, marathon, 10k, 5k, distance, triathlon, ocean, lake, endurance, channel, crossing
- **Fallback:** If no open water articles found, uses general swimming content

### 2. Working Feeds
- ✅ **Open Water Swimming:** SwimSwam with open water filtering
- ✅ **Women's Health:** NIH Women's Health Research
- ✅ **Nutrition:** NIH Nutrition Research
- ✅ **Sports Science:** British Journal of Sports Medicine

### 3. HTML Styling
- **HTML fragments integrate with your existing site**
- Load through: `article-template.html?category=sports&article=weekly-digest-YYYY-MM-DD`
- CSS automatically applied from `styles/style.css`
- No changes needed to your site structure

---

## 🎨 How Styling Works

### Your Current Site Structure:
```html
<!-- article-template.html -->
<article class="body-home" id="article-content">
  <!-- Generated HTML gets injected here -->
</article>
```

### Generated Content Uses:
- `<h1>`, `<h2>`, `<h3>` for headings
- `<blockquote>` for quotes
- `<ul>`, `<li>` for lists
- `<strong>`, `<em>` for emphasis
- `<a>` for links

### Your CSS Already Styles These!
No changes needed - your `styles/style.css` already has rules for `.body-home h1`, `.body-home h2`, etc.

---

## 🏊 Improving Open Water Swimming Coverage

### Option 1: Add More Open Water Keywords

Edit `scripts/fetch_content.py` line 30-33:

```python
OPEN_WATER_KEYWORDS = [
    # Add your own keywords:
    "ultra swim", "33.3km", "Greece swim", "cold water",
    "channel swim", "marathon swim", "distance swimming"
]
```

### Option 2: Add Dedicated Open Water Feeds

If you find better open water swimming news sources:

```python
FEEDS = {
    "open_water_swimming": "https://your-open-water-source.com/feed/",
    # ... rest of feeds
}
```

### Option 3: Multiple Swimming Sources

```python
FEEDS = {
    "open_water_swimming_1": "https://swimswam.com/feed/",
    "open_water_swimming_2": "https://another-source.com/feed/",
    # ... rest
}
```

---

## 👩‍⚕️ Women's Health Content

Current source: **NIH Women's Health Research**
- Scientific, evidence-based
- Updates irregularly (research publication schedule)

### If You Want More Frequent Updates:

Add additional sources:

```python
FEEDS = {
    "women_health": "https://www.ncbi.nlm.nih.gov/feed/rss.cgi?ChanKey=womenshealth",
    "women_fitness": "https://www.outsideonline.com/health/feed/",  # Example
    # ...
}
```

---

## 🍎 Nutrition Content

Current source: **NIH Nutrition Research**
- Peer-reviewed research
- Evidence-based
- Updates regularly

### Alternative Nutrition Sources:

```python
"nutrition_science": "https://www.nutrition.org/feed/",  # American Society for Nutrition
"sports_nutrition": "https://www.issn.org/feed/",  # Int'l Society of Sports Nutrition
```

---

## 🎯 Content Tone Customization

### Current Tone:
- First-person, personal, reflective
- Evidence-based but conversational
- Motivational yet grounded
- Long-form with rich detail

### To Adjust Tone:

Edit `scripts/fetch_content.py` lines 58-81:

```python
prompt = f"""You are writing for andreiaotto.com — a personal portfolio by Andreia Otto.

The site's tone is:
- [YOUR TONE PREFERENCES HERE]
- [MODIFY THESE]
- [ADD MORE]

Write a 4-6 paragraph reflection that:
1. Opens with why this matters to YOU
2. [CUSTOMIZE STRUCTURE]
3. [CUSTOMIZE FOCUS]
4. Ends with practical takeaway
"""
```

---

## 📊 Content Volume Control

### Current Settings:
- **2 articles per feed** = 8 total articles/week
- **800 tokens** per summary (~600 words)

### To Change Volume:

**More articles per feed:**
```python
for entry in feed.entries[:2]:  # Change to [:3] or [:4]
```

**Longer summaries:**
```python
max_tokens=800,  # Change to 1000 or 1200
```

**More feeds:**
Just add more entries to the `FEEDS` dict!

---

## 🧪 Testing Content Changes

### Test Locally:
```bash
# Clean up previous test
rm articles/sports/weekly-digest-*.html

# Run with changes
source venv/bin/activate && python3 scripts/fetch_content.py

# View with styling
open "http://localhost:8000/article-template.html?category=sports&article=weekly-digest-$(date +%Y-%m-%d)"
```

### Test Specific Feed:
```bash
source venv/bin/activate && python3 -c "
import feedparser
feed = feedparser.parse('YOUR_FEED_URL')
print(f'Articles: {len(feed.entries)}')
for entry in feed.entries[:3]:
    print(f'  - {entry.title}')
"
```

---

## 🚀 When You're Happy With It

1. Clean up test files:
   ```bash
   rm articles/sports/weekly-digest-*.html
   ```

2. Commit your changes:
   ```bash
   git add scripts/fetch_content.py
   git commit -m "Update feeds and add open water swimming focus"
   git push
   ```

3. Test in GitHub Actions:
   - Go to Actions tab
   - Run workflow manually
   - Review the PR

4. Enable weekly automation (it's already scheduled for Monday 7am UTC)

---

## 📝 Quick Reference

| Want to... | Edit this... | Line(s) |
|------------|-------------|---------|
| Change feeds | `FEEDS` dict | 24-28 |
| Add open water keywords | `OPEN_WATER_KEYWORDS` | 31-34 |
| Change tone | `summarize()` prompt | 58-81 |
| More articles per feed | `feed.entries[:2]` | ~242 |
| Longer summaries | `max_tokens=800` | ~94 or ~103 |
| Change output location | `output_dir` | ~280 |

---

**Current Status:**
- ✅ Script configured for open water swimming focus
- ✅ Women's health and nutrition feeds working
- ✅ HTML integrates with existing site styling
- ✅ Ready for GitHub Actions testing

**View styled article:**
`http://localhost:8000/article-template.html?category=sports&article=weekly-digest-2026-03-29`
