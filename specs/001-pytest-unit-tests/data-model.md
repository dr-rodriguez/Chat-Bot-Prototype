# Data Model: Pytest Unit Tests

**Feature**: Pytest Unit Tests for Chat Bot Package  
**Date**: 2025-01-27

## Test Entities

### MockSettings
**Purpose**: Test fixture providing Settings instance with controlled configuration

**Fields**:
- `ollama_base_url`: str - Test Ollama base URL (default: "http://localhost:11434")
- `ollama_model`: str - Test Ollama model name (default: "llama3.2")
- `gemini_api_key`: str | None - Test Gemini API key (default: "test-api-key" or None for error tests)
- `gemini_model`: str - Test Gemini model name (default: "gemini-2.5-flash")

**Validation Rules**:
- Can be instantiated with or without environment variables
- Can simulate missing API keys for error testing
- Can override any configuration value for specific test scenarios

**Usage**: Provided via `mock_settings` fixture in conftest.py

---

### MockLLM
**Purpose**: Mock Langchain LLM instance for testing

**Fields**:
- `invoke()`: method - Returns mock response string
- `model`: str - Mock model name
- `base_url`: str | None - Mock base URL (for Ollama)

**Validation Rules**:
- Must implement `invoke(prompt: str) -> str` interface
- Can be configured to return specific responses
- Can be configured to raise exceptions for error testing

**Usage**: Provided via `mock_ollama_llm` and `mock_gemini_llm` fixtures

---

### MockAgent
**Purpose**: Mock ChatAgent instance for CLI testing

**Fields**:
- `invoke(message: str) -> str`: method - Returns mock response
- `get_model_name() -> str`: method - Returns mock model name
- `provider_name`: str - Mock provider name
- `model`: str - Mock model name

**Validation Rules**:
- Must implement ChatAgent interface methods
- Can be configured to return specific responses
- Can be configured to raise exceptions for error testing

**Usage**: Provided via `mock_agent` fixture for CLI tests

---

### MockHTTPResponse
**Purpose**: Mock HTTP response for Ollama API calls

**Fields**:
- `read() -> bytes`: method - Returns mock JSON response bytes
- `status`: int - HTTP status code (default: 200)

**Validation Rules**:
- Must return valid JSON when decoded
- Can simulate different HTTP status codes
- Can raise URLError/HTTPError for error testing

**Usage**: Used in OllamaProvider tests to mock urllib.request.urlopen responses

---

## Test Data Structures

### Ollama Models Response
**Purpose**: Mock response from Ollama /api/tags endpoint

**Structure**:
```json
{
  "models": [
    {"name": "llama3.2:3b"},
    {"name": "llama3.2:1b"},
    {"name": "gemma2:2b"}
  ]
}
```

**Usage**: Returned by mocked urlopen in OllamaProvider._get_available_models() tests

---

### Test Scenarios

#### Success Scenarios
- Valid provider configuration
- Successful LLM initialization
- Successful agent invocation
- Successful model matching (Ollama)
- Successful API calls (mocked)

#### Error Scenarios
- Missing API key (Gemini)
- Invalid provider name
- Model not found (Ollama)
- Network errors (Ollama HTTP calls)
- Invalid configuration
- Empty or malformed inputs

#### Edge Cases
- Empty message strings
- Model matching with no available models
- Model matching with multiple matches
- Settings with missing environment variables
- Provider initialization with None model
- Agent reinitialization after tool addition

---

## State Transitions

### ChatAgent Lifecycle
1. **Initialization**: Settings loaded → Provider created → Agent initialized
2. **Invocation**: Message received → Agent processes → Response returned
3. **Tool Addition**: Tool added → Agent reinitialized → Tools available
4. **Model Query**: get_model_name() called → Provider queried → Model name returned

### Provider Lifecycle
1. **Initialization**: Config received → Model matched (Ollama) → LLM cached
2. **LLM Retrieval**: get_llm() called → LLM created if None → LLM returned
3. **Invocation**: Prompt received → LLM invoked → Response returned
4. **Validation**: validate_config() called → Config checked → True/False returned

### Settings Lifecycle
1. **Initialization**: Environment loaded → Defaults applied → Settings ready
2. **Provider Config**: get_provider_config() called → Config dict returned
3. **Validation**: validate() called → Basic checks → True/False returned

---

## Relationships

- **Settings** → **Provider**: Settings provides config to Provider
- **Provider** → **LLM**: Provider creates and caches LLM instance
- **ChatAgent** → **Provider**: Agent uses Provider for LLM access
- **ChatAgent** → **Agent**: Agent wraps Langchain agent instance
- **CLI** → **ChatAgent**: CLI commands use ChatAgent for processing

---

## Validation Rules

### Settings Validation
- Ollama: base_url and model must be present
- Gemini: api_key and model must be present
- Unknown provider raises ValueError

### Provider Validation
- BaseProvider: validate_config() returns True by default
- OllamaProvider: model and base_url required
- GeminiProvider: api_key and model required

### Agent Validation
- Unknown provider raises ValueError
- Tools can be added after initialization
- Agent reinitializes when tools added

### Model Matching (Ollama)
- Exact match: requested model found in available models
- Prefix match: requested model matches prefix (e.g., "llama3.2" matches "llama3.2:3b")
- Tagged model: model with ":" requires exact match
- No match: raises ValueError with available models list

