#!/bin/bash

echo "🚀 Setting up Azure AI Agent Workshop environment..."

# Update package manager
sudo apt-get update

# Install additional Python packages globally
echo "📦 Installing Python dependencies..."
pip install --upgrade pip

# Install Python dependencies for the workshop
pip install -r samples/python/01_basic_agent/requirements.txt
pip install -r samples/python/02_ai_search_rag/requirements.txt  
pip install -r samples/python/04_connected_agents/requirements.txt

# Install common Python development tools
pip install jupyter notebook ipykernel black flake8 isort pytest

# Setup .NET environment
echo "🔧 Setting up .NET environment..."
dotnet --version

# Restore NuGet packages for C# samples
echo "📦 Restoring .NET packages..."
cd samples/csharp
dotnet restore
cd ../..

# Install Azure CLI extensions
echo "⚡ Installing Azure CLI extensions..."
az extension add --name ai-foundry --upgrade --yes
az extension add --name ml --upgrade --yes

# Configure git (optional - users can override)
git config --global init.defaultBranch main
git config --global pull.rebase false

# Create workspace directories if they don't exist
mkdir -p workspace
mkdir -p logs

# Set permissions
chmod +x scripts/*.sh 2>/dev/null || true

# Display version information
echo ""
echo "✅ Environment setup complete!"
echo ""
echo "📋 Installed versions:"
echo "   Python: $(python --version)"
echo "   .NET: $(dotnet --version)"
echo "   Azure CLI: $(az --version | head -n 1)"
echo "   Node.js: $(node --version)"
echo "   Git: $(git --version)"
echo ""
echo "🎯 Ready to start the Azure AI Agent Workshop!"
echo "   👉 Open the README.md file to get started"
echo "   👉 Run 'az login' to authenticate with Azure"
echo ""