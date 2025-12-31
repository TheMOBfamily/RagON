# Always Backup First

> Backup precedes action. Every edit is destructive until proven safe.

## Mantras

1. Backup before edit. Always.
2. Commit before modify.
3. Verify before trust.
4. Read file, not memory.
5. Checkpoint before experiment.

## Zero Trust Memory

- Never say "I remember..."
- Always say "Let me READ..."
- AI memory fails. Disk is truth.
- Git history is authoritative.

## Workflow

```
git status → git add . → git commit "checkpoint" → EDIT → git diff → git commit
```

## Commands

```bash
# Backup single file
cp file "file.$(date +%Y%m%d_%H%M%S).b"

# Checkpoint commit
git add . && git commit -m "checkpoint: before editing <file>"

# Recovery
mcp__ts-tuc-mang-minh__searchFileHistory
```

## Checklist

- [ ] Read file first?
- [ ] Checkpoint committed?
- [ ] Backup created?
- [ ] Changes verified?

**One-liner**: Backup first. Trust nothing. Verify everything.

**Alias:** `{backup}`, `{safety first}`
