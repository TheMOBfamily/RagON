---
title: "Autoclaude Loop Mode - Example"
date: "2026-01-26"
---

## Loop Mode Example

### Scenario

Chạy 30 tasks từ init file, dùng haiku model, timeout 15 phút/loop.


### Step 1: Tạo init file

```json
{
  "project": "deutschfuns-lms",
  "tasks": [
    {"id": 1, "status": "pending", "file": "01-setup-module.md"},
    {"id": 2, "status": "pending", "file": "02-create-schema.md"},
    {"id": 3, "status": "pending", "file": "03-implement-crud.md"}
  ],
  "completed": []
}
```


### Step 2: Chạy non-block

```bash
cd /home/fong/Projects/de/wp

.claude/skills/autoclaude/scripts/autoclaude-nonblock.sh \
  "/home/fong/Projects/de/public/.temp/init-my-project.json" \
  30 \
  --cheap \
  --max-time 900
```


### Step 3: Monitor

```bash
# List sessions
.claude/skills/autoclaude/scripts/list-sessions.sh

# Tail debug log
tail -f .claude/skills/autoclaude/scripts/debug.log

# Kill if needed
.claude/skills/autoclaude/scripts/kill-stop-autoclaude.sh SESSION_ID
```


### Output

- Telegram notifications BEFORE-DURING-AFTER mỗi loop
- Prompt files lưu tại `.fong/claude-code-automation/prompts/`
- Debug log tại `.claude/skills/autoclaude/scripts/debug.log`
