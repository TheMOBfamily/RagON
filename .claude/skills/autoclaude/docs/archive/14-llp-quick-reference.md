---
title: "Linear Loop Prompt (LLP) - Quick Reference"
subtitle: "Cheatsheet cho 1 Prompt = 1 Loop pattern"
version: "1.2.0"
created: "2025-12-06"
updated: "2025-12-06"
parent: 12-pattern-linear-loop-prompt.md
---

## 🔥 DRY Exception

**Prompts**: Chấp nhận copy lại thông tin. Mỗi prompt = self-contained.

| Rule | Reason |
|------|--------|
| Copy context OK | AI không có memory |
| Redundancy > Missing | Cold start mỗi session |

→ Chi tiết: `12-pattern-linear-loop-prompt.md` § DRY Exception

---

## TL;DR

**Pattern**: 1 Prompt = 1 Loop. Tuyến tính. Diary riêng. Rename khi xong.

```
prompt-XX.md → Execute → diary-prompt-XX-*.json → mv → done-prompt-XX.md
```

---

## Pattern Selection

| Pattern | Use Case |
|---------|----------|
| **LLP** | 30+ sequential steps, automation |
| **Skeleton-WH** | Complex analysis, 5W1H + 6 Hats |


---


## Checklist Tạo Prompt (9 Items)

| Phase | Items |
|-------|-------|
| **Kill (Trước)** | 1. Prompt trước done? 2. Dependencies rõ? 3. Scope độc lập? |
| **Execution (Đang)** | 4. Context đủ? 5. Acceptance gates? 6. Diary fields? |
| **Verify (Sau)** | 7. Self-contained? 8. Naming đúng? 9. Diary linkage? |

→ Chi tiết: `12-pattern-linear-loop-prompt.md` § Checklist Tạo Prompt Stateless

---

## Quick Commands

```bash
# Find current task
ls *.md | grep "^prompt-" | grep -v "^done-" | head -1

# Progress
echo "Done: $(ls done-*.md 2>/dev/null | wc -l) / Total"

# Mark done
mv prompt-XX-task.md done-prompt-XX-task.md

# Copy diary template
cp /path/to/docs/13-diary-template.json diary-prompt-XX-$(date +%Y%m%d-%H%M%S).json
```

---

## Execution Flow

```
1. IDENTIFY → 2. READ → 3. BACKUP → 4. EXECUTE → 5. DIARY → 6. VERIFY → 7. MARK DONE → 8. NEXT
```

---

## Checkpoint Protocol

```
Loop 5, 10, 15, 20, 25, 30... = CHECKPOINT
→ git commit + Full diary sync + Verification
```

---

## Debug Protocol

**PHP**:
```php
$debug_id = 'uuid-from-uuidgen';
dbug('LLP - Loop {N} - ' . $debug_id, $data);
```

**JavaScript**:
```javascript
FongDebug.log('LLP - Loop {N}', { step: 'xxx', data: xxx });
```

**Search Logs**:
```bash
rg "LLP" fong-debug-php.jsonl | tail -30
```

---

## Diary Fields (Essential)

| Field | Description |
|-------|-------------|
| `status` | pending → in_progress → completed |
| `started_at` | ISO8601 timestamp |
| `completed_at` | ISO8601 timestamp |
| `artifacts.files_modified` | List of modified files |
| `notes.technical_decisions` | Key decisions made |
| `notes.next_prompt_hints` | Hints for next prompt |

---

## Error Escalation

| Error | Action |
|-------|--------|
| Attempt 1 | Log + Retry |
| Attempt 2 | Log + Debug + Retry |
| Attempt 3 | Log + Query DKM + Retry |
| Attempt 4 | Log + Manual Review + Retry |
| Attempt 5 | ESCALATE → Create escalation file |

---

## Files

| File | Description |
|------|-------------|
| `12-pattern-linear-loop-prompt.md` | Full LLP documentation |
| `13-diary-template.json` | Diary template |
| `14-llp-quick-reference.md` | This file (cheatsheet) |

---

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| Skip backup | ALWAYS backup before each loop |
| Write diary at end | Write diary ON-THE-FLY |
| Create done-* file | RENAME (mv) to done-* |
| Assume AI remembers | Read previous diary for context |

---

## Backup Before Each Loop

```bash
# DB Backup
curl -s 'https://localhost:1811/_fong-graphql/export.php' -k > /tmp/backup-loop-{N}.sql

# Code Backup
timestamp=$(date +%Y%m%d_%H%M%S) && cp file.php "file.php.${timestamp}.b"

# Git Checkpoint (every 5 loops)
git add . && git commit -m "CHECKPOINT: Loop {N}"
```

---

**Reference**: `12-pattern-linear-loop-prompt.md` for complete documentation.
