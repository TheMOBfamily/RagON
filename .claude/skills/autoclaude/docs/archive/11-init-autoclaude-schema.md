---
title: "Init-Autoclaude Schema v3.0 - Checklist-Driven Stateless Workflow"
parent: 00-skeleton-wh-index.md
version: "3.2.0"
updated: "2025-12-07"
ssot_reference: "ftask/02-diary-schema.md"
---

## 🔗 SSoT Reference: ftask

Core concepts đã merge vào ftask (SSoT):

| Concept | Reference |
|---------|-----------|
| Diary Schema | `ftask/02-diary-schema.md` |
| 8:2:1 Ratio | `ftask/02-diary-schema.md` § 8:2:1 Cycle Logic |
| 9-Item Checklist | `ftask/00-ftask.md` § Microtask Checklist |
| 5W1H + 6 Hats | `mindsets/mindset-brainstorm-5w1h-6-thinking-hats.md` |

---

## Note

Schema này áp dụng cho **Skeleton-WH pattern**.
→ Cho **LLP pattern** (30+ sequential steps): Xem `12-pattern-linear-loop-prompt.md` + `13-diary-template.json`

---

## Overview

> **"The volume and complexity of what we know has exceeded our individual ability to deliver its benefits correctly."**[1]

File `init-autoclaude.json` là **Single Source of Truth (SSoT)** cho mỗi autoclaude task (Skeleton-WH pattern). Thay thế diary.json cũ.

**Core Changes:**
- `init-autoclaude.json` = Entry point + State management + Checklists
- `diary-{loop}-{timestamp}.json` = Loop-specific execution logs
- AI review các diary files → Continue work until done

---

## ⚠️ KILL ITEMS CHECKLIST (3 items - abort nếu fail)

| # | Item | Verify Command |
|---|------|----------------|
| 1 | Working directory correct? | `pwd` = project root |
| 2 | init-autoclaude.json exists? | `test -f init-autoclaude.json` |
| 3 | No uncommitted changes? | `git status --porcelain` = empty |

---

## JSON Schema v3.0

```json
{
  "$schema": "init-autoclaude-v3.0",
  "version": "3.0",

  "metadata": {
    "created": "ISO8601",
    "task": "Short description",
    "prompt_folder": "./prompts/prompt-{name}/",
    "model": "default|cheap",
    "_model_note": "default=opus (không truyền), cheap=haiku (--cheap)"
  },

  "okr": {
    "objective": "One-line objective",
    "key_results": [
      "KR1: Measurable result",
      "KR2: Measurable result"
    ]
  },

  "5w1h": {
    "what": "Task gì?",
    "why": "Tại sao làm?",
    "where": "Files/folders nào?",
    "when": "Deadline?",
    "who": "AI model nào?",
    "how": "Link to instruction files"
  },

  "checklist_kill_items": [
    {"id": 1, "item": "Verify working directory", "status": "pending|passed|failed"},
    {"id": 2, "item": "Confirm backup exists", "status": "pending|passed|failed"},
    {"id": 3, "item": "Check no uncommitted changes", "status": "pending|passed|failed"}
  ],

  "checklist_execution": [
    {"id": 1, "item": "Read related instruction files", "status": "pending|done"},
    {"id": 2, "item": "Execute primary task", "status": "pending|done"},
    {"id": 3, "item": "Capture stdout/stderr", "status": "pending|done"}
  ],

  "checklist_verification": [
    {"id": 1, "item": "Count output matches expected", "status": "pending|done"},
    {"id": 2, "item": "Validate output format", "status": "pending|done"},
    {"id": 3, "item": "Cross-check with independent tool", "status": "pending|done"}
  ],

  "loops": {
    "total_planned": 10,
    "completed": 0,
    "current": 0,
    "status": "not_started|in_progress|completed|failed"
  },

  "diary_files": [
    "diary-001-20251206-120000.json",
    "diary-002-20251206-121500.json"
  ],

  "artifacts": [],
  "errors": [],

  "continue_instructions": {
    "description": "AI đọc section này để biết cách tiếp tục",
    "steps": [
      "1. Parse diary_files[] → lấy diary mới nhất",
      "2. Đọc diary → check completed[], pending[], errors[]",
      "3. Nếu pending[] không rỗng → tiếp tục từ item đầu tiên",
      "4. Nếu errors[] → fix trước khi tiếp tục",
      "5. Update diary-{loop}-{timestamp}.json sau mỗi step",
      "6. Loop until loops.completed = loops.total_planned"
    ]
  },

  "last_updated": "ISO8601"
}
```

---

## Diary File Schema (diary-{loop}-{timestamp}.json)

```json
{
  "$schema": "diary-v3.0",
  "loop_number": 1,
  "timestamp_start": "ISO8601",
  "timestamp_end": "ISO8601",
  "parent_init": "./init-autoclaude.json",

  "execution": {
    "steps_completed": [],
    "steps_pending": [],
    "current_step": "Step description"
  },

  "six_hats": {
    "white_facts": "Data: X files processed",
    "red_intuition": "Feeling: On track",
    "black_risks": "Risk: Memory overflow",
    "yellow_benefits": "Benefit: 50% faster",
    "green_alternatives": "Alt: Could use parallel",
    "blue_process": "Process: Step 3 of 5"
  },

  "outputs": [],
  "errors": [],
  "lessons_learned": [],
  "next_action": "Description of what next loop should do"
}
```

---

## 📋 JSON File Checklist (9 items - READ-DO)

### Before Creating JSON File

- [ ] Verify JSON syntax valid (use `jq .` to validate)
- [ ] Confirm all required fields present
- [ ] Check ISO8601 timestamps correct format

### During Execution

- [ ] Update status fields atomically (tmp → rename)
- [ ] Log errors immediately to errors[]
- [ ] Increment loop counter after each completion

### After Completion

- [ ] Verify all checklist items marked done
- [ ] Cross-check artifacts[] exist on disk
- [ ] Update last_updated timestamp

---

## AI Reading Protocol

```
SESSION_START:
  1. READ init-autoclaude.json → parse okr, 5w1h, loops
  2. CHECK checklist_kill_items → ALL must be "passed"
  3. PARSE diary_files[] → get latest diary
  4. READ latest diary → understand current state
  5. IDENTIFY pending work from continue_instructions

DURING_EXECUTION:
  6. CREATE diary-{loop}-{timestamp}.json for this loop
  7. UPDATE diary after EACH step
  8. INCREMENT loops.completed when loop done
  9. UPDATE init-autoclaude.json with new diary file

SESSION_END:
  10. VERIFY all checklists completed
  11. UPDATE last_updated
  12. LOG lessons_learned in diary
```

---

## File Structure

```
prompts/prompt-{YYYYMMDD}-{HHMMSS}-{description}/
├── init-autoclaude.json              ← SSoT (entry point)
├── diary-001-20251206-120000.json    ← Loop 1 log
├── diary-002-20251206-121500.json    ← Loop 2 log
├── 01-skeleton-wh.md
├── 02-*.md
└── 05-verification-crosscheck.md
```

---

## References

[1] Gawande, A. (2009). Checklist Manifesto, p. 324.
[2] Marrs, T. (2017). JSON at Work, p. 134.
[3] Bornet, P. (2025). Intelligent Automation Simplified, p. 37.

---

**Related**: [ftask/02-diary-schema.md](../../instructions/ftask/02-diary-schema.md) | [ftask/05-ai-workflow.md](../../instructions/ftask/05-ai-workflow.md)
