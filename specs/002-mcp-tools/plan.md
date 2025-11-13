# Implementation Plan: MCP Tools Integration

**Branch**: `002-mcp-tools` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-mcp-tools/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Enable MCP (Model Context Protocol) tool integration for the chat agent when MCP_URL configuration is set. The system will use LangChain's MultiServerMCPClient with streamable HTTP transport to connect to MCP servers and make their tools available to the agent. The implementation must maintain backward compatibility and handle connection failures gracefully.

## Technical Context

**Language/Version**: Python 3.13+ (per pyproject.toml)  
**Primary Dependencies**: langchain>=1.0.5, langchain-mcp-adapters (for MCP tool integration), MultiServerMCPClient with streamable_http transport  
**Storage**: N/A (stateless MCP tool integration)  
**Testing**: pytest>=9.0.0 (existing test infrastructure)  
**Target Platform**: Cross-platform (Windows/Linux/macOS) - CLI application  
**Project Type**: Single Python package (CLI tool)  
**Performance Goals**: MCP tools must load within 5 seconds (per SC-001), agent initialization should not be significantly delayed  
**Constraints**: Must maintain backward compatibility when MCP_URL is unset, graceful error handling for connection failures, timeout handling  
**Scale/Scope**: Single MCP server per agent instance, stateless tool operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Simplicity First**: ✅ YES - Using LangChain's built-in MCP client integration is the simplest approach. No custom MCP protocol implementation needed. Optional configuration keeps the feature simple when not used.

**II. Langchain Agent Architecture**: ✅ YES - Feature integrates directly with LangChain's agent framework using existing tool integration patterns. MCP tools will be added to the agent's tools list, maintaining the existing architecture.

**III. Multi-Provider Support**: ✅ YES - MCP tool integration is provider-agnostic. Tools work with both Ollama and Gemini providers since they integrate at the agent level, not the provider level.

**IV. CLI Interface**: ✅ YES - No new CLI commands required. MCP_URL is a configuration setting that works with existing CLI interface. All functionality remains accessible via existing commands.

**V. MCP Tool Integration**: ✅ YES - This feature directly implements MCP tool integration as specified in Principle V. MCP connections are optional (via MCP_URL config) and non-breaking (graceful error handling when unavailable).

**Violations**: None identified. Feature aligns with all constitutional principles.

**Post-Design Re-evaluation (Phase 1 Complete)**: ✅ All principles still satisfied. Design maintains simplicity through LangChain's built-in MCP integration, follows existing agent architecture patterns, and preserves backward compatibility. No violations introduced during design phase.

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
│   └── agent.py              # ChatAgent class - will add MCP tool loading
├── cli/
│   ├── __init__.py
│   └── main.py               # CLI entry point
├── config/
│   ├── __init__.py
│   └── settings.py           # Settings class - will add MCP_URL config
└── providers/
    ├── __init__.py
    ├── base.py
    ├── gemini.py
    └── ollama.py

tests/
├── __init__.py
├── conftest.py
├── test_agent.py             # Will add MCP tool tests
├── test_config.py            # Will add MCP_URL config tests
├── test_providers_base.py
├── test_providers_gemini.py
└── test_providers_ollama.py
```

**Structure Decision**: Single project structure. MCP integration will be added to existing `chat_bot/agent/agent.py` and `chat_bot/config/settings.py` files. No new modules required - follows existing architecture patterns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
