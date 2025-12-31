# Memetic Lesson Learned

> Knowledge = DNA. Retrieve. Reuse. Evolve. Store. Prune.

---

## Core Principle

Answer exists. Don't guess. Search first.

---

## CRUD by Context

| Phase | Operation | Trigger |
|-------|-----------|---------|
| **START** | **R** (Read) | New task → Search .memory/ → DSS |
| **DURING** | **R** (Read) | Stuck → Search before asking |
| **END** | **C/U** (Create/Update) | Solved → Record lesson |
| **END** | **D** (Delete) | Found outdated/wrong → Remove |

### Read Triggers (R)
- New task → Search .memory/ first.
- Uncertain → Query DSS before guessing.
- Error → Search .memory/ + Perplexity.

### Write Triggers (C/U)
- Failed → Fixed → Record the fix.
- Not found → Figured out → Record.
- Trivial success → Skip.

### Delete Triggers (D)
- Info outdated → Delete or archive.
- Info wrong → Delete immediately.
- Duplicate → Keep SSoT, delete rest.

---

## Search Priority

```
.memory/ → Obsidian → NewRAG → Perplexity → ArXiv → Copilot
```

| Source | When | Style |
|--------|------|-------|
| .memory/ | Project-specific | smart-search keyword |
| Obsidian | Cross-project | fnote-search keywords |
| NewRAG | Best practice | 2-4 words, 3-7 queries |
| Perplexity | Latest info | Structured prompt |
| ArXiv | Academic | cat:cs.* + keywords |
| Copilot | Verify | Second opinion |

---

## Storage

| Scope | Location |
|-------|----------|
| Project-specific | `.fong/.memory/` |
| Cross-project | Obsidian vault |
| Working memory | `.claude/context.json` |

---

## Context.json (AI Working Memory)

```
BEFORE → READ context.json → Understand state
DURING → UPDATE context.json → Track progress
AFTER → WRITE .memory/ → Persist lesson
```

---

## Anti-patterns

- Guess before search.
- Ask user when answer exists.
- Solve but don't record.
- Keep outdated knowledge.

---

## Mantras

1. Search BEFORE. Record AFTER. Prune WHEN stale.
2. Local first. DSS always. Never guess alone.
3. 3+ sources agree → publish. 1 source → verify.
4. NASA lost Apollo knowledge. Don't repeat.

---

**Alias:** `{memetic}`, `{lesson learned}`
