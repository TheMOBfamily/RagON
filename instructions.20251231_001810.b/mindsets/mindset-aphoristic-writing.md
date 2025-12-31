# Aphoristic Writing

> AI-oriented docs only. NOT for human-facing docs.

## Definition

Aphoristic = Khẩu huyết. 1 line = 1 idea.

## 5 Characteristics

1. Single idea per line.
2. Imperative tone.
3. Minimal words. Maximal clarity.
4. Self-contained. No external context.
5. Actionable. Guide behavior.

## Target Metrics

- <100 LOC per file.
- 60-70% reduction from verbose.
- Read once, remember forever.

## Language Rule

**Default: Precise English.** Vietnamese only when explicitly specified.

Why English:
- Terminology/jargon = precise, universal.
- Technical docs benefit from English clarity.
- Vietnamese = when context requires (local audience, explicit request).

## Style

```
❌ "It is recommended that you should always..."
✅ "Always do X."

❌ "In order to ensure proper functionality..."
✅ "X ensures Y."
```

## When to Use

- `.fong/instructions/*.md`
- `CLAUDE.md` files
- AI prompts, init configs
- Memory files (`.memory/`)

## When NOT to Use

- User-facing docs
- README for humans
- API docs, tutorials

## Red-Team Rewrite

1. Backup original
2. Rewrite aphoristic
3. Red-team 3 rounds
4. Pass: 2 consecutive with no critical gaps
5. ≥95% content preservation

**One-liner**: 1 line = 1 idea. Imperative. Minimal. Actionable.

**Alias:** `{aphoristic}`, `{khẩu huyết}`, `{context engineering}`, `{context engineer}`
