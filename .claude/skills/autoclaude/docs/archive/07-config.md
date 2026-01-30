---
title: Config Reference
updated: 2025-12-03
---

# Config Reference

**File**: `config.json`

## Structure

```json
{
  "claude_flags": {
    "verbose": true,
    "dangerously_skip_permissions": true
  },
  "prompt_prefix": "MANDATORY RULES: ...",
  "xterm": {
    "font_family": "Ubuntu Sans Mono",
    "font_size": 13,
    "auto_close_delay": 30
  },
  "telegram": {
    "token": "...",
    "chat_id": "..."
  }
}
```

## Fields

| Field | Mô tả |
|-------|-------|
| `claude_flags.verbose` | Bật `--verbose` |
| `claude_flags.dangerously_skip_permissions` | Bật `--dangerously-skip-permissions` |
| `prompt_prefix` | Prefix inject vào đầu mỗi prompt |
| `xterm.auto_close_delay` | Delay trước khi tự close (giây) |
| `telegram.token` | Bot token |
| `telegram.chat_id` | Chat ID |

## Prompt Prefix

```
MANDATORY RULES:
(1) You MUST operate ONLY within the current git branch
    - DO NOT switch to any other branch
(2) You MUST commit frequently and continuously
(3) You MUST NOT run destructive git commands without approval
    - reset --hard, push --force, etc.
```
