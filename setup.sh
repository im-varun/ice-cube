#!/bin/bash

echo "Setting up IceCube development environment..."

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"
echo "export PYTHONPATH=\"\${PYTHONPATH}:$(pwd)/lib\"" >> ~/.bashrc

# Install pre-commit
echo "Installing pre-commit and Ruff pre-commit hooks..."
pip install --user pre-commit

# Optionally upgrade pre-commit to latest for best compatibility
pip install --user --upgrade pre-commit

# Install Ruff pre-commit hooks defined in .pre-commit-config.yaml
pre-commit install

# Create .gitkeep files so that git can track empty directories as well
touch data/raw/.gitkeep data/cleaned/.gitkeep

echo "Setup complete! Run 'source ~/.bashrc' to activate PYTHONPATH"
echo "You can now use 'git commit' and Ruff will automatically lint and format your code."
