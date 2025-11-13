# ChatAgent API Contract

**Component**: `chat_bot.agent.agent.ChatAgent`  
**Feature**: MCP Tools Integration  
**Date**: 2025-01-27

## Modified Methods

### `__init__(provider, model, settings, tools)`

**Changes**: MCP tools are automatically loaded if `settings.mcp_url` is configured.

**Behavior**:
1. Initialize provider and existing tools as before
2. If `settings.mcp_url` is set and not empty:
   - Call `_load_mcp_tools()` to fetch tools from MCP server
   - Merge MCP tools with existing tools (MCP tools take precedence on name conflicts)
   - Log warnings for tool name conflicts
3. If MCP loading fails:
   - Log error at ERROR level
   - Continue with existing tools only
   - Agent initialization completes successfully
4. Initialize agent with merged tools list

**Error Handling**:
- All MCP-related errors are caught and logged
- Agent initialization never fails due to MCP errors
- Timeout: 5 seconds maximum for MCP connection

**Contract Guarantees**:
- Backward compatible: Works identically when `mcp_url` is `None`
- Graceful degradation: Agent initializes even if MCP fails
- Tool precedence: MCP tools override existing tools with same name

---

## New Methods

### `_load_mcp_tools() -> list`

**Purpose**: Load tools from MCP server and convert to LangChain tool format.

**Returns**: `list` - List of LangChain tool objects from MCP server

**Behavior**:
1. Check if `self.settings.mcp_url` is set
2. If not set, return empty list
3. Create `MultiServerMCPClient` with dictionary config:
   ```python
   client = MultiServerMCPClient({
       "mcp_server": {
           "transport": "streamable_http",
           "url": self.settings.mcp_url
       }
   })
   ```
4. Call async `client.get_tools()` using `asyncio.run()` wrapper
5. Tools are automatically LangChain-compatible (no conversion needed)
6. Handle tool name conflicts:
   - Check for duplicate names with existing `self.tools`
   - Log WARNING for each conflict: `f"MCP tool '{name}' conflicts with existing tool, MCP tool will be used"`
   - MCP tools replace conflicting existing tools
7. Return list of MCP tools

**Error Handling**:
- `TimeoutError`: Log ERROR with timeout details, return empty list
- `ConnectionError`: Log ERROR with connection details, return empty list
- `ValueError`: Log ERROR with error details, return empty list
- Empty tools from server: Log WARNING, return empty list
- Any other exception: Log ERROR with exception details, return empty list

**Contract Guarantees**:
- Never raises exceptions (all errors are caught and logged)
- Always returns a list (may be empty)
- Does not modify `self.tools` directly (caller merges results)

**Example**:
```python
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

def _load_mcp_tools(self) -> list:
    if not self.settings.mcp_url:
        return []
    
    try:
        # Create MCP client
        client = MultiServerMCPClient({
            "mcp_server": {
                "transport": "streamable_http",
                "url": self.settings.mcp_url
            }
        })
        
        # Fetch tools (async method called from sync context)
        mcp_tools = asyncio.run(client.get_tools())
        return mcp_tools
    except Exception as e:
        logger.error(f"Failed to load MCP tools: {e}")
        return []
```

---

## New Attributes

### `mcp_client: Optional[MultiServerMCPClient]`

**Purpose**: Maintain reference to MCP client for potential future use.

**Type**: `Optional[MultiServerMCPClient]` (or appropriate LangChain MCP client type)

**Default**: `None`

**Behavior**:
- Set when MCP connection succeeds
- `None` when MCP is not configured or connection fails
- May be used for future features (reconnection, health checks, etc.)

**Note**: Not required for current implementation but may be useful to store.

---

## Tool Merging Contract

### Tool Name Conflict Resolution

**Rule**: MCP tools take precedence over existing agent tools.

**Process**:
1. Existing tools in `self.tools` are indexed by name
2. For each MCP tool:
   - If name conflicts with existing tool: Log WARNING, replace existing tool
   - If name is unique: Add to tools list
3. Final `self.tools` contains: non-conflicting existing tools + all MCP tools

**Example**:
```python
# Before MCP loading
self.tools = [Tool(name="search", ...), Tool(name="calculator", ...)]

# MCP provides: [Tool(name="search", ...), Tool(name="weather", ...)]
# After merging:
# - "search" from MCP replaces existing "search" (WARNING logged)
# - "calculator" remains (no conflict)
# - "weather" added (new tool)
# Final: [Tool(name="calculator", ...), Tool(name="search", ...), Tool(name="weather", ...)]
```

---

## Contract Guarantees

1. **Backward Compatibility**: Agent behavior unchanged when `mcp_url` is `None`
2. **Error Tolerance**: Agent initialization never fails due to MCP errors
3. **Tool Availability**: All successfully loaded MCP tools are available to agent
4. **Conflict Resolution**: MCP tools always take precedence on name conflicts
5. **Performance**: MCP tool loading completes within 5 seconds or times out

---

## Implementation Notes

- MCP tool loading happens in `__init__` before `_initialize_agent()` is called
- Tools are merged: `self.tools = existing_tools + mcp_tools` (with conflict resolution)
- Use Python's `logging` module for error and warning messages
- Import pattern: `from langchain_mcp_adapters.client import MultiServerMCPClient`
- Use `asyncio.run()` to call async `client.get_tools()` from synchronous context
- Client is stateless - no need to store client instance for future use (optional)

