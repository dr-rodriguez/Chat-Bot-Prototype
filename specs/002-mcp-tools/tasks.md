# Tasks: MCP Tools Integration

**Feature**: MCP Tools Integration  
**Branch**: `002-mcp-tools`  
**Date**: 2025-01-27  
**Status**: Ready for Implementation

## Summary

This document outlines the implementation tasks for integrating MCP (Model Context Protocol) tools into the chat agent. The feature enables the agent to automatically load and use tools from an MCP server when the `MCP_URL` configuration is set.

**Total Tasks**: 18  
**User Story Breakdown**:
- User Story 1 (P1): 6 tasks
- User Story 2 (P2): 4 tasks  
- User Story 3 (P2): 2 tasks
- Setup & Foundational: 4 tasks
- Polish: 2 tasks

**MVP Scope**: User Story 1 (Enable MCP Tools When Configured) - 6 tasks

## Implementation Strategy

**MVP First**: Start with User Story 1 to deliver core functionality. User Stories 2 and 3 can be implemented incrementally.

**Incremental Delivery**:
1. Phase 1-2: Setup and configuration foundation
2. Phase 3: Core MCP tool loading (MVP)
3. Phase 4-5: Error handling and multi-tool support
4. Phase 6: Final polish and documentation

## Dependencies

### User Story Completion Order

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational: Settings.mcp_url)
    ↓
Phase 3 (US1: Enable MCP Tools) ← MVP
    ↓
Phase 4 (US2: Handle Connection Failures)
    ↓
Phase 5 (US3: Support Multiple Tools)
    ↓
Phase 6 (Polish)
```

**Note**: User Stories 2 and 3 can be implemented in parallel after User Story 1 is complete, as they enhance existing functionality rather than blocking each other.

## Parallel Execution Opportunities

### Within User Story 1
- T005 (Settings.mcp_url) and T006 (Add dependency) can be done in parallel
- T007-T009 (Agent implementation) must be sequential

### After User Story 1
- User Stories 2 and 3 can be implemented in parallel (different aspects of the same feature)

## Phase 1: Setup

**Goal**: Prepare project dependencies and structure for MCP integration.

### Tasks

- [ ] T001 Add langchain-mcp-adapters dependency to pyproject.toml
- [ ] T002 Update project documentation to mention MCP tool support in README.md

**Independent Test Criteria**: Project dependencies updated, documentation reflects MCP support.

---

## Phase 2: Foundational - Configuration

**Goal**: Add MCP_URL configuration support to Settings class.

**Why Before User Stories**: All user stories depend on Settings.mcp_url being available.

### Tasks

- [ ] T003 [P] Add mcp_url attribute to Settings class in chat_bot/config/settings.py
- [ ] T004 [P] Add test for Settings.mcp_url in tests/test_config.py

**Independent Test Criteria**: Settings class loads MCP_URL from environment variable, normalizes empty strings to None, and can be tested independently.

---

## Phase 3: User Story 1 - Enable MCP Tools When Configured (Priority: P1)

**Story Goal**: As a user, I want the chat agent to automatically use MCP tools from a configured MCP server so that I can extend the agent's capabilities without code changes.

**Independent Test Criteria**: Can be fully tested by setting MCP_URL environment variable, creating an agent, and verifying that tools from the MCP server are available to the agent.

### Tasks

- [ ] T005 [US1] Import required MCP dependencies in chat_bot/agent/agent.py
- [ ] T006 [US1] Implement _load_mcp_tools() method in chat_bot/agent/agent.py
- [ ] T007 [US1] Integrate MCP tool loading into ChatAgent.__init__() in chat_bot/agent/agent.py
- [ ] T008 [US1] Implement tool merging logic with MCP tool precedence in chat_bot/agent/agent.py
- [ ] T009 [US1] Add test for successful MCP tool loading in tests/test_agent.py
- [ ] T010 [US1] Add test for backward compatibility (no MCP_URL) in tests/test_agent.py

**Acceptance Scenarios**:
1. Given MCP_URL is set in configuration, When I create a ChatAgent instance, Then the agent has access to tools provided by the MCP server
2. Given MCP_URL is set in configuration, When I invoke the agent with a message requiring MCP tools, Then the agent successfully uses those tools to complete the task
3. Given MCP_URL is not set in configuration, When I create a ChatAgent instance, Then the agent works normally without MCP tools (backward compatible)

---

## Phase 4: User Story 2 - Handle MCP Server Connection Failures (Priority: P2)

**Story Goal**: As a user, I want the system to handle MCP server connection failures gracefully so that the agent continues to function even if the MCP server is unavailable.

**Independent Test Criteria**: Can be fully tested by configuring an invalid or unreachable MCP_URL and verifying that the agent initializes successfully with appropriate error handling.

### Tasks

- [ ] T011 [US2] Add error handling for connection failures in _load_mcp_tools() in chat_bot/agent/agent.py
- [ ] T012 [US2] Add timeout handling (5 seconds) in _load_mcp_tools() in chat_bot/agent/agent.py
- [ ] T013 [US2] Add ERROR level logging for connection failures in chat_bot/agent/agent.py
- [ ] T014 [US2] Add tests for connection failure scenarios in tests/test_agent.py

**Acceptance Scenarios**:
1. Given MCP_URL points to an unreachable server, When I create a ChatAgent instance, Then the agent initializes without MCP tools and logs an ERROR level message
2. Given MCP_URL is malformed, When I create a ChatAgent instance, Then the agent initializes without MCP tools and logs an ERROR level message
3. Given MCP server becomes unavailable after agent initialization, When I invoke the agent, Then the agent handles the error gracefully and continues to function with available tools

---

## Phase 5: User Story 3 - Support Multiple MCP Tools (Priority: P2)

**Story Goal**: As a user, I want the agent to access all tools provided by the MCP server so that I can leverage the full capabilities of the configured MCP server.

**Independent Test Criteria**: Can be fully tested by configuring an MCP server with multiple tools and verifying that all tools are available to the agent.

### Tasks

- [ ] T015 [US3] Verify multiple tools are loaded from MCP server in chat_bot/agent/agent.py
- [ ] T016 [US3] Add test for multiple MCP tools in tests/test_agent.py

**Acceptance Scenarios**:
1. Given MCP server provides multiple tools, When I create a ChatAgent instance, Then all tools from the MCP server are available to the agent
2. Given MCP server provides multiple tools, When I invoke the agent with a message, Then the agent can use any of the available MCP tools as needed

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Final refinements, edge cases, and documentation.

### Tasks

- [ ] T017 Handle empty MCP_URL string normalization in chat_bot/config/settings.py
- [ ] T018 Add WARNING logging for empty tools from MCP server in chat_bot/agent/agent.py

**Edge Cases Covered**:
- Empty MCP_URL string treated as unset
- MCP server provides no tools (WARNING logged)
- Tool name conflicts (MCP tools take precedence, WARNING logged)

---

## Task Details

### T001: Add langchain-mcp-adapters dependency
**File**: `pyproject.toml`  
**Action**: Add `langchain-mcp-adapters` to dependencies list in `[project]` section.  
**Reference**: research.md decision #1

### T002: Update project documentation
**File**: `README.md`  
**Action**: Add section about MCP tool support, mentioning MCP_URL configuration.  
**Reference**: quickstart.md usage examples

### T003: Add mcp_url attribute to Settings
**File**: `chat_bot/config/settings.py`  
**Action**: Add `self.mcp_url: Optional[str] = os.getenv("MCP_URL") or None` in `__init__()`, normalize empty strings to None.  
**Reference**: contracts/settings-api.md, data-model.md Settings entity

### T004: Add test for Settings.mcp_url
**File**: `tests/test_config.py`  
**Action**: Add tests for MCP_URL loading, empty string normalization, and None when unset.  
**Reference**: contracts/settings-api.md examples

### T005: Import required MCP dependencies
**File**: `chat_bot/agent/agent.py`  
**Action**: Add imports: `import asyncio`, `from langchain_mcp_adapters.client import MultiServerMCPClient`, `import logging`.  
**Reference**: research.md decision #1, contracts/agent-api.md

### T006: Implement _load_mcp_tools() method
**File**: `chat_bot/agent/agent.py`  
**Action**: Create `_load_mcp_tools() -> list` method that creates MultiServerMCPClient, calls `asyncio.run(client.get_tools())`, returns list of tools or empty list on error.  
**Reference**: contracts/agent-api.md _load_mcp_tools() contract, research.md decision #2

### T007: Integrate MCP tool loading into __init__
**File**: `chat_bot/agent/agent.py`  
**Action**: In `__init__()`, after setting `self.tools`, call `_load_mcp_tools()` if `settings.mcp_url` is set, before `_initialize_agent()`.  
**Reference**: contracts/agent-api.md __init__() changes, data-model.md Agent Initialization Flow

### T008: Implement tool merging logic
**File**: `chat_bot/agent/agent.py`  
**Action**: Merge MCP tools with existing tools, MCP tools take precedence on name conflicts. Log WARNING for conflicts.  
**Reference**: contracts/agent-api.md Tool Merging Contract, data-model.md tool conflict resolution

### T009: Add test for successful MCP tool loading
**File**: `tests/test_agent.py`  
**Action**: Add test that mocks MCP server, verifies tools are loaded and available to agent.  
**Reference**: spec.md User Story 1 acceptance scenarios

### T010: Add test for backward compatibility
**File**: `tests/test_agent.py`  
**Action**: Add test that verifies agent works normally when MCP_URL is not set.  
**Reference**: spec.md User Story 1 acceptance scenario #3, FR-005

### T011: Add error handling for connection failures
**File**: `chat_bot/agent/agent.py`  
**Action**: Wrap MCP connection in try-except, catch ConnectionError, ValueError, and generic Exception. Log ERROR and return empty list.  
**Reference**: contracts/agent-api.md error handling, research.md decision #3

### T012: Add timeout handling
**File**: `chat_bot/agent/agent.py`  
**Action**: Add 5-second timeout to MCP connection. Catch TimeoutError, log ERROR, return empty list.  
**Reference**: spec.md SC-001, research.md decision #3

### T013: Add ERROR level logging
**File**: `chat_bot/agent/agent.py`  
**Action**: Use `logging.error()` for all MCP connection failures with detailed error messages.  
**Reference**: spec.md FR-009, contracts/agent-api.md error handling

### T014: Add tests for connection failure scenarios
**File**: `tests/test_agent.py`  
**Action**: Add tests for unreachable server, malformed URL, timeout scenarios. Verify agent initializes successfully and errors are logged.  
**Reference**: spec.md User Story 2 acceptance scenarios

### T015: Verify multiple tools are loaded
**File**: `chat_bot/agent/agent.py`  
**Action**: Ensure _load_mcp_tools() handles multiple tools correctly (should work automatically if T006 is correct).  
**Reference**: spec.md User Story 3, FR-010

### T016: Add test for multiple MCP tools
**File**: `tests/test_agent.py`  
**Action**: Add test with mocked MCP server providing multiple tools, verify all are available.  
**Reference**: spec.md User Story 3 acceptance scenarios

### T017: Handle empty MCP_URL string normalization
**File**: `chat_bot/config/settings.py`  
**Action**: Ensure empty string is normalized to None in Settings.__init__() (should be in T003, verify/refine).  
**Reference**: spec.md clarification, contracts/settings-api.md

### T018: Add WARNING logging for empty tools
**File**: `chat_bot/agent/agent.py`  
**Action**: In _load_mcp_tools(), if server connection succeeds but returns empty tools list, log WARNING.  
**Reference**: spec.md clarification, FR-012

---

## Validation Checklist

- [x] All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- [x] All user stories have corresponding task phases
- [x] All tasks have clear file paths
- [x] Dependencies are clearly identified
- [x] Parallel execution opportunities are marked with [P]
- [x] User story labels [US1], [US2], [US3] are present on story phase tasks
- [x] Setup and foundational phases have no story labels
- [x] Each user story phase has independent test criteria
- [x] MVP scope is clearly identified (User Story 1)

---

## Notes

- **Async Handling**: Use `asyncio.run()` to call async `client.get_tools()` from synchronous `__init__()` context (research.md decision #5)
- **Timeout**: 5 seconds maximum for MCP connection (SC-001)
- **Error Tolerance**: Agent initialization must never fail due to MCP errors (FR-006)
- **Tool Precedence**: MCP tools override existing tools with same name (FR-011)
- **Backward Compatibility**: Agent must work identically when MCP_URL is unset (FR-005)

