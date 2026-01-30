# Null Hypothesis Templates

## Core Principle

> H₀ = "This is WRONG". Prove otherwise.

Always start with skepticism. The burden of proof is on the claim.

---

## Template Categories

### 1. Code Claims

| Claim Type | H₀ Template |
|------------|-------------|
| "This code works" | H₀: Code has bugs |
| "This is optimal" | H₀: Better solution exists |
| "This is secure" | H₀: Vulnerability present |
| "This scales" | H₀: Performance degrades at scale |

**Attack approach:**
```
H₀: Code has bug at line {N}
Test: Run with edge cases
Evidence: {test output}
Reject H₀ if: All tests pass with coverage ≥80%
```

### 2. Statistical Claims

| Claim Type | H₀ Template |
|------------|-------------|
| "A > B" | H₀: A ≤ B |
| "Method improves X" | H₀: No improvement (μ_diff = 0) |
| "Result significant" | H₀: Result due to chance (p ≥ 0.05) |
| "Trend exists" | H₀: No trend (slope = 0) |

**Attack approach:**
```
H₀: μ₁ = μ₂ (no difference)
Test: t-test or Mann-Whitney
Evidence: p-value, confidence interval
Reject H₀ if: p < α (typically 0.05)
```

### 3. Research Claims

| Claim Type | H₀ Template |
|------------|-------------|
| "Paper conclusion valid" | H₀: Conclusion flawed |
| "Methodology sound" | H₀: Methodology biased |
| "Results reproducible" | H₀: Results cherry-picked |
| "Novel contribution" | H₀: Prior art exists |

**Attack approach:**
```
H₀: Prior work already covers this
Test: Literature search (NewRAG, ArXiv)
Evidence: {similar papers}
Reject H₀ if: No prior work found after exhaustive search
```

### 4. Design Claims

| Claim Type | H₀ Template |
|------------|-------------|
| "Design is correct" | H₀: Design has flaw |
| "Architecture scales" | H₀: Bottleneck exists |
| "Requirements met" | H₀: Requirement missed |
| "User-friendly" | H₀: Usability issue exists |

**Attack approach:**
```
H₀: Requirement {R} not satisfied
Test: Trace requirement to implementation
Evidence: {gap analysis}
Reject H₀ if: All requirements traced and verified
```

### 5. Business Claims

| Claim Type | H₀ Template |
|------------|-------------|
| "ROI positive" | H₀: ROI ≤ 0 |
| "Market exists" | H₀: No product-market fit |
| "Cost estimate accurate" | H₀: Estimate off by ≥2x |
| "Timeline feasible" | H₀: Timeline unrealistic |

**Attack approach:**
```
H₀: Estimate is wrong by factor ≥2
Test: Compare with historical data
Evidence: {actual vs estimated from past projects}
Reject H₀ if: Variance ≤ 20%
```

---

## Formulation Rules

### Rule 1: H₀ must be falsifiable
```
WRONG: H₀: Code might have issues
RIGHT: H₀: Code fails for input X = {edge_case}
```

### Rule 2: H₀ must be specific
```
WRONG: H₀: Something is wrong
RIGHT: H₀: Function returns incorrect value for negative inputs
```

### Rule 3: Define rejection criteria upfront
```
H₀: Performance degrades at scale
Reject if: Response time < 200ms at 10,000 concurrent users
Accept if: Response time ≥ 200ms at 10,000 concurrent users
```

### Rule 4: Use measurable evidence
```
WRONG: H₀ rejected because "it looks right"
RIGHT: H₀ rejected because test suite (87 tests) passed with 94% coverage
```

---

## Evidence Strength Scale

| Strength | Type | Example |
|----------|------|---------|
| 5 (Highest) | Tool output | Test suite pass, profiler result |
| 4 | Primary source | Original paper, official docs |
| 3 | Cross-verified | ≥2 independent sources agree |
| 2 | Single source | One expert opinion |
| 1 (Lowest) | AI assertion | Claude/GPT claim without evidence |

**Rule:** Evidence strength ≥ 3 required to reject H₀

---

## Quick Reference: Hypothesis by Domain

| Domain | Common H₀ | Primary Test |
|--------|-----------|--------------|
| Code | Has bug | Unit tests + edge cases |
| Performance | Too slow | Benchmark + profiler |
| Security | Has vulnerability | Penetration test |
| Data | Incorrect | Validation + sampling |
| Stats | No effect | Significance test |
| Research | Not novel | Literature review |
| Design | Flawed | Requirement tracing |
| Business | Not viable | Financial model |

---

## Anti-Patterns (AVOID)

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague H₀ | Cannot falsify | Be specific |
| No rejection criteria | Subjective | Define metrics upfront |
| Weak evidence | Unreliable | Require strength ≥ 3 |
| Confirmation bias | Cherry-pick | Seek disconfirming evidence |
| Premature rejection | Too eager | Require 2 consecutive pass |
