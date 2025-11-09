# Implementation Plan: Pytest Unit Tests for Chat Bot Package

**Branch**: `001-pytest-unit-tests` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-pytest-unit-tests/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a comprehensive pytest unit test suite for the chat_bot package covering all core components (agent, providers, settings, CLI) with mocked external dependencies. The test suite must achieve 80% branch coverage, run in under 5 seconds, and use shared fixtures to reduce code duplication. All external API calls (Ollama HTTP requests, Gemini API calls, Langchain LLM invocations) must be mocked to ensure tests run without network connectivity or API keys.

## Technical Context

**Language/Version**: Python 3.13+ (requires-python = ">=3.13" in pyproject.toml)  
**Primary Dependencies**: pytest>=9.0.0 (dev), unittest.mock (stdlib), pytest-mock (optional), langchain>=1.0.5, langchain-ollama>=1.0.0, langchain-google-genai>=3.0.1, click>=8.3.0, python-dotenv>=1.2.1  
**Storage**: N/A (unit tests focus on in-memory components)  
**Testing**: pytest framework with unittest.mock for mocking, pytest fixtures for shared setup  
**Target Platform**: Cross-platform (Windows, Linux, macOS) - Python-based  
**Project Type**: Single Python package (chat_bot) with CLI interface  
**Performance Goals**: Test suite execution <5 seconds total, individual tests <1 second each  
**Constraints**: Tests must run without network connectivity, API keys, or external services. Must achieve 80% branch coverage. Must use shared fixtures to reduce duplication by 50%.  
**Scale/Scope**: ~500 lines of test code covering 4 modules (agent, providers, config, cli) with ~15-35 test functions total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Simplicity First**: ✅ PASS - Unit tests use standard pytest and unittest.mock (stdlib). No complex test frameworks or patterns. Simple fixture-based setup reduces duplication without over-engineering.

**II. Langchain Agent Architecture**: ✅ PASS - Tests verify agent correctly uses Langchain's agent framework. Provider-specific tests are isolated in separate test files (test_ollama.py, test_gemini.py). Tests mock Langchain LLM instances to avoid actual invocations.

**III. Multi-Provider Support**: ✅ PASS - Test suite covers both Ollama and Gemini providers. Tests verify provider selection and configuration work correctly for both providers.

**IV. CLI Interface**: ✅ PASS - Tests cover both CLI commands (chat, run) and verify they work in both interactive and non-interactive modes. Tests mock agent interactions to avoid actual LLM calls.

**V. MCP Tool Integration**: ✅ N/A - Unit tests focus on core components. MCP tool integration testing is out of scope for this feature (per spec: "No integration tests are required").

**Violations**: None - All principles satisfied. Unit testing is a standard development practice that aligns with all constitution principles.

**Post-Design Re-evaluation (Phase 1 Complete)**: ✅ All principles still satisfied. Design artifacts (research.md, data-model.md, contracts/, quickstart.md) confirm simple, straightforward approach using standard pytest patterns. No complexity introduced beyond what's necessary for comprehensive unit testing.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
chat_bot/
├── __init__.py
├── agent/
│   ├── __init__.py
│   └── agent.py
├── cli/
│   ├── __init__.py
│   └── main.py
├── config/
│   ├── __init__.py
│   └── settings.py
└── providers/
    ├── __init__.py
    ├── base.py
    ├── ollama.py
    └── gemini.py

tests/
├── __init__.py
├── conftest.py              # Shared pytest fixtures
├── test_agent.py            # ChatAgent unit tests
├── test_providers_base.py   # BaseProvider interface tests
├── test_providers_ollama.py # OllamaProvider unit tests
├── test_providers_gemini.py # GeminiProvider unit tests
├── test_config.py           # Settings unit tests
└── test_cli.py              # CLI command unit tests
```

**Structure Decision**: Single Python package structure. Tests mirror the package structure in a separate `tests/` directory following pytest conventions. Shared fixtures are defined in `conftest.py` at the tests root level.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
