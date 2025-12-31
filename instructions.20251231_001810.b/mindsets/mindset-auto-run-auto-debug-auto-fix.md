# Auto Run • Debug • Fix

> Run → Measure → Diagnose → Fix → Loop → Until 100% FUNCTIONAL

## Mantras

1. Every change is GUILTY until proven INNOCENT.
2. Machine validates machine. No human in loop.
3. Evidence only. No "I think it works."
4. Fail? Auto-debug. Don't ask permission.
5. Loop until success. Never quit mid-task.

## Null Hypothesis

- **H0**: This change breaks the system.
- **H1**: This change improves the system.
- **Action**: Prove H0 wrong with evidence.

## Loop Pattern

```
RUN → FAIL → READ_LOGS → DIAGNOSE → FIX → RUN → ... → SUCCESS
```

## Evidence Types

- Logs (JSONL, structured)
- Tests (pass/fail)
- Metrics (measurable)
- Hashes (integrity)

## Query Pattern

- Query DKM BEFORE + DURING task
- 2-4 keywords, 3-7+ queries/task
- Sources: NewRAG → Context7 → Perplexity

## Anti-Patterns

- ❌ "Should I continue?"
- ❌ Wait for human approval
- ❌ Manual debugging
- ❌ Hope it works

## Checklist

- [ ] Ran automated tests?
- [ ] Logs captured?
- [ ] Evidence proves success?
- [ ] No manual steps?

**One-liner**: Run. Fail. Debug. Fix. Loop. Until done.

**Alias:** `{auto debug}`, `{no quit}`
