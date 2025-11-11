#!/bin/bash

echo "🚀 Setting up simple pre-commit hooks for IceCube..."

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create simple pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

echo "🔍 Running pre-commit checks..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Flag to track if any check fails
FAILED=0

# Get list of Python files being committed
PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -z "$PYTHON_FILES" ]; then
    echo -e "${GREEN}✓ No Python files to check${NC}"
    exit 0
fi

echo "Files to check:"
echo "$PYTHON_FILES"
echo ""

# ============================================
# Check 1: Basic Python Syntax
# ============================================
echo "1. Checking Python syntax..."
for file in $PYTHON_FILES; do
    python3 -m py_compile "$file" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Syntax error in $file${NC}"
        python3 -m py_compile "$file"
        FAILED=1
    fi
done

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All files have valid Python syntax${NC}"
fi
echo ""

# ============================================
# Check 2: Basic Code Style (pycodestyle)
# ============================================
echo "2. Checking code style (PEP 8)..."

# Check if pycodestyle is available
if command -v pycodestyle &> /dev/null; then
    for file in $PYTHON_FILES; do
        # Run pycodestyle with relaxed rules
        pycodestyle --max-line-length=100 --ignore=E203,W503,E501 "$file"
        if [ $? -ne 0 ]; then
            FAILED=1
        fi
    done
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}✓ Code style looks good${NC}"
    fi
else
    echo -e "${YELLOW}⚠ pycodestyle not installed, skipping style check${NC}"
    echo "  Install with: pip install pycodestyle --user"
fi
echo ""

# ============================================
# Check 3: No print statements (use logger)
# ============================================
echo "3. Checking for print statements..."
PRINT_COUNT=0
for file in $PYTHON_FILES; do
    # Skip test files
    if [[ $file == *"test_"* ]] || [[ $file == *"/tests/"* ]]; then
        continue
    fi
    
    # Check for print statements (excluding comments)
    PRINTS=$(grep -n "^\s*print(" "$file" | grep -v "#.*print(")
    if [ ! -z "$PRINTS" ]; then
        echo -e "${YELLOW}⚠ Found print statements in $file:${NC}"
        echo "$PRINTS"
        echo "  Consider using logger instead"
        PRINT_COUNT=$((PRINT_COUNT + 1))
    fi
done

if [ $PRINT_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ No print statements found (good!)${NC}"
fi
echo ""

# ============================================
# Check 4: No TODO/FIXME without issue number
# ============================================
echo "4. Checking for untracked TODOs..."
TODO_COUNT=0
for file in $PYTHON_FILES; do
    # Look for TODO/FIXME without (#issue_number)
    TODOS=$(grep -n "TODO\|FIXME" "$file" | grep -v "#[0-9]")
    if [ ! -z "$TODOS" ]; then
        echo -e "${YELLOW}⚠ Found untracked TODO/FIXME in $file:${NC}"
        echo "$TODOS"
        echo "  Add issue number like: # TODO(#42): description"
        TODO_COUNT=$((TODO_COUNT + 1))
    fi
done

if [ $TODO_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ All TODOs are tracked${NC}"
fi
echo ""

# ============================================
# Check 5: No large files
# ============================================
echo "5. Checking file sizes..."
LARGE_FILES=0
for file in $PYTHON_FILES; do
    SIZE=$(wc -l < "$file")
    if [ $SIZE -gt 500 ]; then
        echo -e "${YELLOW}⚠ $file has $SIZE lines (consider splitting)${NC}"
        LARGE_FILES=$((LARGE_FILES + 1))
    fi
done

if [ $LARGE_FILES -eq 0 ]; then
    echo -e "${GREEN}✓ All files are reasonably sized${NC}"
fi
echo ""

# ============================================
# Final Result
# ============================================
if [ $FAILED -ne 0 ]; then
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}❌ Pre-commit checks FAILED${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo "Please fix the errors above and try again."
    echo "Or use 'git commit --no-verify' to skip checks (not recommended)"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ All pre-commit checks PASSED${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
exit 0
EOF

# Make the hook executable
chmod +x .git/hooks/pre-commit

# Create simple .pycodestyle config
cat > .pycodestyle << 'EOF'
[pycodestyle]
max-line-length = 100
ignore = E203,W503,E501
exclude = lib/,.venv/,build/,dist/
EOF

# Create simplified .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*.sublime-*

# Database
*.db
*.sqlite3
*.db-journal

# Data files
data/raw/*
!data/raw/.gitkeep
data/cleaned/*
!data/cleaned/.gitkeep

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
.DS_Store?

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Build
build/
dist/
*.egg-info/

# Temporary
tmp/
temp/
*.tmp
*~
EOF

# Create simple requirements-dev.txt
cat > requirements-dev.txt << 'EOF'
# Simple linting tool (optional but recommended)
pycodestyle>=2.11.0

# Testing (optional)
pytest>=7.4.0
EOF

# Create updated CONTRIBUTING.md
cat > CONTRIBUTING.md << 'EOF'
# Contributing to IceCube

## Quick Setup (First Time Only)

```bash
# 1. Clone and setup structure
git clone <repo-url>
cd icecube
./create_structure.sh

# 2. Set Python path for lib/ directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"
# Add to your shell config to persist:
echo 'export PYTHONPATH="${PYTHONPATH}:'"$(pwd)/lib"'"' >> ~/.bashrc

# 3. Setup pre-commit hooks
./setup_precommit.sh

# 4. (Optional) Install linter
pip install pycodestyle --user
```

## Daily Workflow

### 1. Start Working

```bash
# Always start from develop branch
git checkout develop
git pull origin develop

# Create your feature branch
git checkout -b feature/your-feature-name
```

### 2. Code in Your Directory

**Work ONLY in your assigned directory:**
- **UI Developer**: `src/ui/`
- **Controller Developer**: `src/controllers/`  
- **Database Developer**: `src/database/`

### 3. Before Committing

The pre-commit hook will automatically check:
- ✅ Python syntax is valid
- ✅ Basic PEP 8 style (if pycodestyle installed)
- ⚠️  No print statements (warnings only)
- ⚠️  TODOs are tracked (warnings only)
- ⚠️  Files aren't too large (warnings only)

**Fix any errors** that block your commit.

### 4. Commit Your Changes

```bash
# Stage your changes
git add src/ui/screens/home_screen.py

# Commit (pre-commit hook runs automatically)
git commit -m "feat: add home screen layout"

# If you need to bypass checks (rarely):
git commit --no-verify -m "wip: saving work"
```

### 5. Push and Create PR

```bash
# Push your branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub/GitLab
```

## Commit Message Format

Use this simple format:

```
<type>: <description>

[optional body]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```bash
git commit -m "feat: add player stats widget"
git commit -m "fix: resolve query timeout issue"
git commit -m "docs: update database schema docs"
```

## Code Style Guidelines

### Keep It Simple

```python
# Good: Clear and simple
def get_player_name(player_id: int) -> str:
    """Get player name by ID."""
    return query_db(f"SELECT name FROM players WHERE id = {player_id}")

# Bad: Overly complex
def get_player_name(player_id: int) -> str:
    """
    This function retrieves the name of a player from the database
    using the player's unique identifier...
    """
    # ... 10 lines of unnecessary code
```

### Use Type Hints

```python
# Good
def calculate_score(points: int, multiplier: float) -> float:
    return points * multiplier

# Bad
def calculate_score(points, multiplier):
    return points * multiplier
```

### Use Logger, Not Print

```python
# Good
from shared.logger import get_logger
logger = get_logger(__name__)
logger.info("Query executed successfully")

# Bad
print("Query executed successfully")
```

### Keep Functions Small

- One function = one responsibility
- Aim for < 50 lines per function
- If longer, consider splitting

## Avoiding Merge Conflicts

### Golden Rules

1. **Stay in your directory** - Don't modify other team members' files
2. **Pull frequently** - `git pull origin develop` at least daily
3. **Shared files** - Create an issue first, discuss with team

### Shared Files (Need Coordination)

Files in `src/shared/` are used by everyone:
1. Create an issue describing the change
2. Get approval from team
3. Make the change
4. Notify everyone in team chat

## Testing Your Code

```bash
# Run tests for your module
pytest tests/test_ui/          # UI tests
pytest tests/test_controllers/ # Controller tests
pytest tests/test_database/    # Database tests

# Run all tests
pytest tests/

# Run with output
pytest tests/ -v
```

## Getting Help

- **Syntax errors?** Read the error message carefully
- **Style warnings?** They won't block commits, fix when convenient
- **Merge conflicts?** Ask in team chat immediately
- **Not sure about something?** Better to ask than guess!

## Troubleshooting

### Pre-commit hook not running?

```bash
# Re-run setup
./setup_precommit.sh

# Check if hook is executable
ls -la .git/hooks/pre-commit
```

### Pycodestyle not found?

```bash
# Install it (optional)
pip install pycodestyle --user

# Or just ignore style warnings
git commit  # Will still work without pycodestyle
```

### PYTHONPATH not set?

```bash
# Temporary (current session)
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"

# Permanent (add to shell config)
echo 'export PYTHONPATH="${PYTHONPATH}:'"$(pwd)/lib"'"' >> ~/.bashrc
source ~/.bashrc
```

## Summary: Your Daily Commands

```bash
# Morning: Get latest code
git checkout develop && git pull

# Start work: Create branch
git checkout -b feature/my-feature

# While working: Check status
git status

# Ready to commit: Stage and commit
git add <files>
git commit -m "feat: description"

# Push your work
git push origin feature/my-feature

# Evening: Create PR and celebrate! 🎉
```

That's it! Keep it simple, stay in your lane, and commit often. 🏒
EOF

# Create simple README for the setup
cat > README_SETUP.md << 'EOF'
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
EOF

echo ""
echo "✅ Simple pre-commit setup complete!"
echo ""
echo "📋 What was created:"
echo "  - .git/hooks/pre-commit (automatic checks)"
echo "  - .pycodestyle (style config)"
echo "  - .gitignore (files to ignore)"
echo "  - requirements-dev.txt (optional tools)"
echo "  - CONTRIBUTING.md (workflow guide)"
echo "  - README_SETUP.md (setup guide)"
echo ""
echo "🎯 What the pre-commit hook does:"
echo "  ✓ Checks Python syntax (blocks commit if error)"
echo "  ✓ Checks PEP 8 style (blocks if pycodestyle installed)"
echo "  ⚠ Warns about print statements"
echo "  ⚠ Warns about untracked TODOs"
echo "  ⚠ Warns about large files"
echo ""
echo "💡 Optional: Install linter for style checking:"
echo "  pip install pycodestyle --user"
echo ""
echo "🚀 Try it out:"
echo "  1. Make some changes to a .py file"
echo "  2. git add <file>"
echo "  3. git commit -m 'test: my changes'"
echo "  4. Watch the pre-commit checks run!"