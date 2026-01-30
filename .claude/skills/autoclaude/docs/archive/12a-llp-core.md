---
title: "LLP Core - Pattern Rules & DRY Exception"
version: "1.0.0"
updated: "2025-12-07"
parent: 12-pattern-linear-loop-prompt.md
---

# LLP Core Patterns

> **1 Prompt = 1 Loop. Stateless, tuần tự, self-contained.**

---

## Pattern Rules

### 1. One Prompt = One Loop

```
prompt-01.md → Loop 1 → done-prompt-01.md
prompt-02.md → Loop 2 → done-prompt-02.md
...
```

- Mỗi prompt = đủ info để execute độc lập
- Tuyến tính: Loop N phụ thuộc output của Loop N-1
- Nếu cần output cũ → đọc diary trước

### 2. Diary Per Prompt

```
diary-{prompt-id}-{timestamp}.json
```

Ví dụ: `diary-prompt-01-20251207.json`

### 3. Done Marking

| Status | Pattern |
|--------|---------|
| Chưa xong | `prompt-05-task.md` |
| Đã xong | `done-prompt-05-task.md` |

```bash
# Find current task
ls *.md | grep "^prompt-" | grep -v "^done-" | head -1

# Mark done
mv prompt-05-task.md done-prompt-05-task.md
```

### 4. Scalability

```
100 loops = 100 prompts
1000 loops = 1000 prompts (nếu cần)
```

---

## DRY Exception cho Prompts

| Loại | DRY? | Lý Do |
|------|------|-------|
| CODE | ✅ YES | Full context khi compile |
| PROMPT | ❌ NO | AI cold start, không nhớ |

**Trade-off**: Redundancy > Missing context

**Ví dụ hợp lệ:**
```markdown
# prompt-15.md
## Context (copy từ prompt-14)
- Project: Deutschfuns LMS
- Branch: feat-fong-thi-cuoi-ki-v3

## Tools (copy lại)
- MCP: mcp__de-MCP__php_file_read
```

---

## Entry Point

AI tiếp cận theo thứ tự:
1. Tìm `init*.json` (init-autoclaude.json)
2. Đọc overview + config
3. Tìm task chưa done
4. Execute → Diary → Mark done

---

→ Workflow chi tiết: `12b-llp-workflow.md`
→ Debug & Checkpoint: `12c-llp-debug-checkpoint.md`
→ Skeleton template: `13-stateless-prompt-skeleton.md`
