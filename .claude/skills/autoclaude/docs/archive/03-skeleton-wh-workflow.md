---
title: "Skeleton-WH: Workflow và Init File Template v3.0"
parent: 00-skeleton-wh-index.md
version: "3.1.0"
updated: "2025-12-06"
---

## Pattern Comparison

| Aspect | Skeleton-WH | Linear Loop Prompt (LLP) |
|--------|-------------|--------------------------|
| Use case | Complex analysis | Sequential automation |
| Diary | Single diary | Per-prompt diary |
| Done marking | Status field | File rename (done-*) |

→ For LLP workflow, see `12-pattern-linear-loop-prompt.md`

---

## Workflow AI Agent (v3.0)

```
┌─────────────────────────────────────────────────────────────┐
│                    AI SESSION START                         │
├─────────────────────────────────────────────────────────────┤
│ 1. Đọc init-autoclaude.json → Hiểu OKR + Checklists        │
│ 2. Parse diary_files[] → Lấy diary mới nhất                │
│ 3. Đọc diary-{loop}-{timestamp}.json → Reconstruct context │
│    - loops.completed → Skip completed loops                 │
│    - artifacts[] → Use existing artifacts                   │
│    - execution.steps_pending[] → Focus on pending           │
│ 4. Đọc instruction files → How-Do, How-Order               │
│ 5. Execute current_step                                     │
│ 6. Update diary-{loop}-{timestamp}.json (atomic write)     │
│ 7. Verify + Cross-check (checklist_verification[])         │
│ 8. Mark step completed hoặc log error                       │
│ 9. Repeat 4-8 until all done                               │
│10. Update init-autoclaude.json (loops.completed++)         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI SESSION END ("chết")                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI SESSION RESTART ("hồi sinh")         │
│ → Đọc init-autoclaude.json → continue_instructions        │
│ → Parse diary_files[] → Tiếp tục từ pending               │
└─────────────────────────────────────────────────────────────┘
```

---

## Mẫu Init File (v3.0)

```markdown
---
created: 2025-12-06 12:00:00
task: [Mô tả task ngắn gọn]
okr: [OKR 1 dòng]
init: ./prompt-{task-name}/init-autoclaude.json
---

## OKR

[Objective và Key Results rõ ràng]

## Instructions

Đọc các file trong folder `./prompt-{task-name}/`:
1. `init-autoclaude.json` - SSoT: State + Checklists
2. `diary-{loop}-{timestamp}.json` - Loop execution logs
3. `01-skeleton-wh.md` - Framework câu hỏi
4. `02-...` - Hướng dẫn chi tiết

## Quy tắc

1. **PHẢI** đọc init-autoclaude.json TRƯỚC khi làm bất cứ điều gì
2. **PHẢI** check checklist_kill_items[] - abort nếu fail
3. **PHẢI** update diary-{loop}-{timestamp}.json SAU mỗi step
4. **PHẢI** verify theo checklist_verification[] trước khi mark completed
5. **KHÔNG** làm lại loop đã completed (idempotent)
```

---

## Integration với RCIFENI (v3.0)

| RCIFENI | Skeleton-WH v3.0 |
|---------|------------------|
| **R**ole | Định nghĩa trong 00-*-init.md |
| **C**ontext | Đọc từ init-autoclaude.json (loops, diary_files) |
| **I**nstructions | Từ folder instruction files |
| **F**ormat | Output theo okr.key_results |
| **E**xample | Concrete example trong document |
| **N**otes | Error handling, checklists |
| **I**nput | diary.execution.steps_pending[] |
