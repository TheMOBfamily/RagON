---
title: "Context.json Usage - Relative Path + TRƯỚC-TRONG-SAU"
version: "2.0.0"
updated: "2025-12-09"
---

## Purpose

`.claude/context.json` dùng để:
1. Track progress của autoclaude tasks
2. Hiểu ngữ cảnh (có thể inject từ bên ngoài)
3. Lưu thinking frameworks (5W1H, Six Hats)

Mỗi dự án có file riêng.


## Critical Rules

| Rule | Description |
|------|-------------|
| **Relative Path Only** | LUÔN dùng `.claude/context.json` (relative) |
| **Never Absolute** | KHÔNG dùng `/home/.../project/.claude/context.json` |
| **Per Project** | Mỗi dự án có file context.json riêng |
| **Create If Missing** | Nếu chưa có → tạo từ skeleton |
| **TRƯỚC-TRONG-SAU** | Đọc/update TRƯỚC-TRONG-SAU mỗi task |


## 🔄 TRƯỚC-TRONG-SAU Pattern (MANDATORY)

### TRƯỚC (Before Task)

```bash
# 1. Đọc context hiện tại
cat .claude/context.json

# 2. Nếu chưa có → tạo từ skeleton
mkdir -p .claude
cp .fong/claude-code-automation/docs/skeleton-context.json .claude/context.json

# 3. Check có context mới inject từ bên ngoài không
```

### TRONG (During Task)

- Update `status: "in_progress"`
- Update `current_task: "[task đang làm]"`
- Update `5w1h` với thinking framework
- Update `six_hats` với De Bono's 6 Thinking Hats
- Check context changes từ bên ngoài (inject)

### SAU (After Task)

- Update `status: "completed"`
- Update `last_completed: "[task vừa xong]"`
- Update `findings: {...}` với kết quả
- Ghi lessons learned


## Setup

```bash
# Tại project root
mkdir -p .claude
cp .fong/claude-code-automation/docs/skeleton-context.json .claude/context.json
```


## AI Instructions

Khi cần update progress:

```bash
# ĐÚNG - Relative path
cat .claude/context.json
# Edit với relative path

# SAI - Absolute path
cat /home/fong/Projects/X/.claude/context.json
```


## Schema

```json
{
  "updated": "2025-12-09T14:00:00+07:00",
  "project": "deutschfuns-lms",
  "last_completed": "prompt-05-task",
  "phase": "2",
  "status": "in_progress",
  "next": "prompt-06-task",
  "findings": {}
}
```


## Prompt Template

Khi tạo prompt cho autoclaude:

```markdown
INSTRUCTIONS:
1. Read init-autoclaude.json in TASK FOLDER
2. Find next pending prompt
3. Execute prompt
4. Update .claude/context.json with progress   ← RELATIVE PATH
5. Commit changes
```

**KHÔNG dùng:**
```markdown
5. Update /home/fong/Projects/X/.claude/context.json   ← SAI
```


## Sync Across Projects

Khi sync autoclaude folder sang dự án mới:

1. Sync `.fong/claude-code-automation/` folder
2. Tạo `.claude/context.json` từ skeleton (nếu chưa có)
3. Prompts dùng relative path → AI edit đúng file của dự án đó


## References

- Skeleton: `docs/skeleton-context.json`
- LLP Pattern: `docs/12-pattern-linear-loop-prompt.md`
