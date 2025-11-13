# Quickstart: MCP Tools Integration

**Feature**: MCP Tools Integration  
**Date**: 2025-01-27

## Overview

This feature enables the chat agent to automatically use tools from an MCP (Model Context Protocol) server when the `MCP_URL` configuration is set. The agent will connect to the MCP server, fetch available tools, and make them available for use during conversations.

## Prerequisites

- Python 3.13+
- `langchain-mcp-adapters` package installed: `pip install langchain-mcp-adapters`
- Access to an MCP server endpoint
- MCP server must support streamable HTTP transport

## Configuration

### Setting MCP_URL

Set the `MCP_URL` environment variable to point to your MCP server:

**Linux/macOS**:
```bash
export MCP_URL="http://localhost:8000/mcp"
```

**Windows (PowerShell)**:
```powershell
$env:MCP_URL="http://localhost:8000/mcp"
```

**Windows (CMD)**:
```cmd
set MCP_URL=http://localhost:8000/mcp
```

**Using .env file**:
```env
MCP_URL=http://localhost:8000/mcp
```

### Disabling MCP Tools

To disable MCP tools, either:
- Unset the `MCP_URL` environment variable
- Set `MCP_URL` to an empty string: `MCP_URL=""`
- Remove `MCP_URL` from your `.env` file

## Usage

### Basic Usage

Once `MCP_URL` is configured, the agent will automatically load MCP tools during initialization:

```python
from chat_bot.agent.agent import ChatAgent
from chat_bot.config.settings import Settings

# MCP_URL is set in environment
settings = Settings()
agent = ChatAgent(settings=settings)

# Agent now has access to MCP tools
response = agent.invoke("Use the weather tool to check the forecast")
```

### With Existing Tools

MCP tools are merged with any existing tools you provide:

```python
from chat_bot.agent.agent import ChatAgent
from langchain.tools import Tool

# Existing tool
calculator = Tool(
    name="calculator",
    func=lambda x: eval(x),
    description="Performs calculations"
)

# MCP tools are automatically added
agent = ChatAgent(tools=[calculator])

# Agent has: calculator tool + all MCP tools
```

### Tool Name Conflicts

If an MCP tool has the same name as an existing tool, the MCP tool takes precedence:

```python
# Existing tool named "search"
existing_search = Tool(name="search", ...)

# MCP provides a tool also named "search"
agent = ChatAgent(tools=[existing_search])

# Result: MCP's "search" tool is used
# Warning logged: "MCP tool 'search' conflicts with existing tool, MCP tool will be used"
```

## Error Handling

The agent handles MCP connection failures gracefully:

### Connection Timeout

If the MCP server doesn't respond within 5 seconds:
- Agent initializes without MCP tools
- ERROR logged: "Failed to load MCP tools: timeout after 5 seconds"

### Invalid URL

If `MCP_URL` is malformed:
- Agent initializes without MCP tools
- ERROR logged: "Failed to load MCP tools: invalid URL"

### Server Unavailable

If the MCP server is unreachable:
- Agent initializes without MCP tools
- ERROR logged: "Failed to load MCP tools: connection refused"

### Empty Tools

If the MCP server provides no tools:
- Agent initializes normally
- WARNING logged: "MCP server provided no tools"

## Examples

### Example 1: Local MCP Server

```python
import os
os.environ["MCP_URL"] = "http://localhost:8000/mcp"

from chat_bot.agent.agent import ChatAgent

agent = ChatAgent()
# MCP tools from localhost:8000 are now available
```

### Example 2: Remote MCP Server

```python
import os
os.environ["MCP_URL"] = "https://mcp.example.com/api/tools"

from chat_bot.agent.agent import ChatAgent

agent = ChatAgent()
# MCP tools from remote server are now available
```

### Example 3: Conditional MCP Usage

```python
from chat_bot.agent.agent import ChatAgent
from chat_bot.config.settings import Settings

settings = Settings()

if settings.mcp_url:
    print(f"MCP tools enabled from: {settings.mcp_url}")
else:
    print("MCP tools not configured")

agent = ChatAgent(settings=settings)
```

## Testing

### Verify MCP Tools Are Loaded

```python
from chat_bot.agent.agent import ChatAgent

agent = ChatAgent()

# Check if agent has tools (including MCP tools)
print(f"Agent has {len(agent.tools)} tools")

# List tool names
for tool in agent.tools:
    print(f"- {tool.name}")
```

### Test Error Handling

```python
import os
os.environ["MCP_URL"] = "http://invalid-server:9999/mcp"

from chat_bot.agent.agent import ChatAgent

# Agent should initialize successfully even with invalid URL
agent = ChatAgent()
# ERROR logged, but agent works normally
```

## Troubleshooting

### MCP Tools Not Loading

1. **Check MCP_URL is set**:
   ```python
   from chat_bot.config.settings import Settings
   settings = Settings()
   print(settings.mcp_url)  # Should not be None
   ```

2. **Check MCP server is accessible**:
   ```bash
   curl http://localhost:8000/mcp
   ```

3. **Check logs for errors**:
   - Look for ERROR level messages about MCP connection failures
   - Verify timeout settings (10 seconds default)

### Tool Conflicts

- Check logs for WARNING messages about tool name conflicts
- MCP tools automatically override existing tools with same name
- Rename existing tools if you want to keep them

### Performance Issues

- MCP tool loading has a 10-second timeout
- If loading is slow, check MCP server performance
- Agent initialization may be delayed if MCP connection is slow

## Next Steps

- See [data-model.md](./data-model.md) for detailed data structures
- See [contracts/](./contracts/) for API documentation
- See [spec.md](./spec.md) for full feature specification

