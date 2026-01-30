# NoSkip Patterns Reference

## Citation Patterns

### Document Citation

```markdown
[filename.md.L##]        # Single line
[filename.md.L##-##]     # Line range
[filename.json.section]  # JSON section
```

### Evidence Citation

```markdown
> Tool: {ToolName}
> Command: {command}
> Output: {output summary}
> Citation: [doc.L##]
```

## Execution Patterns

### Step Execution Template

```markdown
### Step N: {Step Name}

**RE-READ**: [document.md.L##-##]
> "{quoted text from document}"

**DO**:
> Tool: {ToolName}
> Command/Action: {what was done}
> Output: {tool output}

**MARK**: [x] {Step Name} [document.md.L##-##]
```

### Checklist Template

```markdown
## Checklist từ {document}

1. [ ] Step 1 description
2. [ ] Step 2 description
...
N. [ ] Step N description
```

### Final Review Template

```markdown
## Final Checklist

1. [x] Step 1 [doc.L##]
2. [x] Step 2 [doc.L##]
...
N. [x] Step N [doc.L##]

## Red Team Attack

H₀: "I missed something"

- [ ] Verification 1? ✅/❌
- [ ] Verification 2? ✅/❌
...

**Conclusion**: X/Y steps executed. Evidence shown. Red Team {passed/failed}.
```

## Anti-Pattern Detection

### Wrong Patterns (FORBIDDEN)

```markdown
❌ "Step 1 done" (no citation)
❌ "I completed the setup" (no evidence)
❌ "Steps 1-5 executed" (batch, no individual proof)
❌ "This is obvious so I skipped" (assumption)
```

### Correct Patterns (REQUIRED)

```markdown
✅ [x] Step 1 [doc.L5-8] → Tool output: success
✅ Each step has RE-READ section
✅ Each step has DO section với tool output
✅ Each step has MARK section với citation
```

## Long Document Handling

When document >200 LOC:

```bash
# Check size
wc -l document.md

# Sliding window read
sed -n '1,200p' document.md    # Batch 1
sed -n '181,380p' document.md  # Batch 2 (overlap)
...
```

Reference: `instructions-read-long-file.md`

## DSS Integration Pattern

When document unclear:

```markdown
### Step N: {Unclear Step}

**RE-READ**: [document.md.L##]
> "{unclear text}"

**UNCLEAR**: Need clarification on "{specific question}"

**DSS QUERY**:
> Tool: mcp__dkm-knowledgebase__queryNewRAG
> Query: ["relevant keywords"]
> Result: {summary}

**COMBINED EVIDENCE**:
> Document says: "{doc text}"
> DSS says: "{DSS result}"
> Decision: {based on combined evidence}

**DO**: {execute based on combined evidence}

**MARK**: [x] {Step} [doc.L##] + [DSS-NewRAG]
```

## Mindset Integration

| Phase | Mindset File | Key Rule |
|-------|--------------|----------|
| RECON | `mindset-stateless-memoryless.md` | Reconstruct context |
| READ | `mindset-anti-confirmation-bias-evidence-first.md` | Doc = evidence |
| EXECUTE | `mindset-step-by-step-exact-execution-no-skip.md` | Skip = failure |
| EXECUTE | `custom-mindset-slow-is-better-good.md` | One by one |
| REVIEW | `mindset-proof-by-contradiction-null-hypothesis-adversarial-validation-red-team-exploratory-testing.md` | H₀ = wrong |
| REVIEW | `mindset-double-check-cross-check.md` | Verify twice |
