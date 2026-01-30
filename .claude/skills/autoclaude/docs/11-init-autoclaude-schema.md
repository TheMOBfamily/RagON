---
title: "Init-Autoclaude Schema"
updated: "2025-12-20"
ssot_ref: "ftask/02-diary-schema.md"
---

# Init-Autoclaude Schema

> SSoT: `ftask/02-diary-schema.md`

## Kill Items (3)
| # | Item | Verify |
|---|------|--------|
| 1 | Working directory? | `pwd` |
| 2 | init-autoclaude.json exists? | `test -f` |
| 3 | No uncommitted changes? | `git status --porcelain` |

## Schema
```json
{
  "metadata": {"task": "...", "model": "default|cheap"},
  "okr": {"objective": "...", "key_results": ["KR1", "KR2"]},
  "5w1h": {"what": "", "why": "", "where": "", "when": "", "who": "", "how": ""},
  "checklist_kill_items": [{"id": 1, "item": "...", "status": "pending|passed"}],
  "checklist_execution": [{"id": 1, "item": "...", "status": "pending|done"}],
  "checklist_verification": [{"id": 1, "item": "...", "status": "pending|done"}],
  "loops": {"total_planned": 10, "completed": 0, "status": "in_progress"},
  "diary_files": ["diary-001-*.json"],
  "artifacts": [],
  "errors": [],
  "last_updated": "ISO8601"
}
```

## Diary Schema
```json
{
  "loop_number": 1,
  "execution": {"steps_completed": [], "steps_pending": []},
  "six_hats": {"white": "", "red": "", "black": "", "yellow": "", "green": "", "blue": ""},
  "outputs": [],
  "errors": [],
  "next_action": ""
}
```

## AI Protocol
```
START: Read init → Check kill items → Get latest diary → Find pending
DURING: Create diary → Update after each step → Increment completed
END: Verify checklists → Update last_updated → Log lessons
```

## File Structure
```
prompts/prompt-{name}/
├── init-autoclaude.json   ← Entry point
├── diary-001-*.json       ← Loop logs
└── XX-task.md             ← Task files
```
