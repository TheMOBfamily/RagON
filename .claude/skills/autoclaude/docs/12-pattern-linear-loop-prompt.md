---
title: "Linear Loop Prompt (LLP)"
version: "5.0.0"
updated: "2025-12-20"
ssot_ref: "ftask/04-micro-task-template.md"
---

# Linear Loop Prompt (LLP)

> 1 Prompt = 1 Loop. Stateless. Self-contained.

## Clone Rule
```bash
cp ftask/TEMPLATE-SKELETON.md prompts/XX-task.md
# Fill placeholders. NEVER write from scratch.
```

## Entry Point
AI finds `init*.json` → Read config → Find undone task → Execute

## Done Marking
```bash
mv prompt-XX.md done-prompt-XX.md
```

## Workflow
```
1. Find: ls *.md | grep "^prompt-" | grep -v "^done-"
2. Read prompt + prev diary
3. Execute steps
4. Update diary on-the-fly
5. Cross-check
6. Mark done → Next loop
```

## Diary
```
diary-{prompt-id}-{timestamp}.json
```

## DRY Exception
Prompts: Copy OK (cold start). Redundancy > Missing.

## Checkpoint
Loop 5, 10, 15... → `git commit -m "CHECKPOINT: Loop N"`

## Error Escalation
```
Attempt 1-2: Fix → Retry
Attempt 3-4: Rollback → Simplify
Attempt 5: STOP → Document → Notify
```

## Token Budget
- Per loop: 4-6k tokens
- Split if: >3k prompt, >20 files, >5 objectives

## Checklist (9 items)
Kill: Prev done? Dependencies? Scope?
Exec: Context? Gates? Diary fields?
Verify: Self-contained? Naming? Cross-check?

## SSoT
| Concept | Location |
|---------|----------|
| Template | `ftask/TEMPLATE-SKELETON.md` |
| Skeleton | `ftask/05a-stateless-prompt-skeleton.md` |
| Micro-task | `ftask/04-micro-task-template.md` |
