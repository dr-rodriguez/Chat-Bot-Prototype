# Chat-Bot-Prototype

A simple AI chat bot prototype built with Langchain, supporting multiple LLM providers (Ollama and Google Gemini) with a command-line interface.

## Overview

Chat-Bot-Prototype is an intermediate-level project designed for data scientists. It provides a straightforward, maintainable implementation of a Langchain-based chat agent that can work with both local (Ollama) and external (Google Gemini) LLM providers.

## Features

- **Multi-Provider Support**: Switch between Ollama (local) and Google Gemini (external) providers
- **Langchain Agent Architecture**: Built on Langchain for modular, provider-agnostic agent logic
- **CLI Interface**: Command-line interface using Click with both interactive and non-interactive modes
- **Simple Configuration**: Environment-based configuration with sensible defaults
- **Extensible Design**: Easy to add new providers or tools

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Chat-Bot-Prototype
```

2. Install dependencies using uv:
```bash
uv sync
```

3. (Optional) Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Create a `.env` file in the project root with the following variables:

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Google Gemini Configuration (optional)
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
```

### Provider Setup

**Ollama (Local)**:
- Install and run [Ollama](https://ollama.ai/)
- Pull a model: `ollama pull llama3.2`
- No API key required

**Google Gemini (External)**:
- Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Set `GEMINI_API_KEY` in your `.env` file

## Usage

### Interactive Chat Mode

Start an interactive chat session:

```bash
uv run python -m chat_bot.cli.main chat
```

With specific provider:

```bash
uv run python -m chat_bot.cli.main chat --provider ollama
uv run python -m chat_bot.cli.main chat --provider gemini
```

With custom model:

```bash
uv run python -m chat_bot.cli.main chat --provider ollama --model llama3.1
```

### Non-Interactive Mode

Run a single message:

```bash
uv run python -m chat_bot.cli.main run "Hello, how are you?"
```

Pipe input from stdin:

```bash
echo "What is Python?" | uv run python -m chat_bot.cli.main chat --no-interactive
```

## Project Structure

```
src/
└── chat_bot/
    ├── cli/
    │   └── main.py              # Click CLI entry point
    ├── agent/
    │   └── agent.py             # Langchain agent core
    ├── providers/
    │   ├── base.py              # Base provider interface
    │   ├── ollama.py            # Ollama provider
    │   └── gemini.py            # Gemini provider
    └── config/
        └── settings.py          # Configuration management

tests/
└── (test files)

.env.example                     # Environment configuration template
```

## Architecture

The project follows a modular architecture:

- **CLI Layer**: Click-based command-line interface
- **Agent Layer**: Langchain agent orchestration with tool support
- **Provider Layer**: Abstracted LLM provider implementations
- **Config Layer**: Environment-based configuration management

Providers are isolated and swappable without code changes. The agent uses Langchain's interfaces to remain provider-agnostic.

## Development

### Running Tests

```bash
uv run pytest
```

### Adding a New Provider

1. Create a new provider class in `src/chat_bot/providers/` inheriting from `BaseProvider`
2. Implement required methods: `get_llm()`, `invoke()`, `validate_config()`
3. Add provider configuration to `Settings` class
4. Register provider in `ChatAgent.__init__()`

## License

See LICENSE file for details.
