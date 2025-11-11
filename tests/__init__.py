"""
Tests Module - Unit and Integration Tests
=========================================

Test suite organized to mirror the src/ structure.

Structure:
---------
test_ui/
    Tests for UI components, screens, and widgets.
    Uses mock controllers to test UI in isolation.

test_controllers/
    Tests for controller logic and data orchestration.
    Uses mock database responses to test independently.

test_database/
    Tests for query engine, validators, and predefined queries.
    Uses test database with known data.

test_shared/
    Tests for shared utilities, interfaces, and helpers.

Guidelines:
----------
- One test file per source file
- Use descriptive test names: test_<function>_<scenario>_<expected>
- Include docstrings explaining what is being tested
- Use fixtures for common setup
- Mock external dependencies
- Aim for >80% code coverage
- Run tests before committing

Running Tests:
-------------
pytest tests/                    # Run all tests
pytest tests/test_ui/           # Run UI tests only
pytest tests/ -v                # Verbose output
pytest tests/ --cov=src         # With coverage report

Owner: All members test their own code
"""
