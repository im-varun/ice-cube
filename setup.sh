#!/bin/bash

echo "🏒 Setting up IceCube development environment..."

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"
echo "export PYTHONPATH=\"\${PYTHONPATH}:$(pwd)/lib\"" >> ~/.bashrc

# Install pre-commit
echo "Installing pre-commit hooks..."
pip install pre-commit --user
pre-commit install

# Create .gitkeep files so that git can track empty directories as well
touch data/raw/.gitkeep data/cleaned/.gitkeep logs/.gitkeep

echo "Setup complete! Run 'source ~/.bashrc' to activate PYTHONPATH"
