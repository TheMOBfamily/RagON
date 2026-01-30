# Attack Patterns Reference

## 5W1H Attack Templates

### What (Definition/Output Attack)

| Pattern | Template |
|---------|----------|
| Definition wrong | "Is {term} correctly defined? Check against {source}." |
| Output format wrong | "Does output match expected format? Compare with spec." |
| Logic wrong | "Is logic sound? Trace step-by-step." |
| Scope wrong | "Is scope correct? Check boundaries." |

**Evidence sources:**
- NewRAG: "define {term}"
- Perplexity: "{term} definition 2025"

### Why (Reason/Assumption Attack)

| Pattern | Template |
|---------|----------|
| Wrong reason | "Is the stated reason valid? Find counterexamples." |
| Hidden assumption | "What assumptions are implicit? List and verify each." |
| Circular logic | "Does reasoning depend on conclusion?" |
| Missing justification | "Is there evidence for this claim?" |

**Evidence sources:**
- NewRAG: "why {concept} works"
- Perplexity: "criticism of {concept}"

### Where (Scope/Context Attack)

| Pattern | Template |
|---------|----------|
| Wrong file | "Is this the right file? Check imports/dependencies." |
| Wrong scope | "Does this apply in this context? Check constraints." |
| Wrong line | "Is the error actually here? Trace execution." |
| Wrong environment | "Works in dev, fails in prod? Check environment." |

**Evidence sources:**
- Code analysis: `mcp__ts-py-reader__analyzePythonFile`
- Grep: Search for usage patterns

### When (Timing/Sequence Attack)

| Pattern | Template |
|---------|----------|
| Wrong order | "Must A happen before B? Check dependencies." |
| Race condition | "Can concurrent access cause issues?" |
| Timing assumption | "Is timing guaranteed? Check async/sync." |
| Stale data | "Is data fresh? Check cache/updates." |

**Evidence sources:**
- Trace execution flow
- Check async patterns

### Who (Source/Authority Attack)

| Pattern | Template |
|---------|----------|
| Wrong source | "Is this source authoritative? Check credentials." |
| Outdated source | "Is source still relevant? Check date." |
| Biased source | "Does source have conflict of interest?" |
| Single source | "Is this the only source? Find corroboration." |

**Evidence sources:**
- Cross-check with NewRAG
- Verify with Perplexity

### How (Method/Tool Attack)

| Pattern | Template |
|---------|----------|
| Wrong method | "Is this the right approach? Check alternatives." |
| Wrong tool | "Is this tool appropriate? Check constraints." |
| Missing step | "Are all steps included? Walk through." |
| Over-engineering | "Is this simpler than needed?" |

**Evidence sources:**
- NewRAG: "best practice {method}"
- Perplexity: "alternatives to {method}"

---

## 3-Level Attack Templates

### L1: Counter-Example Attack

```
Claim: {X is always Y}
Attack: Find ONE case where X is NOT Y
Evidence: {specific case}
Result: FAIL if counter-example found
```

**Templates:**
- "Is there a case where {claim} fails?"
- "What happens when {edge case}?"
- "Does this work for {boundary value}?"

### L2: Contradiction Attack (Proof by Contradiction)

```
Claim: {X is true}
Attack:
  1. Assume X is true
  2. Derive logical consequences
  3. Find absurd/contradictory result
  4. Conclude X must be false
Evidence: {chain of reasoning}
Result: FAIL if contradiction found
```

**Templates:**
- "If {claim} is true, then {consequence}. But {consequence} is impossible because..."
- "Assume {claim}. This implies... which contradicts..."

### L3: Null Hypothesis Attack

```
H₀: {Claim is WRONG}
Attack:
  1. State null hypothesis (claim is wrong)
  2. Gather evidence
  3. Try to reject H₀
  4. If cannot reject → claim likely wrong
Evidence: {statistical/logical evidence}
Result: FAIL if cannot reject H₀
```

**Templates:**
- "H₀: {claim} is false. Evidence to reject?"
- "What p-value would we need to accept {claim}?"
- "What sample size needed to verify {claim}?"

---

## Tool Attack Patterns

### NewRAG Attack

```python
# Find contradicting evidence
queryNewRAG(["criticism of {concept}", "{concept} problems", "{concept} failures"])

# Find alternative perspectives
queryNewRAG(["alternatives to {concept}", "better than {concept}"])
```

### Perplexity Attack

```python
queryPerplexity({
    "role": "Devil's advocate researcher",
    "context": "Finding problems with {claim}",
    "instructions": ["Find counterarguments", "List known failures", "Identify edge cases"],
    "output_format": "Bullet points of problems",
    "question": "What are the problems with {claim}?",
    "okr_krs": "O: Find weaknesses. KR: ≥3 valid concerns"
})
```

### Safe Math Attack

```python
# Verify ALL numbers
calculate({
    "operation": "eval",
    "params": {"expression": "{claimed_formula}"}
})

# Check against claimed result
# If different → FAIL
```

---

## Quick Reference: Attack by Target Type

| Target | Primary Attack | Secondary Attack |
|--------|---------------|------------------|
| Code | L1 (edge cases) | How (method) |
| Claim | L2 (contradiction) | Who (source) |
| Data | Safe Math | When (timing) |
| Design | What (definition) | Why (assumption) |
| Process | How (method) | When (sequence) |
| Research | Who (source) | L3 (null hypothesis) |
