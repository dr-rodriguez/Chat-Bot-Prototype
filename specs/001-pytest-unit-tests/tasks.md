# Tasks: Pytest Unit Tests for Chat Bot Package

**Feature**: Pytest Unit Tests for Chat Bot Package  
**Branch**: `001-pytest-unit-tests`  
**Date**: 2025-01-27  
**Status**: Ready for Implementation

## Summary

This document outlines the implementation tasks for creating a comprehensive pytest unit test suite for the chat_bot package. The test suite will cover all core components (agent, providers, settings, CLI) with mocked external dependencies, achieving 80% branch coverage and running in under 5 seconds.

**Total Tasks**: 68  
**User Story Breakdown**:
- User Story 1 (P1): 36 tasks
- User Story 2 (P2): 8 tasks  
- User Story 3 (P3): 7 tasks
- Setup & Foundational: 7 tasks
- Polish: 10 tasks

**MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (User Story 1) = 43 tasks

## Dependencies

### User Story Completion Order

1. **Phase 1: Setup** (must complete first)
2. **Phase 2: Foundational** (must complete before user stories)
3. **Phase 3: User Story 1** (P1 - Core Component Unit Tests) - Can start after Phase 2
4. **Phase 4: User Story 2** (P2 - Provider Mocking and Isolation) - Can start after Phase 2, can run in parallel with Phase 3
5. **Phase 5: User Story 3** (P3 - CLI Command Testing) - Requires Phase 3 (agent tests) to be complete
6. **Phase 6: Polish** - Requires all user stories complete

### Parallel Execution Opportunities

**Within User Story 1 (Phase 3)**:
- Test files can be written in parallel: `test_agent.py`, `test_providers_base.py`, `test_providers_ollama.py`, `test_providers_gemini.py`, `test_config.py` (different files, no dependencies)

**Within User Story 2 (Phase 4)**:
- Mocking verification tests can be written in parallel with other Phase 4 tasks

**Within User Story 3 (Phase 5)**:
- CLI test functions can be written in parallel (different test functions, same file)

## Implementation Strategy

**MVP First**: Implement Phase 1, Phase 2, and Phase 3 (User Story 1) to deliver core component testing capability. This provides the foundation for all other testing.

**Incremental Delivery**: Each user story phase is independently testable and can be delivered incrementally:
- Phase 3 delivers core component tests
- Phase 4 delivers mocking verification
- Phase 5 delivers CLI testing

**Test-Driven Development**: Tests are written first (if TDD approach is used), then implementation is verified. For this feature, we're writing tests for existing code, so the workflow is: write test → verify it passes → ensure coverage.

---

## Phase 1: Setup

**Goal**: Initialize test infrastructure and project structure.

**Independent Test**: Can verify setup by checking that `tests/conftest.py` exists and pytest can discover test files.

### Tasks

- [X] T001 Create tests directory structure per implementation plan in tests/
- [X] T002 Create tests/__init__.py to make tests a Python package
- [ ] T003 Verify pytest is installed and accessible via `pytest --version`

---

## Phase 2: Foundational

**Goal**: Create shared test fixtures and infrastructure that all test files will use.

**Independent Test**: Can verify foundational setup by importing fixtures from `tests/conftest.py` and verifying they work.

### Tasks

- [X] T004 [P] Create tests/conftest.py with mock_settings fixture returning Settings instance with test configuration
- [X] T005 [P] Add mock_ollama_llm fixture to tests/conftest.py returning MagicMock configured as Ollama LLM
- [X] T006 [P] Add mock_gemini_llm fixture to tests/conftest.py returning MagicMock configured as Gemini LLM
- [X] T007 [P] Add mock_agent fixture to tests/conftest.py returning MagicMock configured as ChatAgent for CLI tests

---

## Phase 3: User Story 1 - Core Component Unit Tests (P1)

**Goal**: Create unit tests for core chat bot components (agent, providers, settings) that verify functionality works correctly without making live API calls.

**Independent Test**: Can be fully tested by running `pytest tests/test_agent.py tests/test_providers_base.py tests/test_providers_ollama.py tests/test_providers_gemini.py tests/test_config.py` and verifying all tests pass without external calls.

**Acceptance Criteria**:
- All agent initialization, invocation, and tool management tests pass without external calls
- All provider tests pass with mocked LLM responses
- All configuration loading and validation tests pass

### Tasks

#### Agent Module Tests

- [X] T008 [P] [US1] Create tests/test_agent.py with test_agent_initialization_ollama() verifying ChatAgent initializes with Ollama provider
- [X] T009 [P] [US1] Add test_agent_initialization_gemini() to tests/test_agent.py verifying ChatAgent initializes with Gemini provider
- [X] T010 [US1] Add test_agent_initialization_unknown_provider() to tests/test_agent.py verifying ValueError raised for unknown provider
- [X] T011 [US1] Add test_agent_invoke() to tests/test_agent.py verifying agent.invoke() returns response from mocked LLM
- [X] T012 [US1] Add test_agent_add_tool() to tests/test_agent.py verifying tool addition triggers agent reinitialization
- [X] T013 [US1] Add test_agent_get_model_name() to tests/test_agent.py verifying get_model_name() returns correct model name
- [X] T014 [US1] Add test_agent_clear_history() to tests/test_agent.py verifying clear_history() method exists (no-op implementation)

#### Base Provider Tests

- [X] T015 [P] [US1] Create tests/test_providers_base.py with test_base_provider_initialization() verifying BaseProvider cannot be instantiated (abstract)
- [X] T016 [US1] Add test_base_provider_interface() to tests/test_providers_base.py verifying concrete providers implement required methods
- [X] T017 [US1] Add test_base_provider_get_model_name() to tests/test_providers_base.py verifying get_model_name() default implementation
- [X] T018 [US1] Add test_base_provider_validate_config() to tests/test_providers_base.py verifying validate_config() default implementation

#### Ollama Provider Tests

- [X] T019 [P] [US1] Create tests/test_providers_ollama.py with test_ollama_provider_initialization() verifying OllamaProvider initializes with config
- [X] T020 [US1] Add test_ollama_get_available_models() to tests/test_providers_ollama.py verifying _get_available_models() returns model list with mocked urlopen
- [X] T021 [US1] Add test_ollama_get_available_models_network_error() to tests/test_providers_ollama.py verifying graceful handling of network errors
- [X] T022 [US1] Add test_ollama_match_model_exact() to tests/test_providers_ollama.py verifying exact model matching
- [X] T023 [US1] Add test_ollama_match_model_prefix() to tests/test_providers_ollama.py verifying prefix model matching
- [X] T024 [US1] Add test_ollama_match_model_tagged() to tests/test_providers_ollama.py verifying tagged model requires exact match
- [X] T025 [US1] Add test_ollama_match_model_not_found() to tests/test_providers_ollama.py verifying ValueError raised when model not found
- [X] T026 [US1] Add test_ollama_get_llm() to tests/test_providers_ollama.py verifying get_llm() returns OllamaLLM instance (mocked)
- [X] T027 [US1] Add test_ollama_invoke() to tests/test_providers_ollama.py verifying invoke() returns LLM response
- [X] T028 [US1] Add test_ollama_get_model_name() to tests/test_providers_ollama.py verifying get_model_name() returns matched model
- [X] T029 [US1] Add test_ollama_validate_config() to tests/test_providers_ollama.py verifying validate_config() checks required fields

#### Gemini Provider Tests

- [X] T030 [P] [US1] Create tests/test_providers_gemini.py with test_gemini_provider_initialization() verifying GeminiProvider initializes with config
- [X] T031 [US1] Add test_gemini_get_llm() to tests/test_providers_gemini.py verifying get_llm() returns ChatGoogleGenerativeAI instance (mocked)
- [X] T032 [US1] Add test_gemini_get_llm_missing_api_key() to tests/test_providers_gemini.py verifying ValueError raised when API key missing
- [X] T033 [US1] Add test_gemini_invoke() to tests/test_providers_gemini.py verifying invoke() returns LLM response content
- [X] T034 [US1] Add test_gemini_invoke_message_object() to tests/test_providers_gemini.py verifying invoke() handles message objects correctly
- [X] T035 [US1] Add test_gemini_get_model_name() to tests/test_providers_gemini.py verifying get_model_name() returns model name
- [X] T036 [US1] Add test_gemini_validate_config() to tests/test_providers_gemini.py verifying validate_config() checks required fields

#### Settings/Config Tests

- [X] T037 [P] [US1] Create tests/test_config.py with test_settings_initialization_defaults() verifying Settings loads with default values
- [X] T038 [US1] Add test_settings_initialization_env_vars() to tests/test_config.py verifying Settings loads from environment variables with mocked os.getenv
- [X] T039 [US1] Add test_settings_get_provider_config_ollama() to tests/test_config.py verifying Ollama config retrieval
- [X] T040 [US1] Add test_settings_get_provider_config_gemini() to tests/test_config.py verifying Gemini config retrieval
- [X] T041 [US1] Add test_settings_get_provider_config_gemini_missing_key() to tests/test_config.py verifying ValueError when API key missing
- [X] T042 [US1] Add test_settings_get_provider_config_unknown() to tests/test_config.py verifying ValueError for unknown provider
- [X] T043 [US1] Add test_settings_validate() to tests/test_config.py verifying validate() returns True

---

## Phase 4: User Story 2 - Provider Mocking and Isolation (P2)

**Goal**: Verify that all provider tests use mocks and never make actual HTTP requests or API calls.

**Independent Test**: Can be fully tested by verifying that all provider tests use mocks and never make actual HTTP requests or API calls, running tests without network connectivity and without API keys configured.

**Acceptance Criteria**:
- All provider tests use mocks and never make actual HTTP requests to Ollama or Gemini APIs
- All tests pass without API keys configured
- All tests pass offline

### Tasks

- [X] T044 [P] [US2] Add network monitoring verification to tests/test_providers_ollama.py ensuring no actual HTTP requests are made
- [X] T045 [US2] Add test verification to tests/test_providers_ollama.py ensuring tests pass without Ollama service running
- [X] T046 [P] [US2] Add network monitoring verification to tests/test_providers_gemini.py ensuring no actual API calls are made
- [X] T047 [US2] Add test verification to tests/test_providers_gemini.py ensuring tests pass without GEMINI_API_KEY environment variable
- [X] T048 [US2] Add test verification to tests/test_providers_gemini.py ensuring tests pass with mocked ChatGoogleGenerativeAI initialization
- [X] T049 [US2] Verify all provider tests use @patch decorators or with patch() context managers for external dependencies
- [X] T050 [US2] Add documentation comment to tests/test_providers_ollama.py explaining mocking strategy for urllib.request.urlopen
- [X] T051 [US2] Add documentation comment to tests/test_providers_gemini.py explaining mocking strategy for ChatGoogleGenerativeAI

---

## Phase 5: User Story 3 - CLI Command Testing (P3)

**Goal**: Create unit tests for CLI commands that verify command-line interface behavior works correctly.

**Independent Test**: Can be fully tested by running `pytest tests/test_cli.py` and verifying all command parsing and execution tests pass with mocked agent calls.

**Acceptance Criteria**:
- All command parsing and execution tests pass with mocked agent calls
- Appropriate error messages are displayed for invalid inputs

### Tasks

- [X] T052 [P] [US3] Create tests/test_cli.py with test_cli_chat_command() verifying chat command initializes agent and starts interactive loop (mocked)
- [X] T053 [US3] Add test_cli_chat_command_exit() to tests/test_cli.py verifying chat command handles exit/quit commands
- [X] T054 [US3] Add test_cli_chat_command_error() to tests/test_cli.py verifying chat command handles errors gracefully
- [X] T055 [US3] Add test_cli_run_command() to tests/test_cli.py verifying run command processes message and outputs response
- [X] T056 [US3] Add test_cli_run_command_error() to tests/test_cli.py verifying run command handles errors and exits with code 1
- [X] T057 [US3] Add test_cli_provider_option() to tests/test_cli.py verifying provider option is passed to agent
- [X] T058 [US3] Add test_cli_model_option() to tests/test_cli.py verifying model option is passed to agent

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Ensure test suite meets all success criteria, achieves coverage targets, and follows best practices.

**Independent Test**: Can verify polish by running full test suite with coverage reporting and verifying all success criteria are met.

### Tasks

- [ ] T059 Verify test suite execution time is under 5 seconds by running `pytest tests/` and measuring execution time (requires pytest installation)
- [ ] T060 Install pytest-cov if needed and run `pytest --cov=chat_bot --cov-branch tests/` to verify 80% branch coverage achieved (requires pytest installation)
- [X] T061 Review all test files to ensure shared fixtures from conftest.py are used, reducing code duplication by at least 50%
- [X] T062 Verify all test functions follow pytest naming conventions (test_*.py files, test_* functions)
- [X] T063 Add docstrings to all test functions explaining what they test
- [ ] T064 Verify all tests can run without network connectivity by disabling network and running `pytest tests/` (requires pytest installation)
- [ ] T065 Verify all tests can run without API keys by unsetting environment variables and running `pytest tests/` (requires pytest installation)
- [X] T066 Review test organization to ensure tests mirror package structure (test_agent.py, test_providers_*.py, test_config.py, test_cli.py)
- [X] T067 Add edge case tests for empty inputs, model matching failures, and configuration edge conditions if not already covered
- [X] T068 Verify all error handling scenarios are tested including invalid configurations, missing API keys, and network errors

---

## Task Summary

**Total Tasks**: 68

**By Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 4 tasks
- Phase 3 (User Story 1): 36 tasks
- Phase 4 (User Story 2): 8 tasks
- Phase 5 (User Story 3): 7 tasks
- Phase 6 (Polish): 10 tasks

**By User Story**:
- User Story 1: 36 tasks (core component tests)
- User Story 2: 8 tasks (mocking verification)
- User Story 3: 7 tasks (CLI tests)

**Parallel Opportunities**: 
- Phase 3: Multiple test files can be written in parallel (T008, T015, T019, T030, T037 for file creation; then subsequent tests in each file)
- Phase 4: Mocking verification tasks can be done in parallel (T044, T046)
- Phase 5: CLI test functions can be written in parallel (T052-T058)

**MVP Scope**: Phases 1-3 (43 tasks) deliver core component testing capability.

