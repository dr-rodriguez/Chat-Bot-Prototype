# Data Model: MCP Tools Integration

**Feature**: MCP Tools Integration  
**Date**: 2025-01-27

## Entities

### Settings

**Purpose**: Configuration management for MCP server connection.

**Fields**:
- `mcp_url: Optional[str]` - URL of the MCP server endpoint (from `MCP_URL` environment variable)
  - Default: `None` (unset)
  - Validation: Empty strings are normalized to `None`
  - Format: HTTP/HTTPS URL string

**Relationships**:
- Used by `ChatAgent` to determine if MCP tools should be loaded
- Accessed via `settings.mcp_url` in agent initialization

**State Transitions**:
- Unset → Set: When `MCP_URL` environment variable is provided
- Set → Unset: When `MCP_URL` is removed or set to empty string

**Validation Rules**:
- No format validation required (connection will fail gracefully if invalid)
- Empty string is treated as unset (no connection attempt)

---

### ChatAgent

**Purpose**: LangChain-based chat agent with optional MCP tool support.

**Fields** (existing + new):
- `settings: Settings` - Application settings (includes `mcp_url`)
- `tools: list` - List of LangChain tools (includes MCP tools if loaded)
- `mcp_client: Optional[MultiServerMCPClient]` - MCP client instance (optional, for potential future use)
  - Type: `Optional[MultiServerMCPClient]` from `langchain_mcp_adapters.client`
  - Default: `None`
  - Purpose: Optional reference to MCP client (client is stateless, not required to store)

**Relationships**:
- Uses `Settings` to get `mcp_url` configuration
- Creates `MultiServerMCPClient` instance temporarily during tool loading (stateless design)
- Aggregates MCP tools into `tools` list

**State Transitions**:
- Initialization without MCP: `tools = []` (or existing tools)
- Initialization with MCP (success): `tools = [existing_tools + mcp_tools]` (client created temporarily, not stored)
- Initialization with MCP (failure): `tools = [existing_tools]` (MCP tools not added)

**Validation Rules**:
- MCP tools are only loaded if `settings.mcp_url` is not `None` and not empty
- Tool name conflicts: MCP tools take precedence, existing tools with same name are replaced
- Agent initialization must complete even if MCP connection fails

---

### MCP Tool

**Purpose**: Represents a tool provided by an MCP server.

**Fields** (LangChain tool interface):
- `name: str` - Tool name (must be unique within agent's tools)
- `description: str` - Tool description for agent use
- `parameters: dict` - Tool input parameters schema
- `handler: callable` - Function to execute the tool

**Relationships**:
- Provided by MCP server via `MultiServerMCPClient`
- Converted to LangChain tool format
- Added to `ChatAgent.tools` list

**State Transitions**:
- Not loaded → Loaded: When MCP server connection succeeds and tools are fetched
- Loaded → Removed: If MCP connection fails during operation (tool becomes unavailable)

**Validation Rules**:
- Tool names must be valid Python identifiers (enforced by LangChain)
- Tool parameters must match LangChain tool schema format
- Duplicate tool names: MCP tools override existing agent tools

---

## Data Flow

### Agent Initialization Flow

```
1. ChatAgent.__init__() called
2. Settings instance created/accessed
3. Check settings.mcp_url:
   - If None/empty: Skip MCP loading, proceed with existing tools
   - If set: Attempt MCP connection
4. _load_mcp_tools() called:
   - Create MultiServerMCPClient with streamable_http transport
   - Connect to MCP server (5-second timeout)
   - Fetch available tools
   - Convert to LangChain tool format
   - Handle name conflicts (MCP tools take precedence)
   - Log warnings for conflicts
5. Merge tools: existing_tools + mcp_tools
6. _initialize_agent() called with merged tools
7. Agent ready for use
```

### Error Handling Flow

```
MCP Connection Attempt:
- Success: Tools added, agent initialized normally
- TimeoutError: Log ERROR, continue without MCP tools
- ConnectionError: Log ERROR, continue without MCP tools
- ValueError (invalid URL): Log ERROR, continue without MCP tools
- Empty tools from server: Log WARNING, continue without MCP tools
- Any other exception: Log ERROR with details, continue without MCP tools
```

---

## State Management

### Agent States

1. **Uninitialized**: ChatAgent object created but `__init__` not complete
2. **Initialized (No MCP)**: Agent ready, no MCP tools available
3. **Initialized (With MCP)**: Agent ready, MCP tools available
4. **Initialized (MCP Failed)**: Agent ready, MCP connection failed, no MCP tools

### MCP Connection States

1. **Not Configured**: `mcp_url` is `None` or empty
2. **Connecting**: Attempting to connect to MCP server
3. **Connected**: Successfully connected, tools loaded
4. **Failed**: Connection failed, agent continues without MCP tools

---

## Constraints

- **Backward Compatibility**: Agent must work identically when `MCP_URL` is unset
- **Timeout**: MCP connection must complete or timeout within 5 seconds
- **Error Tolerance**: Agent initialization must never fail due to MCP errors
- **Tool Uniqueness**: Tool names must be unique within agent's tool list (MCP tools override conflicts)
- **Stateless**: MCP tools operate statelessly (no session management)

---

## Notes

- MCP client instance may be stored in `ChatAgent` for potential future use (e.g., reconnection)
- Tool loading is synchronous during initialization (no async operations)
- No persistent state is maintained for MCP connections
- MCP server unavailability during agent operation is handled at tool execution time (LangChain error handling)

