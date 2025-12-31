# Memetic Lesson Learned

> Knowledge = DNA. Retrieve. Reuse. Evolve. Store. Prune.

## Core Principle

Answer exists. Don't guess. Search first.

## CRUD by Context

| Phase | Op | Trigger |
|-------|----|---------|
| START | R | New task → Search .memory/ → DSS |
| DURING | R | Stuck → Search before asking |
| END | C/U | Solved → Record lesson |
| END | D | Outdated/wrong → Remove |

## Search Priority

```
.memory/ → Obsidian → NewRAG → Perplexity → Copilot
```

## Storage

| Scope | Location |
|-------|----------|
| Project | `.fong/.memory/` |
| Cross-project | Obsidian vault |
| Working | `.claude/context.json` |

## Lesson Format (WHEN/THEN/FIX)

```
WHEN: [Trigger situation]
THEN: [Consequence if not fixed]
FIX:  [Specific solution]
```

## Context.json Flow

```
BEFORE → READ context.json → understand state
DURING → UPDATE context.json → track progress
AFTER → WRITE .memory/ → persist lesson
```

## Anti-patterns

- ❌ Guess before search
- ❌ Ask when answer exists
- ❌ Solve but don't record
- ❌ Keep outdated knowledge
- ❌ Write WHAT without WHY

## Mantras

1. Search BEFORE. Record AFTER. Prune WHEN stale.
2. Local first. DSS always. Never guess alone.
3. 3+ sources agree → publish.

**One-liner**: Search first. Record after. Prune when stale.

**Alias:** `{memetic}`, `{lesson learned}`
