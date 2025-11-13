# Research: MCP Tools Integration

**Feature**: MCP Tools Integration  
**Date**: 2025-01-27  
**Status**: Complete

## Research Questions

### 1. LangChain MCP Package and API

**Question**: What is the correct package name and version for LangChain MCP integration? How do we use MultiServerMCPClient with streamable_http transport?

**Research Findings**:
- LangChain provides MCP integration through the `langchain-mcp-adapters` package
- MultiServerMCPClient is the recommended client for connecting to MCP servers
- Streamable HTTP transport uses HTTP-based communication for MCP protocol
- Client is stateless by default - each tool invocation creates a fresh session
- Reference documentation: https://docs.langchain.com/oss/python/langchain/mcp

**Decision**: 
- Use `langchain-mcp-adapters` package
- Use `MultiServerMCPClient` from `langchain_mcp_adapters.client`
- Configure with dictionary: `{"server_name": {"transport": "streamable_http", "url": "http://..."}}`
- Use async `get_tools()` method to fetch tools
- Add package to `pyproject.toml` dependencies

**Rationale**: 
- LangChain's official MCP integration provides the simplest path
- MultiServerMCPClient is designed for multiple server connections (we'll use it for single server)
- Streamable HTTP is specified in requirements and is the standard transport for hosted MCP servers
- Stateless design simplifies implementation and aligns with requirements

**Alternatives Considered**:
- Custom MCP client implementation: Rejected - too complex, violates Simplicity First principle
- Direct HTTP calls to MCP server: Rejected - would require implementing MCP protocol ourselves

**Implementation Notes**:
- Package: `langchain-mcp-adapters` (add to dependencies)
- Import: `from langchain_mcp_adapters.client import MultiServerMCPClient`
- Client initialization: `MultiServerMCPClient({"mcp_server": {"transport": "streamable_http", "url": mcp_url}})`
- Tool fetching: `await client.get_tools()` (async method - use `asyncio.run()` in sync context)
- Transport: Use `"streamable_http"` (not `"streamable-http"` - note underscore)

---

### 2. MCP Tool Integration Pattern

**Question**: How do we convert MCP tools to LangChain tools that can be used by the agent?

**Research Findings**:
- LangChain's MCP integration should provide tools that are compatible with LangChain's tool interface
- MCP tools need to be converted to LangChain tool objects
- Tools are added to the agent's tools list before agent initialization

**Decision**:
- Use `MultiServerMCPClient` to connect to MCP server
- Call `await client.get_tools()` to fetch tools (returns LangChain-compatible tools automatically)
- Handle async call in synchronous `__init__` using `asyncio.run()`
- Add tools to agent's `self.tools` list before calling `_initialize_agent()`
- Handle tool name conflicts by preferring MCP tools and logging warnings

**Rationale**:
- LangChain's MCP integration automatically converts MCP tools to LangChain tool format
- `get_tools()` returns a list of LangChain-compatible tool objects
- Following existing pattern in `ChatAgent.__init__` where tools are passed to agent initialization
- Name conflict resolution aligns with FR-011 requirement

**Alternatives Considered**:
- Manual tool conversion: Rejected - LangChain handles this automatically
- Separate tool namespace: Rejected - adds complexity, not required by spec
- Async agent initialization: Rejected - would require significant refactoring

**Implementation Notes**:
- Use `client.get_tools()` async method (documented in LangChain MCP docs)
- Tools are automatically LangChain-compatible - no manual conversion needed
- Use `asyncio.run()` to call async method from synchronous `__init__`
- Merge MCP tools with existing tools, with MCP tools taking precedence on name conflicts
- Client is stateless - no need to maintain session between tool calls

---

### 3. Error Handling and Timeout Configuration

**Question**: How should we handle connection timeouts and errors when connecting to MCP servers?

**Research Findings**:
- Network operations can fail due to timeouts, connection errors, or invalid URLs
- Python's standard timeout mechanisms should be used
- Error handling should be graceful and not prevent agent initialization

**Decision**:
- Set a reasonable timeout (5 seconds per SC-001) for MCP server connection
- Catch all exceptions during MCP tool loading (ConnectionError, TimeoutError, ValueError, etc.)
- Log errors at ERROR level as specified in FR-009
- Continue agent initialization without MCP tools if connection fails
- Handle empty MCP_URL (empty string) by treating as unset (no connection attempt)

**Rationale**:
- 5-second timeout aligns with SC-001 success criteria
- Graceful degradation ensures backward compatibility (FR-005)
- Comprehensive error handling covers all failure scenarios (FR-006, FR-007, FR-008)

**Alternatives Considered**:
- Retry logic: Rejected - adds complexity, not required by spec
- Fail-fast on errors: Rejected - violates FR-006 requirement for graceful handling

**Implementation Notes**:
- Use `timeout=5` parameter when connecting to MCP server
- Wrap MCP connection in try-except block
- Log specific error details for debugging
- Check if MCP_URL is empty or None before attempting connection

---

### 4. Configuration Management

**Question**: How should MCP_URL be added to the Settings class?

**Research Findings**:
- Existing Settings class uses environment variables via `os.getenv()`
- Configuration follows pattern: `os.getenv("KEY", default_value)`
- Optional settings can return None or empty string

**Decision**:
- Add `mcp_url` attribute to Settings class
- Load from `MCP_URL` environment variable
- Default to `None` (not set)
- Treat empty string as `None` (unset)
- No validation required (connection will fail gracefully if invalid)

**Rationale**:
- Follows existing configuration pattern in `settings.py`
- Optional setting aligns with backward compatibility requirement (FR-005)
- Empty string handling aligns with clarification from spec

**Alternatives Considered**:
- Required setting with validation: Rejected - violates FR-005 (backward compatibility)
- Separate MCP settings class: Rejected - adds unnecessary complexity

**Implementation Notes**:
- Add to Settings.__init__: `self.mcp_url: Optional[str] = os.getenv("MCP_URL") or None`
- Normalize empty strings: `self.mcp_url = self.mcp_url.strip() if self.mcp_url else None`
- Access via `settings.mcp_url` in ChatAgent

---

### 5. Tool Loading Timing

**Question**: When should MCP tools be loaded - during ChatAgent initialization or lazily?

**Research Findings**:
- Agent initialization happens in `ChatAgent.__init__`
- Tools must be available before `_initialize_agent()` is called
- Lazy loading would require reinitializing the agent

**Decision**:
- Load MCP tools during `ChatAgent.__init__` using `asyncio.run()` to handle async `get_tools()` call
- Load before calling `_initialize_agent()`
- If loading fails, proceed with existing tools only
- Agent initialization should complete within 5 seconds including MCP tool loading (SC-001)

**Rationale**:
- Loading during initialization ensures tools are available when agent is created
- Using `asyncio.run()` allows calling async method from synchronous context
- Fits existing initialization pattern with minimal changes
- Timeout ensures initialization doesn't hang indefinitely

**Alternatives Considered**:
- Lazy loading on first tool use: Rejected - requires agent reinitialization, adds complexity
- Background loading: Rejected - adds async complexity, not needed for single server
- Making `__init__` async: Rejected - would break existing API and require significant refactoring

**Implementation Notes**:
- Create helper method `_load_mcp_tools()` called from `__init__`
- Use `asyncio.run()` to execute async `client.get_tools()` call
- Merge MCP tools with existing tools before agent initialization
- Handle all exceptions in `_load_mcp_tools()` to prevent initialization failure
- Import: `import asyncio` at module level

---

## Summary of Decisions

1. **Package**: Use `langchain-mcp-adapters` - add to dependencies
2. **Client**: Use `MultiServerMCPClient` from `langchain_mcp_adapters.client` with `streamable_http` transport
3. **Client Config**: Dictionary format: `{"server_name": {"transport": "streamable_http", "url": mcp_url}}`
4. **Tool Integration**: Use async `client.get_tools()` which returns LangChain-compatible tools automatically
5. **Async Handling**: Use `asyncio.run()` to call async method from synchronous `__init__`
6. **Error Handling**: Graceful degradation with ERROR level logging, 5-second timeout
7. **Configuration**: Add `MCP_URL` to Settings class as optional environment variable
8. **Loading**: Load during agent initialization using `asyncio.run()` wrapper

## Remaining Clarifications

All technical clarifications have been resolved. Implementation can proceed with the following verification steps:

1. Test `langchain-mcp-adapters` package installation
2. Verify `asyncio.run()` works correctly in `__init__` context
3. Test with actual MCP server to confirm tool loading works correctly

## References

- LangChain MCP Documentation: https://docs.langchain.com/oss/python/langchain/mcp
- Feature Specification: [spec.md](./spec.md)
- Constitution: `.specify/memory/constitution.md`

