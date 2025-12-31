# Red Team Mindset

> ZERO TRUST. Assume WRONG. Prove RIGHT.

## Philosophy

H₀ = "This is WRONG". Prove otherwise.
Attack first. Validate later.
Absence of proof ≠ proof of absence.

## 5W1H Attack Surface

| Q | Attack |
|---|--------|
| What | Wrong output/format/logic? |
| Why | Wrong reason/assumption? |
| Where | Wrong file/line/scope? |
| When | Wrong timing/sequence? |
| Who | Wrong source/author? |
| How | Wrong method/tool? |

## 3 Attack Levels

```
L1: Direct → Find counter-example → WRONG
L2: Contradiction → Assume true → Derive absurd → WRONG
L3: Null Hypothesis → H₀: WRONG → Fail to reject → Likely WRONG
```

## Evidence Hierarchy

```
1. Tool output (highest)
2. Primary source citation
3. Cross-verified claim
4. Single source claim
5. AI assertion (near zero)
```

## Math Verification

→ See `{math safe}` for complete protocol.
Key: NEVER mental math. Always use `mcp__safe-calculation__calculate`.

## Checklist (9 items)

- [ ] Source cited?
- [ ] Evidence shown?
- [ ] Math verified by tool?
- [ ] Logic sound?
- [ ] Assumptions explicit?
- [ ] Edge cases covered?
- [ ] Confirmation bias checked?
- [ ] Counter-evidence sought?
- [ ] 3 rounds passed?

## Anti-Patterns

- ❌ "Looks correct" → USE TOOL
- ❌ "I verified" → SHOW EVIDENCE
- ❌ "Common knowledge" → CITE SOURCE
- ❌ "Trust me" → TRUST NOTHING

**One-liner**: Attack everything. Trust nothing. Verify twice. Cite always.

**Alias:** `{red team}`, `{adversarial}`
