# NoSkip Example: Setup a New Project

Ví dụ thực tế khi dùng `/noskip` để setup project theo document.

## Scenario

User có file `setup-instructions.md` với 10 bước setup. User muốn AI tuân thủ tuyệt đối.

## User Prompt

```
/noskip setup-instructions.md
```

## AI Response

```
`Think BIG, DO small steps`, `step by step`. Best effort to `get things done`. ULTRATHINK activated.
Skill: /noskip | Mode: Zero-Trust-Self Execution
2026-01-28 13:30:00 (+07)

# 1. Role:
Document Executor + Evidence Validator

# 2. Context:
Document: setup-instructions.md
Mode: Zero-trust-self. Document = primary source.
H₀: "AI will skip steps" — Prove otherwise.

---

## PHASE 0: RECON

tree .
└── setup-instructions.md

## PHASE 1: READ

Reading setup-instructions.md...

## PHASE 2: EXTRACT

📋 Checklist từ document (10 steps):

1. [ ] Create project folder
2. [ ] Initialize git
3. [ ] Create .gitignore
4. [ ] Install dependencies
5. [ ] Create config file
6. [ ] Setup database
7. [ ] Create .env
8. [ ] Run migrations
9. [ ] Seed data
10. [ ] Verify setup

## PHASE 3: EXECUTE

### Step 1: Create project folder

**RE-READ**: [setup-instructions.md.L5-8]
> "mkdir my-project && cd my-project"

**DO**:
> Tool: Bash
> Command: mkdir -p my-project
> Output: (success, no error)

**MARK**: [x] Create project folder [setup-instructions.md.L5-8]

---

### Step 2: Initialize git

**RE-READ**: [setup-instructions.md.L10-12]
> "git init"

**DO**:
> Tool: Bash
> Command: git init my-project
> Output: Initialized empty Git repository in /path/my-project/.git/

**MARK**: [x] Initialize git [setup-instructions.md.L10-12]

---

... (tiếp tục cho mỗi step)

---

## PHASE 4: REVIEW

### Checklist Final

1. [x] Create project folder [setup-instructions.md.L5-8]
2. [x] Initialize git [setup-instructions.md.L10-12]
3. [x] Create .gitignore [setup-instructions.md.L14-20]
4. [x] Install dependencies [setup-instructions.md.L22-25]
5. [x] Create config file [setup-instructions.md.L27-35]
6. [x] Setup database [setup-instructions.md.L37-42]
7. [x] Create .env [setup-instructions.md.L44-50]
8. [x] Run migrations [setup-instructions.md.L52-55]
9. [x] Seed data [setup-instructions.md.L57-60]
10. [x] Verify setup [setup-instructions.md.L62-70]

### Red Team Attack

H₀: "I missed something"

- [ ] All folders created? ✅ Verified với `tree`
- [ ] Git initialized? ✅ Verified với `git status`
- [ ] Dependencies installed? ✅ Verified với `npm list`
- [ ] Config valid? ✅ Verified với syntax check
- [ ] Database connected? ✅ Verified với test query

**Conclusion**: 10/10 steps executed. 10/10 evidence shown. Red Team passed.
```

## Key Points

1. **RE-READ** mỗi step trước khi execute
2. **CITE** document line number
3. **SHOW** tool output as evidence
4. **MARK** với [x] và citation
5. **RED TEAM** sau khi hoàn thành
