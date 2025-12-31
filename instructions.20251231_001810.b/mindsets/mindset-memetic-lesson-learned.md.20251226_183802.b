# Memetic Lesson Learned

> Knowledge DNA: Store → Retrieve → Reuse → Evolve

## Mantras

1. Search BEFORE task. Record AFTER.
2. Failed → Fixed → RECORD the fix.
3. NASA lost Apollo knowledge. Don't repeat.
4. Memory = organizational survival.
5. context.json = AI working memory. CRUD on-the-fly.

---

## Context.json = AI Working Memory

### Concept
- **Working memory** (short-term): `.claude/context.json`
- **Long-term memory**: `.fong/.memory/*.md`
- AI has no persistent memory → MUST write to survive context loss.

### CRUD On-the-fly
```
BEFORE task → READ context.json → Understand state
DURING task → UPDATE context.json → Track progress
AFTER task → WRITE .memory/ → Persist lesson
```

### Context.json Structure
```json
{
  "what": {"current": "...", "next": "...", "completed": []},
  "where": {"workspace": "...", "files": {"edited": [], "backups": []}},
  "who": {"branch": "..."},
  "when": {"started": "...", "updated": "..."},
  "how": {"method": "...", "result": "..."}
}
```

### Why On-the-fly?
1. AI context window = limited. Summarization = loss.
2. Session interrupt = context loss. Written = survives.
3. Multiple sessions = fragmented. context.json = continuity.
4. "Đang làm gì" → context.json. "Đã học gì" → .memory/.

### Pattern
```
1. Read context.json → Reconstruct state
2. Update "what.current" → Mark task
3. Work → Update "where.files"
4. Complete → Move to "what.completed"
5. Write .memory/ → Persist lesson
```

---

## Search Triggers

| Trigger | Search Where |
|---------|--------------|
| New task | `.fong/.memory/` |
| Error | `.memory/` → project |
| Uncertain | `.fong/` → DKM |

## Record Triggers

| Scenario | Record? |
|----------|---------|
| Failed → fixed | ✅ YES |
| Searched → not found → figured out | ✅ YES |
| Trivial success | ❌ NO |

## Knowledge Sources (CRUD)

| Source | Purpose | When |
|--------|---------|------|
| `.fong/.memory/` | Long-term lessons | Search BEFORE, Write AFTER |
| `.claude/context.json` | AI working memory | CRUD on-the-fly |
| `{workspace}` | Task-specific notes | If defined in fongtools.json AND relevant |
| `.fong/instructions/` | Guides, best practices | Reference |
| DKM | External knowledge | Query when uncertain |

> **{workspace} Rule**: Nếu `fongtools.json` có định nghĩa `{workspace}` VÀ task hiện tại liên quan → Ghi chép song song vào workspace.

## Search Scope

```
{workspace} (if relevant) → .fong/.memory/ → .fong/instructions/ → project → DKM
```

## Checklist

**BEFORE task:**
- [ ] Searched `.memory/`?
- [ ] Queried DKM?

**AFTER task:**
- [ ] Recorded lesson learned?
- [ ] Aligned to existing file (SSoT)?

**One-liner**: Search first. Record after. Never forget twice.

**Alias:** `{memetic}`, `{lesson learned}`
