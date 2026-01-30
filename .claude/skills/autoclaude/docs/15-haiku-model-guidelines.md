---
title: "Haiku Model Guidelines"
updated: "2025-12-20"
---

# Haiku Model

## Characteristics
| Aspect | Haiku | Sonnet/Opus |
|--------|-------|-------------|
| Context | Short | Long |
| Cost | Cheap | Expensive |
| Speed | Fast | Slower |

## Rules
1. **Atomic Steps**: 1 step = 1 action = 1 MCP call
2. **Explicit MCP**: Write full tool name
3. **Verify Output**: Check actual files, not diary

## Prompt Template
```
Read [instruction], ultrathink, no quit,
CALL [mcp_tool] for each step,
NO fake data, follow atomic steps,
start from [state file]
```

## When to Use
| Use Case | Model |
|----------|-------|
| Repetitive tasks | Haiku |
| Complex reasoning | Sonnet |
| Browser automation | Haiku + atomic |
| Batch processing | Haiku |

## Checklist
- [ ] Atomic steps file? (1 step = 1 action)
- [ ] MCP calls explicit?
- [ ] State file ready?
- [ ] Verification method?
