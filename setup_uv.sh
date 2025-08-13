#!/bin/bash

# Setup script for uv environment
echo "🐾 Setting up uv environment for Animales Agent"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
uv venv
source .venv/bin/activate

# Install dependencies
echo "🔧 Installing project dependencies..."
uv pip install -r requirements.txt

# Install dev dependencies (optional)
read -p "Do you want to install development dependencies? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Installing development dependencies..."
    uv pip install pytest black isort
fi

echo "✅ Environment setup complete!"
echo ""
echo "To activate the environment:"
echo "   source .venv/bin/activate"
echo ""
echo "To test the agent:"
echo "   python test_animales_agent.py"
echo ""
echo "To run with Slack:"
echo "   python slack_app.py"
echo ""
echo "To deactivate the environment:"
echo "   deactivate" 