#!/bin/bash

# Local testing script for content automation
# Run this to test the content generation locally before pushing to GitHub

set -e  # Exit on error

echo "🧪 Testing Content Automation Locally"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Create it by running:"
    echo "  cp .env.example .env"
    echo "  nano .env  # Add your GROQ_API_KEY"
    echo ""
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python3 -c "import feedparser, openai" 2>/dev/null || {
    echo "❌ Missing dependencies. Install with:"
    echo "  pip3 install feedparser openai anthropic python-dotenv"
    exit 1
}

echo "✅ Dependencies OK"
echo ""

# Check if API key is set
if ! grep -q "GROQ_API_KEY=gsk_" .env; then
    echo "⚠️  Warning: GROQ_API_KEY not found in .env file"
    echo "   Make sure you've added your actual API key"
    echo ""
fi

# Run the script
echo "🚀 Running content generation..."
echo ""
python3 scripts/fetch_content.py

echo ""
echo "======================================"
echo "✅ Test complete!"
echo ""
echo "Check the generated files:"
echo "  - articles/sports/weekly-digest-*.html"
echo "  - articles-config.json (updated)"
echo ""
echo "To view in browser:"
echo "  open articles/sports/weekly-digest-*.html"
