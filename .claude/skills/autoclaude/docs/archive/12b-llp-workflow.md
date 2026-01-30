---
title: "LLP Workflow & Diary Schema"
version: "1.0.0"
updated: "2025-12-07"
parent: 12-pattern-linear-loop-prompt.md
---

# LLP Workflow & Diary

---

## File Structure

```
stateless-prompts/
├── 00-init-{module}.md           # Init với pattern rules
├── prompt-01-setup.md            # Loop 1
├── prompt-02-implement.md        # Loop 2
├── done-prompt-01-setup.md       # Đã xong
├── diary-prompt-01-20251207.json # Diary Loop 1
└── diary-template.json           # Template
```

---

## AI Automation Workflow

```
┌─────────────────────────────────────────┐
│ 1. IDENTIFY: Find prompt-*.md not done- │
│ 2. READ: Load prompt + prev diary       │
│ 3. BACKUP: Git commit trước             │
│ 4. EXECUTE: Run steps                   │
│ 5. DIARY: Update on-the-fly             │
│ 6. VERIFY: Cross-check results          │
│ IF PASS: Mark done → Next loop          │
│ IF FAIL: Debug → Retry (max 5)          │
└─────────────────────────────────────────┘
```

---

## Diary Schema (Key Fields)

```json
{
  "prompt_id": "prompt-05", "loop": 5, "status": "completed",
  "pre_work": {"backup": true, "commit": "abc123"},
  "execution": {"attempts": 1, "steps": ["step1", "step2"]},
  "artifacts": {"created": [], "modified": []},
  "files_read": {"12a-llp-core.md": 2},
  "cross_check": {"double": "PASSED", "cross": "PASSED"}
}
```

---

## 9-Item Checklist

### Kill (3)
- [ ] Prompt trước đã done?
- [ ] Dependencies rõ ràng?
- [ ] Scope độc lập?

### Execution (3)
- [ ] Context đầy đủ?
- [ ] Acceptance gates rõ?
- [ ] Diary fields xác định?

### Verification (3)
- [ ] Self-contained?
- [ ] Naming convention đúng?
- [ ] Cross-check defined?

---

## Commands Cheat Sheet

```bash
# Find current
ls *.md | grep "^prompt-" | grep -v "^done-" | head -1

# Count progress
echo "Done: $(ls done-*.md | wc -l) / Total: $(ls prompt-*.md done-*.md | wc -l)"

# Mark done
mv prompt-XX.md done-prompt-XX.md
```

---

→ Core patterns: `12a-llp-core.md`
→ Debug & Checkpoint: `12c-llp-debug-checkpoint.md`
