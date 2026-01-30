---
name: noskip
description: This skill should be used when the user asks to "follow instructions exactly", "step by step", "no skip", "tuân thủ tuyệt đối", "làm theo document", uses {noskip}, {exact execution}, {strict follow}, or needs zero-trust-self execution with document as primary source.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: /home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/mindsets/mindset-step-by-step-exact-execution-no-skip.md
---

# NoSkip - Zero-Trust-Self Instruction Execution Skill

Tuân thủ tuyệt đối instructions. AI làm người học. Document là nguồn sơ cấp.

**CRITICAL - MANDATORY FIRST ACTION**:
```
READ /home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/mindsets/mindset-step-by-step-exact-execution-no-skip.md
READ /home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/instructions-do-take-note-stick-the-plan-professor-v2.json
```
Use Read tool with ABSOLUTE PATH. Do NOT skip this step.

## Core Philosophy

```
H₀: "AI sẽ skip steps" — Prove otherwise by DOING each step.
H₀: "AI reasoning is CORRECT" — Disprove by checking DOCUMENT.
```

**One-liner**: Document first. Execute exactly. Trust nothing. Verify each.

## Mental Model

```
╔════════════════════════════════════════════════════════════════╗
║  AI (Claude) = Reasoning tool. WISE but NOT primary source.    ║
║  Document = Primary source. TRUTH until proven otherwise.      ║
║  DSS = Cross-check tool. Use when document insufficient.       ║
╚════════════════════════════════════════════════════════════════╝
```

## 5 Core Principles

| # | Principle | Action |
|---|-----------|--------|
| 1 | **Document First** | READ document BEFORE reasoning. ALWAYS. |
| 2 | **Execute Exactly** | Every step. No skip. No shortcut. No "I know this". |
| 3 | **Zero Trust Self** | AI reasoning ≠ evidence. Document = evidence. |
| 4 | **Show Work** | Prove each step. Visible output. Mark done with proof. |
| 5 | **Continuous Reference** | Check document DURING execution. Not just at start. |

## Anti-Patterns (FORBIDDEN)

| # | Anti-Pattern | Why Wrong | Correct |
|---|--------------|-----------|---------|
| 1 | "I know this" | Overconfidence → Skip | READ document anyway |
| 2 | "This is obvious" | Assumption → Error | VERIFY with document |
| 3 | "Read once, execute all" | Context drift | RE-READ during execution |
| 4 | Mental reasoning | AI hallucination risk | CITE document source |
| 5 | Batch execution | Skip risk increases | One step → Verify → Next |
| 6 | "Done" without proof | No evidence | Show tool output as proof |

## Execution Workflow

```
╔════════════════════════════════════════════════════════════════╗
║  PHASE 0: RECON                                                ║
║  ├─ tree target document/folder                                ║
║  └─ Understand structure BEFORE reading                        ║
╠════════════════════════════════════════════════════════════════╣
║  PHASE 1: READ                                                 ║
║  ├─ Read document thoroughly                                   ║
║  ├─ Extract checklist/steps                                    ║
║  └─ Print checklist to user                                    ║
╠════════════════════════════════════════════════════════════════╣
║  PHASE 2: ULTRATHINK                                           ║
║  ├─ Understand what each step means                            ║
║  ├─ Identify dependencies                                      ║
║  └─ Note unclear parts → Query DSS if needed                   ║
╠════════════════════════════════════════════════════════════════╣
║  PHASE 3: EXECUTE (One-by-One)                                 ║
║  ├─ FOR each step:                                             ║
║  │   ├─ RE-READ relevant section of document                   ║
║  │   ├─ DO step exactly as written                             ║
║  │   ├─ SHOW evidence (tool output)                            ║
║  │   ├─ MARK [x] with citation [doc.L##]                       ║
║  │   └─ VERIFY before next step                                ║
║  └─ REPEAT until all steps done                                ║
╠════════════════════════════════════════════════════════════════╣
║  PHASE 4: REVIEW                                               ║
║  ├─ Cross-check: All steps marked?                             ║
║  ├─ Red Team: Attack own execution                             ║
║  └─ Document lesson learned                                    ║
╚════════════════════════════════════════════════════════════════╝
```

## Checklist (13 items - MANDATORY)

### Kill Items (abort if fail)
- [ ] Document path exists?
- [ ] Document readable?
- [ ] Checklist/steps identified?

### Pre-Execution
- [ ] tree'd target folder?
- [ ] Document read thoroughly?
- [ ] Checklist printed to user?
- [ ] Unclear parts identified?

### Execution
- [ ] Each step: RE-READ relevant section?
- [ ] Each step: Executed EXACTLY as written?
- [ ] Each step: Evidence shown (tool output)?
- [ ] Each step: Marked [x] with citation?

### Post-Execution
- [ ] All steps marked [x]?
- [ ] Red Team attack on own execution?

## Integration with Mindsets

| Phase | Mindsets | Purpose |
|-------|----------|---------|
| RECON | `{stateless}` | No memory. Reconstruct context. |
| READ | `{evidence first}` | Document = evidence. |
| ULTRATHINK | `{brainstorm}`, `{5w1h}` | Understand deeply. |
| EXECUTE | `{no skip}`, `{slow is better}`, `{agile}` | One by one. Verify each. |
| REVIEW | `{red team}`, `{double check}`, `{memetic}` | Attack own work. Document WHY. |

## DSS Integration

When document insufficient:
```
╔════════════════════════════════════════════════════════════════╗
║  Document unclear → Query DSS                                  ║
║  Document conflicts with knowledge → Query DSS to verify       ║
║  Document outdated → Query DSS for latest                      ║
║                                                                ║
║  DSS result + Document = Combined evidence                     ║
║  DSS result alone ≠ Sufficient (need document context)         ║
╚════════════════════════════════════════════════════════════════╝
```

**DSS Priority:**
1. NewRAG → Books, PDFs
2. Perplexity → Latest practices
3. Context7 → Library docs (if coding)
4. Copilot → Cross-check

## Citation Format

**In execution:**
```markdown
- [x] Step 1: Create backup [mindset-always-backup-first.md.L15-18]
- [x] Step 2: Read config [instructions.md.L45-52]
```

**Evidence format:**
```markdown
Step 1 executed:
> Tool output: `cp file file.20260128_131500.b` → Success
> Citation: [mindset-always-backup-first.md.L15]
```

## Pre-Prompt Template

Khi user invoke `/noskip`, AI PHẢI output:

```
`Think BIG, DO small steps`, `step by step`. Best effort to `get things done`. ULTRATHINK activated.
Skill: /noskip | Mode: Zero-Trust-Self Execution
{YYYY-MM-DD HH:MM:SS} (+07)

# 1. Role:
Document Executor + Evidence Validator

# 2. Context:
Document: {document path}
Mode: Zero-trust-self. Document = primary source.
H₀: "AI will skip steps" — Prove otherwise.

# 3. Instructions:
1. RECON: tree target folder
2. READ: Document thoroughly
3. EXTRACT: Checklist/steps → Print to user
4. ULTRATHINK: Understand each step
5. EXECUTE: One by one. RE-READ → DO → SHOW → MARK
6. REVIEW: Red Team attack on own execution

# 4. Output Format:
- Checklist với [x] marks
- Citation [doc.L##] cho mỗi step
- Evidence (tool output) cho mỗi step

# 5. Cautions:
- anti: "I know this" (MUST read document)
- anti: Skip steps (Đọc ≠ Làm)
- anti: Mental reasoning (Document = evidence)
- anti: Batch execution (One step → Verify → Next)
- anti: "Done" without proof (Show tool output)

# 6. OKR:
O: Execute {document} với zero-trust-self
KR1: 100% steps executed exactly as written
KR2: 100% steps have evidence (tool output)
KR3: 100% steps have citation [doc.L##]
```

## AI Workflow (Step-by-Step)

**⚠️ STEP 0 - MANDATORY FIRST:**
```
Read tool → mindset-step-by-step-exact-execution-no-skip.md
Read tool → instructions-do-take-note-stick-the-plan-professor-v2.json
```

1. **Print Pre-Prompt** → Show template above
2. **RECON** → `tree` target folder/document
3. **READ** → Read document thoroughly (use sliding window if >200 LOC)
4. **EXTRACT** → Identify checklist/steps
5. **PRINT** → Show checklist to user
6. **EXECUTE** loop:
   ```
   FOR each step in checklist:
     RE-READ: Relevant section of document
     DO: Execute exactly as written
     SHOW: Tool output as evidence
     MARK: [x] với citation [doc.L##]
     VERIFY: Correct before next step
   ```
7. **REVIEW** → Cross-check all steps marked
8. **RED TEAM** → Attack own execution. H₀ = "I missed something"
9. **DOCUMENT** → Lesson learned if applicable

## Quick Reference

| Question | Answer |
|----------|--------|
| Trust AI reasoning? | NO. Trust DOCUMENT. |
| Skip "obvious" step? | NO. Execute EVERY step. |
| Execute batch? | NO. One step → Verify → Next. |
| "Done" without proof? | NO. Show tool output. |
| Document unclear? | Query DSS. Cross-check. |

## Related Files

- **Mindset**: `mindset-step-by-step-exact-execution-no-skip.md`
- **Professor**: `instructions-do-take-note-stick-the-plan-professor-v2.json`
- **Anti-Bias**: `mindset-anti-confirmation-bias-evidence-first.md`
- **Red Team**: `mindset-proof-by-contradiction-null-hypothesis-adversarial-validation-red-team-exploratory-testing.md`
- **Long File**: `instructions-read-long-file.md`

## Alias

`{noskip}`, `{no skip}`, `{exact execution}`, `{strict follow}`, `{zero trust self}`
