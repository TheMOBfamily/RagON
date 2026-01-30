---
title: "LLP Debug, Checkpoint & Token Management"
version: "1.0.0"
updated: "2025-12-07"
parent: 12-pattern-linear-loop-prompt.md
---

# LLP Debug & Checkpoint

---

## Debug Protocol

### PHP Debug (dbug)
```php
$debug_id = 'd9af119b-fb45-4d45-ba61-1aa1d5754026'; // uuidgen
dbug('LLP - Loop 5 - ' . $debug_id, $data);
// Search: rg "d9af119b" logs/fong-debug-php.jsonl
```

### JavaScript Debug (FongDebug)
```javascript
FongDebug.log('LLP - Loop 5', {step: 'current', debug_id: 'uuid'});
```

**Rules**: Hard-coded UUID (uuidgen), include loop number, log start + end.

---

## Checkpoint Protocol

**Trigger**: Loop 5, 10, 15, 20...

```bash
# 1. Backup
git add . && git commit -m "CHECKPOINT: Loop {N}"

# 2. Verify
echo "Done: $(ls done-*.md | wc -l) / Total: $(ls *.md | wc -l)"
```

**Diary checkpoint field:**
```json
{"checkpoint": {"is_checkpoint": true, "number": 1, "summary": "5/5 done"}}
```

---

## Error Escalation

```
Attempt 1 → Fail → Analyze → Fix
Attempt 2 → Fail → Different approach
Attempt 3 → Fail → Rollback + Retry
Attempt 4 → Fail → Simplify scope
Attempt 5 → Fail → ESCALATE (stop, document, notify)
```

---

## Token Management (Guidelines)

> **⚠️ LƯU Ý**: Chỉ là gợi ý, điều chỉnh theo thực tế.

| Metric | Guideline |
|--------|-----------|
| Usable | ~160k-170k tokens |
| Per Loop | 4k-6k tokens |
| Loops/Session | ~32-56 loops |

**Split triggers:**
- Prompt > 3k tokens → Split
- Đọc > 20 files → Split
- > 5 objectives → Split

---

## Best Practices

| Rule | Đúng | Sai |
|------|------|-----|
| Diary | On-the-fly | Cuối session |
| Prev output | Đọc diary trước | Assume nhớ |
| Naming | `prompt-01-setup.md` | `prompt-01.md` |

---

## Iterative Reading

```
Read → Work → Read → Work (min 2 reads/file)
```

Track trong diary: `"files_read": {"file.md": 2}`

---

→ Core patterns: `12a-llp-core.md`
→ Workflow: `12b-llp-workflow.md`
→ Full skeleton: `fongtask/05-stateless-prompt-skeleton.md`
