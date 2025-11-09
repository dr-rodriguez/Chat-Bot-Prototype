# Research: Pytest Unit Tests Implementation

**Feature**: Pytest Unit Tests for Chat Bot Package  
**Date**: 2025-01-27  
**Status**: Complete

## Research Tasks

### 1. Pytest Framework and Best Practices

**Decision**: Use pytest with unittest.mock (stdlib) for mocking. Use pytest fixtures for shared test setup.

**Rationale**: 
- pytest is already in dev dependencies (pytest>=9.0.0)
- unittest.mock is part of Python standard library, no additional dependencies needed
- pytest fixtures provide clean, reusable test setup that reduces duplication
- pytest's plugin ecosystem (pytest-mock) is available if needed but not required

**Alternatives Considered**:
- pytest-mock plugin: Provides mocker fixture, but unittest.mock is sufficient for this use case
- unittest framework: Less modern, more verbose, pytest is already in dependencies
- mock library (PyPI): Deprecated in favor of unittest.mock

**Best Practices Applied**:
- Test files follow `test_*.py` naming convention
- Test functions follow `test_*` naming convention
- Shared fixtures defined in `conftest.py` at tests root
- Use pytest fixtures for dependency injection
- Use unittest.mock.patch for mocking external dependencies

### 2. Mocking Strategy for Langchain LLM Instances

**Decision**: Mock Langchain LLM instances at the provider level using unittest.mock.MagicMock or unittest.mock.patch.

**Rationale**:
- Langchain LLM instances (OllamaLLM, ChatGoogleGenerativeAI) are complex objects with many methods
- Mocking at the provider.get_llm() level prevents actual LLM initialization
- Mock LLM instances can return predictable responses for testing
- Avoids network calls and API key requirements

**Alternatives Considered**:
- Mock at langchain library level: Too low-level, breaks encapsulation
- Use actual LLM instances with test models: Requires network, API keys, slow, non-deterministic
- Mock at agent.invoke() level: Too high-level, doesn't test provider logic

**Implementation Approach**:
- Mock `provider.get_llm()` to return a MagicMock with `invoke()` method
- Mock `agent.agent.invoke()` for agent-level tests
- Use `@patch` decorator or `with patch()` context manager

### 3. Mocking Strategy for Ollama HTTP Requests

**Decision**: Mock urllib.request.urlopen using unittest.mock.patch to prevent actual HTTP requests to Ollama API.

**Rationale**:
- OllamaProvider uses urllib.request.urlopen to fetch available models
- Mocking urlopen prevents network calls during tests
- Can return predictable JSON responses for model listing
- Tests can simulate both success and failure scenarios

**Alternatives Considered**:
- Use actual Ollama instance: Requires Ollama running, network dependency
- Use responses library: Additional dependency, unittest.mock is sufficient
- Mock at higher level (OllamaProvider._get_available_models): Less isolation

**Implementation Approach**:
- Patch `urllib.request.urlopen` in OllamaProvider tests
- Return mock HTTPResponse with JSON data for successful cases
- Raise URLError/HTTPError for failure cases

### 4. Mocking Strategy for Gemini API Calls

**Decision**: Mock ChatGoogleGenerativeAI class initialization and invoke method using unittest.mock.patch.

**Rationale**:
- GeminiProvider uses ChatGoogleGenerativeAI from langchain_google_genai
- Mocking class prevents actual API initialization
- Mock instances can return predictable responses
- Avoids API key requirements and network calls

**Alternatives Considered**:
- Use actual Gemini API with test key: Requires API key, network, costs, non-deterministic
- Mock at Settings level: Too high-level, doesn't test provider logic
- Use test double classes: More complex than needed

**Implementation Approach**:
- Patch `langchain_google_genai.ChatGoogleGenerativeAI` in GeminiProvider tests
- Return mock instance with invoke() method that returns mock message objects
- Test both successful initialization and missing API key scenarios

### 5. Test Fixture Design for Code Reuse

**Decision**: Create shared fixtures in conftest.py for common test objects (Settings, mock LLMs, mock agents).

**Rationale**:
- Reduces code duplication by 50% as required by spec
- Provides consistent test setup across all test files
- Makes tests more maintainable and readable
- Follows pytest best practices

**Alternatives Considered**:
- Duplicate setup in each test: Violates DRY principle, increases maintenance
- Use test base classes: Less idiomatic in pytest, fixtures are preferred
- Use pytest plugins: Overkill for this use case

**Fixtures to Create**:
- `mock_settings`: Settings instance with test configuration
- `mock_ollama_llm`: Mock Ollama LLM instance
- `mock_gemini_llm`: Mock Gemini LLM instance
- `mock_agent`: Mock ChatAgent instance for CLI tests

### 6. Test Coverage Strategy

**Decision**: Aim for 80% branch coverage using pytest-cov (if available) or manual verification.

**Rationale**:
- Spec requires 80% branch coverage (both true/false paths in conditionals)
- Branch coverage ensures both success and error paths are tested
- Coverage tools help identify untested code paths

**Alternatives Considered**:
- Line coverage only: Doesn't ensure conditional branches are tested
- 100% coverage: Overkill, may require testing implementation details
- No coverage measurement: Doesn't meet spec requirements

**Coverage Areas**:
- All conditional branches (if/else, try/except)
- Both provider types (Ollama, Gemini)
- Success and error paths
- Edge cases (empty inputs, missing config, model matching failures)

### 7. Test Organization and Structure

**Decision**: Organize tests by module with one test file per source module, mirroring package structure.

**Rationale**:
- Clear mapping between source code and tests
- Easy to find tests for specific components
- Follows pytest conventions and Python best practices
- Maintainable as codebase grows

**Alternatives Considered**:
- Single test file: Too large, hard to navigate
- Organize by test type (unit/integration): Only unit tests in scope
- Organize by feature: Doesn't match code structure

**Test File Structure**:
- `test_agent.py`: ChatAgent class tests
- `test_providers_base.py`: BaseProvider abstract class tests
- `test_providers_ollama.py`: OllamaProvider tests
- `test_providers_gemini.py`: GeminiProvider tests
- `test_config.py`: Settings class tests
- `test_cli.py`: CLI command tests

## Summary

All research tasks completed. No clarifications needed. The implementation will use:
- pytest with unittest.mock for mocking
- Shared fixtures in conftest.py for code reuse
- Module-level test organization
- Comprehensive mocking of all external dependencies
- Branch coverage focus for thorough testing

