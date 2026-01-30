---
title: "Skeleton-WH: Error Handling, Rollback và Atomic Write v3.0"
parent: 00-skeleton-wh-index.md
version: "3.1.0"
updated: "2025-12-06"
---

## Note

Error handling này áp dụng cho cả Skeleton-WH và LLP pattern.
→ LLP Error Escalation: see `12-pattern-linear-loop-prompt.md` ## Error Escalation

---

## Error Handling (v3.0)

### Khi step FAIL:

```
1. Log error vào diary-{loop}-{timestamp}.json errors[]
2. KHÔNG increment execution.steps_completed
3. Retry với max_retry = 3
4. Nếu fail 3 lần → status = "failed" → DỪNG
5. Update init-autoclaude.json errors[] với summary
```

### Error Schema (trong diary-{loop}-{timestamp}.json):

```json
{
  "errors": [
    {
      "step": 2,
      "error_type": "validation|timeout|dependency",
      "message": "...",
      "retry_count": 1,
      "resolved": false
    }
  ]
}
```

### Flow:

```
Execute → Success? YES → next step | NO → retry < 3? YES → retry | NO → STOP
```

---

## Rollback Procedure (v3.0)

```bash
# 1. Backup init-autoclaude.json
cp init-autoclaude.json init-autoclaude.json.backup.$(date +%s)

# 2. Rollback loops.completed về loop N
jq '.loops.completed = N | .loops.status = "in_progress"' init-autoclaude.json > tmp && mv tmp init-autoclaude.json

# 3. Remove diary files sau loop N
# diary_files[] chỉ giữ các file từ loop 1 → N
jq '.diary_files = [.diary_files[] | select(test("diary-00[1-N]"))]' init-autoclaude.json > tmp && mv tmp init-autoclaude.json

# 4. Remove artifacts sau loop N
jq '.artifacts = [.artifacts[] | select(.loop <= N)]' init-autoclaude.json > tmp && mv tmp init-autoclaude.json
```

### Triggers:

| Trigger | Action |
|---------|--------|
| checklist_verification fail | Rollback 1 loop |
| Error 3x consecutive | Rollback + human review |
| Corrupt artifact | Delete + rollback to creator loop |

---

## Atomic Write (v3.0)

### Pattern: Write-Rename (POSIX safe)

```bash
# ❌ KHÔNG: echo "$json" > init-autoclaude.json  (có thể corrupt)
# ✅ ĐÚNG:
echo "$json" > init-autoclaude.json.tmp && mv init-autoclaude.json.tmp init-autoclaude.json
```

### Python pseudo-code:

```python
def update_init(path, updates):
    data = json.load(open(path))
    data.update(updates)
    data['last_updated'] = datetime.now().isoformat()
    with open(f"{path}.tmp", 'w') as f:
        json.dump(data, f, indent=2)
    os.rename(f"{path}.tmp", path)  # Atomic on POSIX
```

### Validate:

```bash
# Validate init-autoclaude.json
jq '.' init-autoclaude.json > /dev/null && echo "✅ Valid" || echo "❌ Corrupt"

# Validate diary files
for f in diary-*.json; do
  jq '.' "$f" > /dev/null && echo "✅ $f Valid" || echo "❌ $f Corrupt"
done
```
