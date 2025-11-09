# Test Contracts: Pytest Unit Tests

**Feature**: Pytest Unit Tests for Chat Bot Package  
**Date**: 2025-01-27

## Test Interface Contracts

### ChatAgent Test Contract

**Module**: `tests/test_agent.py`

**Test Functions**:
- `test_agent_initialization_ollama()` - Verifies ChatAgent initializes with Ollama provider
- `test_agent_initialization_gemini()` - Verifies ChatAgent initializes with Gemini provider
- `test_agent_initialization_unknown_provider()` - Verifies ValueError raised for unknown provider
- `test_agent_invoke()` - Verifies agent.invoke() returns response from mocked LLM
- `test_agent_add_tool()` - Verifies tool addition triggers agent reinitialization
- `test_agent_get_model_name()` - Verifies get_model_name() returns correct model name
- `test_agent_clear_history()` - Verifies clear_history() method exists (no-op implementation)

**Mocking Requirements**:
- Mock `provider.get_llm()` to return mock LLM
- Mock `agent.agent.invoke()` to return mock response
- Mock provider initialization

**Expected Behaviors**:
- Initialization succeeds with valid provider
- Initialization fails with unknown provider (ValueError)
- Invoke returns string response
- Tool addition reinitializes agent
- Model name retrieval works correctly

---

### BaseProvider Test Contract

**Module**: `tests/test_providers_base.py`

**Test Functions**:
- `test_base_provider_initialization()` - Verifies BaseProvider cannot be instantiated (abstract)
- `test_base_provider_interface()` - Verifies concrete providers implement required methods
- `test_base_provider_get_model_name()` - Verifies get_model_name() default implementation
- `test_base_provider_validate_config()` - Verifies validate_config() default implementation

**Mocking Requirements**:
- Use ABCMeta to verify abstract class behavior
- Test with concrete provider instances (OllamaProvider, GeminiProvider)

**Expected Behaviors**:
- BaseProvider is abstract and cannot be instantiated
- Concrete providers implement get_llm() and invoke()
- Default methods work correctly

---

### OllamaProvider Test Contract

**Module**: `tests/test_providers_ollama.py`

**Test Functions**:
- `test_ollama_provider_initialization()` - Verifies OllamaProvider initializes with config
- `test_ollama_get_available_models()` - Verifies _get_available_models() returns model list
- `test_ollama_get_available_models_network_error()` - Verifies graceful handling of network errors
- `test_ollama_match_model_exact()` - Verifies exact model matching
- `test_ollama_match_model_prefix()` - Verifies prefix model matching
- `test_ollama_match_model_tagged()` - Verifies tagged model requires exact match
- `test_ollama_match_model_not_found()` - Verifies ValueError raised when model not found
- `test_ollama_get_llm()` - Verifies get_llm() returns OllamaLLM instance (mocked)
- `test_ollama_invoke()` - Verifies invoke() returns LLM response
- `test_ollama_get_model_name()` - Verifies get_model_name() returns matched model
- `test_ollama_validate_config()` - Verifies validate_config() checks required fields

**Mocking Requirements**:
- Mock `urllib.request.urlopen` for HTTP requests
- Mock `langchain_ollama.OllamaLLM` for LLM creation
- Mock LLM.invoke() for response generation

**Expected Behaviors**:
- Initialization succeeds with valid config
- Model matching works for exact, prefix, and tagged models
- Network errors handled gracefully (returns empty list)
- LLM creation uses matched model name
- Validation fails if model or base_url missing

---

### GeminiProvider Test Contract

**Module**: `tests/test_providers_gemini.py`

**Test Functions**:
- `test_gemini_provider_initialization()` - Verifies GeminiProvider initializes with config
- `test_gemini_get_llm()` - Verifies get_llm() returns ChatGoogleGenerativeAI instance (mocked)
- `test_gemini_get_llm_missing_api_key()` - Verifies ValueError raised when API key missing
- `test_gemini_invoke()` - Verifies invoke() returns LLM response content
- `test_gemini_invoke_message_object()` - Verifies invoke() handles message objects correctly
- `test_gemini_get_model_name()` - Verifies get_model_name() returns model name
- `test_gemini_validate_config()` - Verifies validate_config() checks required fields

**Mocking Requirements**:
- Mock `langchain_google_genai.ChatGoogleGenerativeAI` for LLM creation
- Mock LLM.invoke() to return mock message objects
- Mock message.content attribute

**Expected Behaviors**:
- Initialization succeeds with valid config and API key
- LLM creation fails if API key missing (ValueError)
- Invoke extracts content from message objects
- Validation fails if API key or model missing

---

### Settings Test Contract

**Module**: `tests/test_config.py`

**Test Functions**:
- `test_settings_initialization_defaults()` - Verifies Settings loads with default values
- `test_settings_initialization_env_vars()` - Verifies Settings loads from environment variables
- `test_settings_get_provider_config_ollama()` - Verifies Ollama config retrieval
- `test_settings_get_provider_config_gemini()` - Verifies Gemini config retrieval
- `test_settings_get_provider_config_gemini_missing_key()` - Verifies ValueError when API key missing
- `test_settings_get_provider_config_unknown()` - Verifies ValueError for unknown provider
- `test_settings_validate()` - Verifies validate() returns True

**Mocking Requirements**:
- Mock `os.getenv` for environment variable access
- Mock `dotenv.load_dotenv` if needed

**Expected Behaviors**:
- Default values used when env vars not set
- Environment variables override defaults
- Provider config returns correct dict structure
- Missing API key raises ValueError for Gemini
- Unknown provider raises ValueError

---

### CLI Test Contract

**Module**: `tests/test_cli.py`

**Test Functions**:
- `test_cli_chat_command()` - Verifies chat command initializes agent and starts interactive loop (mocked)
- `test_cli_chat_command_exit()` - Verifies chat command handles exit/quit commands
- `test_cli_chat_command_error()` - Verifies chat command handles errors gracefully
- `test_cli_run_command()` - Verifies run command processes message and outputs response
- `test_cli_run_command_error()` - Verifies run command handles errors and exits with code 1
- `test_cli_provider_option()` - Verifies provider option is passed to agent
- `test_cli_model_option()` - Verifies model option is passed to agent

**Mocking Requirements**:
- Mock `ChatAgent` class and instances
- Mock `click.prompt` for interactive input
- Mock `click.echo` for output verification
- Mock `sys.exit` for error exit testing

**Expected Behaviors**:
- Chat command initializes agent with correct provider/model
- Chat command handles user input and displays responses
- Run command processes single message and outputs response
- Errors are displayed and handled appropriately
- Options are passed correctly to agent

---

## Fixture Contracts

### conftest.py Fixtures

**mock_settings**:
- Returns: Settings instance with test configuration
- Scope: function (default)
- Usage: Injected into test functions requiring Settings

**mock_ollama_llm**:
- Returns: MagicMock configured as Ollama LLM
- Scope: function
- Usage: Mock LLM for OllamaProvider tests

**mock_gemini_llm**:
- Returns: MagicMock configured as Gemini LLM
- Scope: function
- Usage: Mock LLM for GeminiProvider tests

**mock_agent**:
- Returns: MagicMock configured as ChatAgent
- Scope: function
- Usage: Mock agent for CLI tests

---

## Test Execution Contract

**Command**: `pytest tests/` or `pytest` (from repo root)

**Expected Output**:
- All tests pass
- Execution time < 5 seconds
- No network requests made
- No API keys required
- Coverage report shows >= 80% branch coverage

**Prerequisites**:
- pytest installed (dev dependency)
- Python 3.13+
- No external services running
- No environment variables set (or mocked)

---

## Error Handling Contracts

### Network Errors
- Ollama HTTP requests: Return empty list, don't raise exceptions
- Tests verify graceful degradation when Ollama unavailable

### Configuration Errors
- Missing API key (Gemini): Raise ValueError with clear message
- Missing model: Raise ValueError with clear message
- Unknown provider: Raise ValueError with provider name

### Invocation Errors
- LLM invocation errors: Propagate to caller
- Agent invocation errors: Display error message, continue or exit appropriately

---

## Coverage Requirements

**Branch Coverage**: >= 80%

**Critical Branches to Test**:
- Provider selection (ollama vs gemini vs unknown)
- Model matching logic (exact, prefix, tagged, not found)
- API key validation (present vs missing)
- Configuration validation (valid vs invalid)
- Error handling paths (success vs exception)
- Tool addition (with tools vs without tools)
- Model name retrieval (matched vs requested vs unknown)

