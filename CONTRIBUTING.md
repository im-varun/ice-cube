## 📋 CONTRIBUTING.md

# Contributing to IceCube

## Getting Started

1. Clone the repository

   ```
   git clone <repo-url>
   cd IceCube
   ```
2. Set up Python path for lib/ directory

   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"
   ```
3. Install pre-commit hooks

   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Branch Strategy

* main - Production-ready code
* develop - Integration branch
* feature/`<name>` - Feature branches
* bugfix/`<name>` - Bug fix branches

## Workflow

1. Create a feature branch

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```
2. Make changes in your designated directory

   * UI Developer: src/ui/
   * Controller Developer: src/controllers/
   * Database Developer: src/database/
3. Run linters before committing

   ```bash
   flake8 src/
   black src/ --check
   mypy src/
   ```
4. Commit your changes

   ```bash
   git add .
   git commit -m "feat: add player stats widget"
   ```

   Pre-commit hooks will run automatically!
5. Push and create PR

   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Message Convention

Use conventional commits:

* feat: - New feature
* fix: - Bug fix
* docs: - Documentation changes
* style: - Code style changes (formatting)
* refactor: - Code refactoring
* test: - Adding tests
* chore: - Maintenance tasks

## Code Standards

### Python Style

* Line length: 100 characters
* Formatting: Black formatter
* Imports: isort with black profile
* Type hints: Use type hints for all function signatures
* Docstrings: Google-style docstrings

### Example

```python
from typing import List, Dict, Any

def get_player_stats(player_id: int, season: str) -> Dict[str, Any]:
    """
    Retrieve player statistics for a given season.

    Args:
        player_id: Unique identifier for the player
        season: Season year (e.g., "2019-2020")

    Returns:
        Dictionary containing player statistics

    Raises:
        ValueError: If player_id is invalid
        DatabaseError: If query fails
    """
    pass
```

## Testing

Write tests for all new features:

```bash
# Run all tests
python -m pytest tests/

# Run tests for specific module
python -m pytest tests/test_ui/

# Run with coverage
python -m pytest --cov=src tests/
```

## Communication

* Interfaces changed? Notify all team members immediately
* Breaking changes? Create an issue first, discuss with team
* Stuck? Ask in team chat, don't struggle alone

## Avoiding Merge Conflicts

1. Pull frequently
   ```bash
   git pull origin develop
   ```
2. Stay in your directory
   * UI dev: Only modify src/ui/
   * Controller dev: Only modify src/controllers/
   * Database dev: Only modify src/database/
3. Shared files (src/shared/):
   * Create an issue before modifying
   * Get team approval
   * Notify everyone after changes
4. Rebase before PR
   ```bash
   git fetch origin
   git rebase origin/develop
   ```

## Code Review Checklist

* [ ] Code follows style guidelines (passes flake8/black)
* [ ] All functions have type hints
* [ ] Docstrings added for public functions
* [ ] Tests added/updated
* [ ] No hardcoded values (use config.py)
* [ ] Error handling implemented
* [ ] Logging added for important operations
* [ ] No print statements (use logger)
* [ ] Interfaces respected (no direct imports across layers)

## Questions?

Check the wiki or ask in the telegram channel


## 🚀 Setup Script

**File:** `setup.sh`

```
#!/bin/bash

echo "🏒 Setting up IceCube development environment..."

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/lib"
echo "export PYTHONPATH=\"\${PYTHONPATH}:$(pwd)/lib\"" >> ~/.bashrc

# Install pre-commit
echo "Installing pre-commit hooks..."
pip install pre-commit --user
pre-commit install

# Create necessary directories
mkdir -p data/raw data/cleaned logs tests

# Create .gitkeep files
touch data/raw/.gitkeep data/cleaned/.gitkeep logs/.gitkeep

echo "Setup complete! Run 'source ~/.bashrc' to activate PYTHONPATH"
```

---

## 📦 Example Implementation

### Shared Interfaces

File: src/shared/interfaces.py

```python
"""
Central interface definitions for IceCube.
ALL members should reference these interfaces.
"""

from typing import Protocol, Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    """Available UI actions"""
    LOGIN = "login"
    LOGOUT = "logout"
    GET_PLAYER_STATS = "get_player_stats"
    RUN_ANALYTICS = "run_analytics"
    CUSTOM_QUERY = "custom_query"


@dataclass
class UIRequest:
    """Request from UI to Controller"""
    action: ActionType
    params: Dict[str, Any]
    user_id: Optional[int] = None
  
    def validate(self) -> bool:
        """Validate request has required fields"""
        return self.action is not None


@dataclass
class UIResponse:
    """Response from Controller to UI"""
    success: bool
    data: Any
    message: str
    error_code: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ControllerInterface(Protocol):
    """Contract for all controllers"""
  
    def handle_request(self, request: UIRequest) -> UIResponse:
        """Handle a UI request and return formatted response"""
        ...
```
