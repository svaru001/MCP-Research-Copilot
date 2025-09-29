#!/bin/bash

# Development setup script for MCP servers

set -e

echo "🛠️ Setting up MCP Server Development Environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual API keys"
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

# Make scripts executable
chmod +x run_share_price.py
chmod +x run_pinecone.py
chmod +x main.py

echo "✅ Development setup complete!"
echo ""
echo "To run servers:"
echo "  Share Price Server: python run_share_price.py"
echo "  Pinecone Server: python run_pinecone.py"
echo "  Both servers: python main.py both"
echo ""
echo "To activate virtual environment:"
echo "  source .venv/bin/activate"
