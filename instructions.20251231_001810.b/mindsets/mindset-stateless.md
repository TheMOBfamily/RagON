# Stateless AI Execution

> Each session = isolated universe. All context lives in files.

## 3 Ngôn ngữ Viết Stateless Prompt (MANDATORY)

```
1. APHORISTIC     → Ngữ nghĩa. 1 dòng = 1 ý.
2. FORMAL SPEC    → Logic. PRE/POST/INVARIANT.
3. PSEUDOCODE     → Algorithm (nếu cần).
```

## Mantras

1. Fresh AI can execute. No questions asked.
2. All info in-file. Nothing implicit.
3. Paths absolute. Tools explicit.
4. No prior conversation assumed.

## Stateless Prompt Components

| Component | Required |
|-----------|----------|
| **OKR** | Objective + Key Results |
| **Tools** | MCP + Fallback CLI |
| **Credentials** | API keys or .env path |
| **Resources** | Absolute paths |
| **Verification** | Acceptance criteria |

## Cold Start Test

> "If fresh AI CANNOT execute → file lacks info."

- [ ] New AI can run without questions?
- [ ] All paths absolute?
- [ ] Dependencies explicit?
- [ ] Verification clear?

## Properties

| Property | Meaning |
|----------|---------|
| Context-Independent | No prior history needed |
| Zero-Assumption | No implicit knowledge |
| Self-Contained | All tools included |
| Verifiable | Testable, reproducible |

## Checklist

- [ ] OKR defined?
- [ ] Cold start passes?
- [ ] All explicit, no implicit?

**One-liner**: Fresh AI reads prompt. Executes immediately. No questions.

**Alias:** `{stateless}` `{memoryless}`
