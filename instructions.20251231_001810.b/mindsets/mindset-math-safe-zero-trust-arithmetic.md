# Math Safe - Zero Trust Arithmetic

> AI math = unreliable. Always verify with tools.

## Core Principle

Zero trust for self-computed math.
Token prediction ≠ calculation.
"9.11 > 9.9" = famous AI bug.

## 5 Forbidden

1. ❌ Mental arithmetic (even 2+2)
2. ❌ Counting by "looking"
3. ❌ "I think N items"
4. ❌ Sequence without explicit list
5. ❌ Statistics without tool

## 5 Required

1. ✅ `mcp__safe-calculation__calculate` for ALL math
2. ✅ Write task list to context.json
3. ✅ Number each task (1, 2, 3...)
4. ✅ Update status after EACH task
5. ✅ Verify count before "done"

## Tool Priority

```
1. mcp__safe-calculation__calculate (primary)
2. wc -l / wc -w (counts)
3. jq length (JSON arrays)
4. rg -c (pattern counts)
```

## Pattern

```
Before claim: COUNT with tool
After claim: RE-COUNT with different tool
Discrepancy: STOP. Investigate.
```

## Checklist (9 items)

- [ ] Used calculation tool?
- [ ] Counted with wc/jq?
- [ ] Double-checked result?
- [ ] No mental math?
- [ ] No "I think" statements?
- [ ] Tool output quoted?
- [ ] Tasks numbered in context.json?
- [ ] Discrepancies investigated?
- [ ] Final count verified?

**One-liner**: Never trust AI math. Always use tools. Verify twice.

**Alias:** `{math safe}`, `{zero trust}`, `{SCME}`
