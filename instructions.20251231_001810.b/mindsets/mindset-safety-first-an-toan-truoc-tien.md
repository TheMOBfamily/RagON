# Safety First

> Safety > Speed. Reversibility > Cleverness.

## Core Mantras

1. Backup before edit. → `{backup}`
2. Strangler fig: gradual migration, zero downtime.
3. Backward compatible: never break existing users.
4. Zero trust tools: verify everything.
5. Branch first, merge after done. → `{agile}`
6. Reuse proven solutions. → `{giants}`

## Strangler Fig Pattern

```
Legacy ← Wrapper → Gradual migration → Legacy dies naturally
```

Never rewrite from scratch. Wrap old. Add new around.
Evolution > Revolution.

## Backward Compatibility

- SemVer: MAJOR.MINOR.PATCH
- Deprecation warnings first. Grace period. Then remove.
- Feature flags: toggle new code, instant rollback.
- Default unchanged. New = opt-in.

## Zero Trust Tools

- MCP down → CLI fallback exists. Find it.
- Git + 7zip: double backup.
- One backup = zero backup.

## Git Flow

→ See `{agile}` for details.
Key: Never commit to main. Feature branch = sandbox.

## Checklist (9 items)

- [ ] Backup created?
- [ ] Branch forked?
- [ ] Backward compatible?
- [ ] Tests pass?
- [ ] Peer reviewed?
- [ ] Rollback plan ready?
- [ ] Feature flag if risky?
- [ ] Docs updated?
- [ ] Escape hatch exists?

**One-liner**: Safety first. Backup twice. Branch always. Trust but verify.

**Alias:** `{safety}`, `{an toàn}`, `{strangler fig}`, `{backward compatible}`
