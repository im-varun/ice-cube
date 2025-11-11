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

# run linters
ruff check . --fix
ruff format .

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

# Stage changes
git add <files>


# Run linters
ruff check <files> --fix
ruff format <files>

# Commit changes
git commit -m "feat: description"

# Push your work
git push origin feature/my-feature

# Evening: Create PR and celebrate!
```

That's it! Keep it simple, stay in your lane, and commit often. 🏒
