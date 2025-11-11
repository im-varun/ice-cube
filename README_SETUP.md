# IceCube Setup Guide

## Step-by-Step Setup

### 1. Create Project Structure

```bash
chmod +x create_structure.sh
./create_structure.sh
```

### 2. Set PYTHONPATH

```bash
# For current session
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"

# To make it permanent, add to your shell config:
echo 'export PYTHONPATH="${PYTHONPATH}:'"$(pwd)/lib"'"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Setup Pre-commit Hooks

```bash
chmod +x setup_precommit.sh
./setup_precommit.sh
```

### 4. (Optional) Install Linter

```bash
pip install pycodestyle --user
```

That's it! Start coding. 🚀

## Testing Your Setup

```bash
# Test if pre-commit works
git add .
git commit -m "test: initial commit"

# Should see:
# 🔍 Running pre-commit checks...
# ✓ All files have valid Python syntax
# ...
```

## Quick Reference

```bash
# Check code style manually
pycodestyle src/ui/app.py

# Run tests
pytest tests/

# See git hooks
cat .git/hooks/pre-commit
```
