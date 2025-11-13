# Settings API Contract

**Component**: `chat_bot.config.settings.Settings`  
**Feature**: MCP Tools Integration  
**Date**: 2025-01-27

## New Attributes

### `mcp_url: Optional[str]`

**Purpose**: URL of the MCP server endpoint for tool integration.

**Source**: `MCP_URL` environment variable

**Default**: `None` (when environment variable is not set or is empty)

**Behavior**:
- Loaded from `MCP_URL` environment variable in `__init__()`
- Empty strings are normalized to `None`
- No format validation (invalid URLs will fail at connection time)
- Optional setting - agent works normally when `None`

**Example**:
```python
# MCP_URL=http://localhost:8000/mcp
settings = Settings()
assert settings.mcp_url == "http://localhost:8000/mcp"

# MCP_URL not set
settings = Settings()
assert settings.mcp_url is None

# MCP_URL=""
settings = Settings()
assert settings.mcp_url is None  # Empty string normalized to None
```

**Access Pattern**:
```python
settings = Settings()
if settings.mcp_url:
    # MCP is configured
    connect_to_mcp(settings.mcp_url)
```

---

## Contract Guarantees

1. **Backward Compatibility**: Existing code that doesn't use `mcp_url` continues to work unchanged
2. **Optional**: `mcp_url` may be `None` - this is a valid state
3. **Normalization**: Empty strings are always converted to `None`
4. **No Validation**: No URL format validation is performed (simplicity first)

---

## Implementation Notes

- Add to `Settings.__init__()`:
  ```python
  self.mcp_url: Optional[str] = os.getenv("MCP_URL") or None
  if self.mcp_url:
      self.mcp_url = self.mcp_url.strip()
      if not self.mcp_url:
          self.mcp_url = None
  ```

