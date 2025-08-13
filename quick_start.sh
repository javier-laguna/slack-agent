#!/bin/bash

echo "🐾 Quick Start - Animales Agent with Slack"
echo "=========================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv installed successfully!"
    echo ""
fi

# Setup environment
echo "📦 Setting up uv environment..."
./setup_uv.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Gemini API key and Slack tokens"
echo "2. Activate the virtual environment: source .venv/bin/activate"
echo "3. Test the agent: python test_animales_agent.py"
echo "4. Run with Slack: python slack_app.py"
echo ""
echo "Example .env format:"
echo "GEMINI_API_KEY=AIzaSyC..."
echo "SLACK_BOT_TOKEN=xoxb-..."
echo "SLACK_SOCKET_TOKEN=xapp-..." 