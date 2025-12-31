# Giants' Shoulders: Reuse Over Rebuild

> "Standing on the shoulders of giants." — Newton, 1675

## Core Principle

Search first. Build last.
Someone solved this. Find them.
DRY: Don't Repeat Yourself. Don't Repeat History.

## Decision: Reuse → Buy → Build

| Priority | When | Action |
|----------|------|--------|
| 1. Reuse | OSS exists, ≥80% fit | Use it. Adapt 20%. |
| 2. Buy | Commercial better | Evaluate lock-in first. |
| 3. Build | Core business, unique | Build minimal. |

**Default**: Reuse. Build = last resort.

## Before Coding: DSS Checklist

- [ ] Search GitHub/npm/PyPI?
- [ ] Query RAG for patterns?
- [ ] Query Perplexity for latest libs?
- [ ] Context7 for docs?
- [ ] Compare ≥3 options?

## Library Evaluation (7/10 = proceed)

1. Activity (recent commits?)
2. Community (stars, contributors?)
3. Documentation (clear, examples?)
4. Tests (CI/CD, coverage?)
5. Security (CVE history?)
6. License (compatible?)
7. Fit (≥80% problem solved?)

## Integration: Adapter Pattern

```
Library → Adapter interface → Your code
```

Wrap external. Never call directly.
Adapter = single point of change.

## Escape Hatch (MANDATORY)

Every dependency needs:
1. Rollback plan
2. Fork option
3. Substitution test

**No escape hatch = No adoption.**

## Anti-Patterns

- ❌ "I can write better" → Prove with evidence
- ❌ "Too simple to search" → Search anyway
- ❌ NIH syndrome → Ego blocks progress
- ❌ Copy without understanding → Cargo cult

**One-liner**: Search 10 min. Save 10 hours. Best code = unwritten code.

**Alias:** `{giants}`, `{reuse}`, `{xài lại}`, `{steal}`, `{copy}`, `{đứng trên vai người khổng lồ}`
