# Quickstart: Running Pytest Unit Tests

**Feature**: Pytest Unit Tests for Chat Bot Package  
**Date**: 2025-01-27

## Prerequisites

- Python 3.13+
- uv package manager (or pip)
- Project dependencies installed

## Installation

```bash
# Install dependencies (if not already installed)
uv sync

# Or with pip
pip install -e ".[dev]"
```

## Running Tests

### Run All Tests

```bash
# From repository root
pytest

# Or explicitly specify tests directory
pytest tests/
```

### Run Specific Test File

```bash
# Test agent module
pytest tests/test_agent.py

# Test providers
pytest tests/test_providers_ollama.py
pytest tests/test_providers_gemini.py

# Test config
pytest tests/test_config.py

# Test CLI
pytest tests/test_cli.py
```

### Run Specific Test Function

```bash
# Run single test
pytest tests/test_agent.py::test_agent_initialization_ollama

# Run tests matching pattern
pytest -k "ollama"
pytest -k "initialization"
```

### Run with Verbose Output

```bash
# Verbose output showing each test
pytest -v

# Very verbose with print statements
pytest -vv -s
```

## Test Coverage

### Check Coverage

```bash
# Install coverage tool (if not already installed)
uv add --dev pytest-cov

# Run tests with coverage
pytest --cov=chat_bot --cov-branch

# Generate HTML report
pytest --cov=chat_bot --cov-branch --cov-report=html

# View report
# Open htmlcov/index.html in browser
```

### Coverage Requirements

- **Target**: >= 80% branch coverage
- **Focus**: Both true/false paths in conditionals must be tested
- **Measurement**: Use `--cov-branch` flag for branch coverage

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_agent.py            # ChatAgent tests
├── test_providers_base.py   # BaseProvider tests
├── test_providers_ollama.py # OllamaProvider tests
├── test_providers_gemini.py # GeminiProvider tests
├── test_config.py           # Settings tests
└── test_cli.py              # CLI tests
```

## Key Features

### No External Dependencies

- ✅ All tests run without network connectivity
- ✅ No API keys required
- ✅ No external services needed (Ollama, Gemini)
- ✅ All external calls are mocked

### Fast Execution

- ✅ Test suite runs in < 5 seconds
- ✅ Individual tests run in < 1 second
- ✅ No network delays
- ✅ No LLM processing delays

### Shared Fixtures

- ✅ Common test setup in `conftest.py`
- ✅ Reduces code duplication by 50%
- ✅ Consistent test data across tests

## Example Test Output

```
============================= test session starts ==============================
platform win32 -- Python 3.13.0, pytest-9.0.0, pluggy-1.5.0
rootdir: C:\Users\strak\Projects\Chat-Bot-Prototype
collected 20 items

tests/test_agent.py ..........                                          [ 50%]
tests/test_providers_ollama.py .....                                    [ 75%]
tests/test_providers_gemini.py .....                                    [100%]

============================= 20 passed in 2.34s ==============================
```

## Troubleshooting

### Tests Fail with Import Errors

```bash
# Ensure package is installed in development mode
uv sync
# or
pip install -e .
```

### Tests Make Network Calls

- Check that mocks are properly applied
- Verify `@patch` decorators are used correctly
- Ensure `conftest.py` fixtures are loaded

### Coverage Below 80%

- Run coverage report to identify untested branches
- Add tests for missing conditional paths
- Focus on error handling and edge cases

### Tests Run Slowly

- Verify all external calls are mocked
- Check for actual LLM invocations
- Ensure no network requests are made

## Next Steps

1. **Review Test Contracts**: See `contracts/test-contracts.md` for detailed test specifications
2. **Check Data Model**: See `data-model.md` for test entities and structures
3. **Read Research**: See `research.md` for implementation decisions
4. **Run Tests**: Execute `pytest` to verify all tests pass

## Development Workflow

1. Write test for new functionality
2. Run test to verify it fails (TDD)
3. Implement functionality
4. Run test to verify it passes
5. Check coverage to ensure branches tested
6. Refactor if needed

## Continuous Integration

Tests are designed to run in CI/CD pipelines:
- No external dependencies
- Fast execution
- Deterministic results
- No environment setup required

