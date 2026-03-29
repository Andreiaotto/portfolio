#!/usr/bin/env python3
"""
Automated content aggregator for andreiaotto.com
Fetches RSS feeds, summarizes with AI, generates HTML articles compatible with existing site structure
"""

import feedparser
import os
import datetime
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Load .env file for local testing (optional, won't fail if not present)
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    pass  # dotenv not installed (fine for GitHub Actions)

# Choose your AI provider: 'anthropic', 'openai', or 'groq'
AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

# RSS Feeds organized by category
FEEDS = {
    "sports": {
        "open_water_swimming": "https://swimswam.com/feed/",
        "sports_science": "https://bjsm.bmj.com/rss/current.xml",
    },
    "health": {
        "women_health": "https://www.ncbi.nlm.nih.gov/feed/rss.cgi?ChanKey=womenshealth",
        "nutrition": "https://www.ncbi.nlm.nih.gov/feed/rss.cgi?ChanKey=nutr",
    },
    "technology": {
        "sre_google": "https://cloud.google.com/blog/products/devops-sre/rss",
        "devops_weekly": "https://sreweekly.com/feed/",
    }
}

# Keywords to filter for open water swimming content
OPEN_WATER_KEYWORDS = [
    "open water", "openwater", "marathon", "10k", "10km", "5k", "5km",
    "distance", "triathlon", "ocean", "lake", "outdoor", "sea",
    "long distance", "endurance", "channel", "crossing"
]

# Category display names and descriptions
CATEGORY_INFO = {
    "sports": {
        "display_name": "Open Water Swimming & Sports Science",
        "description": "Latest insights on open water swimming, endurance training, and sports science research"
    },
    "health": {
        "display_name": "Women's Health & Nutrition",
        "description": "Evidence-based research on women's health and nutrition for athletes"
    },
    "technology": {
        "display_name": "SRE & Technology",
        "description": "Site Reliability Engineering practices, DevOps insights, and technical learnings"
    }
}


def is_open_water_content(title: str, summary: str) -> bool:
    """Check if content is related to open water swimming"""
    content = (title + " " + summary).lower()
    return any(keyword.lower() in content for keyword in OPEN_WATER_KEYWORDS)


def get_ai_client():
    """Initialize AI client based on provider"""
    if AI_PROVIDER == "openai":
        import openai
        return openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    elif AI_PROVIDER == "groq":
        import openai  # Groq uses OpenAI-compatible API
        return openai.OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1"
        )
    else:  # anthropic
        import anthropic
        return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def summarize(text: str, topic: str, title: str) -> str:
    """
    Summarize article content using AI.

    Args:
        text: Article content (summary or title)
        topic: Content category (swimming, women_health, nutrition, sports_science)
        title: Article title

    Returns:
        Rich HTML summary matching andreiaotto.com style
    """
    client = get_ai_client()

    prompt = f"""You are writing for andreiaotto.com — a personal portfolio by Andreia Otto, a software engineer and former athlete.

The site's tone is:
- First person, personal, and reflective
- Evidence-based but conversational
- Motivational yet grounded in reality
- Long-form with rich detail
- Uses strong HTML formatting (h2, h3, blockquotes, ul, li, strong, em)

Task: Transform this {topic} news article into a reflection/insight piece for Andreia's audience.

Original article: "{title}"
Content: {text}

Write a 4-6 paragraph reflection that:
1. Opens with why this matters to YOU (as Andreia, a former athlete/engineer)
2. Breaks down the key insights with evidence
3. Relates it to training, performance, or health optimization
4. Ends with a practical takeaway or call to action

Use semantic HTML: <h3> for subsections, <blockquote> for key quotes, <ul>/<li> for lists, <strong>/<em> for emphasis.
Write as if you're sharing this insight with fellow athletes and health-conscious engineers.

Return ONLY the HTML content (no <html>, <body>, or <h1> tags - just the article content)."""

    if AI_PROVIDER == "groq":
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Best balance of speed/quality
            # Alternative models: "llama-3.1-70b-versatile", "mixtral-8x7b-32768"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7,
        )
        return response.choices[0].message.content
    elif AI_PROVIDER == "openai":
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4o-mini" for lower cost
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7,
        )
        return response.choices[0].message.content
    else:  # anthropic
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text


def generate_html_article(category: str, items: List[Dict], week: str) -> str:
    """Generate category-specific HTML article"""

    category_info = CATEGORY_INFO[category]
    date_str = datetime.datetime.strptime(week, "%Y-%m-%d").strftime("%B %d, %Y")

    # Category-specific intros
    intros = {
        "sports": """<p>This week's insights from the world of open water swimming and sports science. As I train for my 33.3km swim in Greece, these findings shape my approach to endurance, technique, and performance optimization.</p>""",
        "health": """<p>This week's evidence-based research on women's health and nutrition. Understanding how physiology, hormones, and nutrition interact is crucial for optimizing training and recovery.</p>""",
        "technology": """<p>This week's learnings from the world of Site Reliability Engineering and DevOps. As a software engineer, these insights help me build more resilient systems and improve operational practices.</p>"""
    }

    # Category-specific reflections
    reflections = {
        "sports": """<h2>Applying to Training</h2>
<p>These insights directly impact my preparation for the 33.3km swim:</p>
<ul>
  <li><strong>Technique refinement</strong>: Incorporating findings on efficiency and endurance</li>
  <li><strong>Training periodization</strong>: Adjusting volume and intensity based on latest research</li>
  <li><strong>Mental preparation</strong>: Building resilience for ultra-distance challenges</li>
</ul>
<p><em>Every session in the water is informed by the latest science. That's how you optimize performance.</em></p>""",

        "health": """<h2>Practical Application</h2>
<p>Translating research into action for training and recovery:</p>
<ul>
  <li><strong>Nutrition timing</strong>: Optimizing fueling around training sessions</li>
  <li><strong>Cycle-aware training</strong>: Aligning intensity with physiological phases</li>
  <li><strong>Recovery protocols</strong>: Evidence-based approaches to adaptation</li>
</ul>
<p><em>Understanding the science helps me make better decisions about training, nutrition, and recovery.</em></p>""",

        "technology": """<h2>Engineering Takeaways</h2>
<p>Applying these insights to build better systems:</p>
<ul>
  <li><strong>Reliability practices</strong>: Implementing proven SRE patterns</li>
  <li><strong>Operational excellence</strong>: Learning from production incidents</li>
  <li><strong>System design</strong>: Building for resilience and observability</li>
</ul>
<p><em>Great engineering, like great training, is about consistent practice and learning from experience.</em></p>"""
    }

    html_content = f"""<h1>Weekly Insights: {category_info['display_name']}</h1>

<p><em>Date: {date_str}</em></p>

{intros[category]}

<hr>
"""

    for item in items:
        html_content += f"""
<h2><a href="{item['link']}" target="_blank" rel="noopener">{item['title']}</a></h2>

{item['summary']}

<p><strong>Source:</strong> <a href="{item['link']}" target="_blank" rel="noopener">Read the full article →</a></p>

<hr>
"""

    html_content += reflections[category]

    return html_content


def update_articles_config(week: str, category: str, category_display_name: str) -> None:
    """Update articles-config.json with new category-specific digest entry"""

    config_path = Path("articles/articles-config.json")

    with open(config_path, "r") as f:
        config = json.load(f)

    # Create article metadata
    article_id = f"{category}-digest-{week}"
    article_entry = {
        "id": article_id,
        "title": f"{category_display_name} Digest — {week}",
        "filename": f"{category}-digest-{week}.html",
        "description": CATEGORY_INFO[category]["description"]
    }

    # Check if article already exists
    if category in config["categories"]:
        existing_ids = [a["id"] for a in config["categories"][category]["articles"]]
        if article_id not in existing_ids:
            config["categories"][category]["articles"].insert(0, article_entry)  # Add at beginning
    else:
        print(f"⚠️  Category '{category}' not found in config")

    # Write back to file
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Updated articles-config.json: {category}/{article_id}")


def main():
    """Main execution: fetch feeds, summarize, generate separate HTML articles per category"""

    print(f"🤖 Using AI provider: {AI_PROVIDER.upper()}")
    print("Fetching RSS feeds...")

    week = datetime.date.today().strftime("%Y-%m-%d")
    os.environ["WEEK_DATE"] = week  # Export for GitHub Actions

    # Organize items by category
    items_by_category = {
        "sports": [],
        "health": [],
        "technology": []
    }

    # Fetch feeds for each category
    for category, feeds in FEEDS.items():
        print(f"\n📁 {category.upper()}")

        for topic, url in feeds.items():
            print(f"  → {topic}: {url}")
            try:
                feed = feedparser.parse(url)

                # For open water swimming, filter articles
                if topic == "open_water_swimming":
                    relevant_entries = []
                    for entry in feed.entries:
                        title = entry.get("title", "")
                        summary = entry.get("summary", entry.get("description", ""))
                        if is_open_water_content(title, summary):
                            relevant_entries.append(entry)
                            if len(relevant_entries) >= 2:
                                break

                    if not relevant_entries:
                        print(f"    ⚠️  No open water articles found, using general swimming")
                        relevant_entries = feed.entries[:2]

                    entries_to_process = relevant_entries
                else:
                    entries_to_process = feed.entries[:2]

                # Process selected articles
                for entry in entries_to_process:
                    title = entry.get("title", "Untitled")
                    link = entry.get("link", "#")
                    content = entry.get("summary", entry.get("description", title))

                    print(f"    Summarizing: {title[:60]}...")
                    summary = summarize(content, topic, title)

                    items_by_category[category].append({
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "topic": topic
                    })

            except Exception as e:
                print(f"    ⚠️  Error fetching {topic}: {e}")
                continue

    # Generate separate HTML articles for each category with content
    generated_files = []
    for category, items in items_by_category.items():
        if not items:
            print(f"\n⚠️  No items for {category}, skipping")
            continue

        print(f"\n📝 Generating {category} digest...")

        html_content = generate_html_article(category, items, week)

        # Ensure output directory exists
        output_dir = Path(f"articles/{category}")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{category}-digest-{week}.html"
        output_file.write_text(html_content)

        print(f"✅ Generated: {output_file} ({len(items)} articles)")
        generated_files.append((category, output_file, len(items)))

        # Update articles-config.json
        update_articles_config(week, category, CATEGORY_INFO[category]["display_name"])

    if not generated_files:
        print("\n⚠️  No content generated. Exiting.")
        return

    print("\n🎉 Content generation complete!")
    print(f"   Generated {len(generated_files)} digest articles:")
    for category, file_path, count in generated_files:
        print(f"   → {category}: {file_path.name} ({count} articles)")
    print("\n   → Review the PR, then merge to publish")


if __name__ == "__main__":
    main()
