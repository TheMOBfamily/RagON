---
name: red-team
description: This skill should be used when the user asks to "attack", "validate", "challenge", "red team", "adversarial", "prove wrong", "null hypothesis", uses {red-team}, {adversarial}, or needs extreme multi-perspective validation before decision.
version: 3.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: .fong/instructions/instructions-DSS-decision-support-system.md
textor_instructions: .fong/instructions/textor-mdlatex/
veta_instructions: .fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json
output_language: Vietnamese
---

# Red Team - Adversarial Validation Skill

Kiem chung CUC DOAN voi H0 = "CAI NAY SAI". Output .md TIENG VIET voi attack matrix + footnote citations. Export PDF qua Textor.


## Output Language: TIENG VIET (MANDATORY)

> **VIET HOA CUC DOAN** - Tat ca output phai bang tieng Viet.

**Ref:** `.fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json`

**Rules:**

- Output file .md/.pdf = TIENG VIET
- Thuat ngu ky thuat = Inline format: "Ten Viet (English term)"
- KHONG tao bang thuat ngu rieng (render xau trong PDF)
- Dung VETA de viet hoa chinh xac

**VETA Execution:**

```
# Co file path
.fong/tools/veta-gemini.sh /path/to/file

# Fallback
.fong/tools/veta-copilot.sh /path/to/file

# Khong co file path
mcp__dkm-knowledgebase__queryCopilot
```


## Input Types: GENERAL (Moi loai deu duoc)

> **KHONG FIX CUNG** - Skill nhan BAT KY loai input nao.

| Input Type | Vi du | Attack Focus |
|------------|-------|--------------|
| **Code** | Python, JS, PHP... | Bugs, security, performance |
| **Paper** | Research claims | Methodology, statistics, citations |
| **Content** | Blog, docs, marketing | Accuracy, bias, sources |
| **Claim** | Business, technical | Evidence, logic, assumptions |
| **Design** | Architecture, UX | Patterns, scalability, usability |
| **Data** | Datasets, reports | Quality, completeness, bias |
| **Process** | Workflows, SOPs | Efficiency, gaps, risks |
| **Decision** | Business, technical | ROI, risks, alternatives |

**Auto-Detection:**

```
IF input contains code syntax → Attack as Code
IF input cites papers/research → Attack as Paper
IF input makes claims → Attack as Claim
IF input describes process → Attack as Process
ELSE → Attack as General Content
```

**CRITICAL - MANDATORY FIRST ACTIONS (Zero Skip)**:

```
READ .fong/instructions/instructions-DSS-decision-support-system.md
READ .fong/instructions/mindsets/mindset-proof-by-contradiction-null-hypothesis-adversarial-validation-red-team-exploratory-testing.md
READ .fong/instructions/mindsets/mindset-brainstorm-5w1h-6-thinking-hats.md
READ .fong/instructions/textor-mdlatex/01-critical-rules.md
READ .fong/instructions/textor-mdlatex/12-footnote-citation.md
READ .fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json
```

Use Read tool with ABSOLUTE PATH. Do NOT skip ANY step.


## Core Concept

H0 = "This is WRONG". Prove otherwise.
Attack first. Validate later.
Absence of proof # proof of absence.


## Protocol: RT7 ONLY (No Exceptions)

> **EXTREME MODE** - 7 rounds. No shortcuts. No quick checks.

| Protocol | Description | Attack Rounds |
|----------|-------------|---------------|
| **{RT7}** | Extreme adversarial validation | **7 rounds MANDATORY** |

**Rules:**

- NO RT3, NO RT5. Only RT7.
- Every attack MUST complete 7 rounds.
- Shortcut = Failure. No exceptions.


## 5W1H Attack Surface (MANDATORY)

| Q | Attack Question |
|---|-----------------|
| **What** | Wrong output/format/logic/definition? |
| **Why** | Wrong reason/assumption/motivation? |
| **Where** | Wrong file/line/scope/context? |
| **When** | Wrong timing/sequence/dependency? |
| **Who** | Wrong source/author/stakeholder? |
| **How** | Wrong method/tool/approach? |


## 6 Thinking Hats Attack Angles (Internal Only)

**Rule**: Hats = think tool. NOT output format. Never list hats in report.

| Hat | Attack Focus |
|-----|--------------|
| White | Data wrong? Evidence missing? |
| Red | Gut feeling says problem? |
| Black | Risks? Failure modes? |
| Yellow | Benefits overstated? |
| Green | Better alternatives exist? |
| Blue | Process flawed? |


## 3 Attack Levels (MANDATORY per round)

```
L1: Direct -> Find counter-example -> WRONG
L2: Contradiction -> Assume true -> Derive absurd -> WRONG
L3: Null Hypothesis -> H0: WRONG -> Fail to reject -> Likely WRONG
```


## Evidence Hierarchy

```
1. Tool output (highest)
2. Primary source citation
3. Cross-verified claim (>=2 sources)
4. Single source claim
5. AI assertion (near zero - NEVER trust)
```


## DSS Tools (MANDATORY - from DSS Skill)

**Ref:** `.fong/instructions/instructions-DSS-decision-support-system.md`

| # | Tool | MCP | Purpose |
|---|------|-----|---------|
| 1 | NewRAG | `mcp__dkm-knowledgebase__queryNewRAG` | Find contradicting evidence |
| 2 | Perplexity | `mcp__dkm-knowledgebase__queryPerplexity` | Latest counterarguments |
| 3 | Copilot | `mcp__dkm-knowledgebase__queryCopilot` | Alternative perspective |
| 4 | Z.AI | `mcp__mcp-zai__chinese-zai` | Cross-check reasoning |
| 5 | Safe Math | `mcp__safe-calculation__calculate` | Verify ALL numbers |

**Rule:** Every claim MUST be attacked with >=1 DSS tool.

**Query Pattern (from DSS):**

- SHORT (2-4 words). SPECIFIC. MULTIPLE.
- 3 queries per tool minimum.
- 5W1H + 6 Hats angles.


## Retry Mechanism (from DSS)

**Rule:** Moi tool PHAI retry toi thieu 3 lan truoc khi chuyen sang fallback.

| Attempt | Wait | Action |
|---------|------|--------|
| 1 | 0s | First try |
| 2 | 3s | Retry after timeout/error |
| 3 | 5s | Final retry |


---


## Critical Rules

1. **H0 = WRONG** - Always start assuming target is wrong
2. **7 rounds MANDATORY** - No RT3, No RT5
3. **NEVER mental math** - Use `mcp__safe-calculation__calculate`
4. **OUTPUT = .md + .pdf** - Footnote citations required
5. **Cite ALL evidence** - Uncited = worthless
6. **5W1H + 6 Hats** - Every round, every angle
7. **DSS Tools** - Use ALL tools per round


## Output Location

**Default folder:** `.fong/docs/red-team-output/{YYYYMMDD-HHMMSS}/`

**File Naming Convention:**

| Pattern | Example |
|---------|---------|
| `RT7-{topic}-attack-{YYYYMMDD-HHMMSS}.md` | `RT7-paper-claims-attack-20260124-190500.md` |
| `RT7-{topic}-attack-{YYYYMMDD-HHMMSS}.pdf` | `RT7-paper-claims-attack-20260124-190500.pdf` |

**Output files trong folder:**

| File | Muc dich |
|------|----------|
| `RT7-{topic}-attack-{datetime}.md` | Full attack matrix voi footnote citations |
| `RT7-{topic}-attack-{datetime}.pdf` | PDF export via Textor |
| `RT7-{topic}-attack-{datetime}_img/` | Diagram images (neu co) |


---


## Footnote Citation Format (MANDATORY)

**Ref:** `.fong/instructions/textor-mdlatex/12-footnote-citation.md`

**In text:**

```markdown
Claim nay co van de[^1]. Evidence cho thay sai[^2].
```

**End of file:**

```markdown
[^1]: Author (Year). Title. Publisher, p.XX.

[^2]: NewRAG: DKM-BookName.pdf.P##.

[^3]: Perplexity (2026-01-24). Query: "keyword".

[^4]: Copilot (2026-01-24). Query: "keyword".
```

**Rule:** Bat buoc dau `^`. `[^1]` KHONG phai `[1]`.


---


## Textor PDF Export (MANDATORY)

**Ref:** `.fong/instructions/textor-mdlatex/*`

**CRITICAL - AI PHAI DOC CAC FILE TEXTOR TRUOC KHI EXPORT:**

```
READ .fong/instructions/textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md
READ .fong/instructions/textor-mdlatex/01-critical-rules.md
READ .fong/instructions/textor-mdlatex/12-footnote-citation.md
```

**Textor Critical Rules:**

1. **NO EMOJI** - XeLaTeX khong render emoji
2. **Max 3 heading levels** - H1 (YAML only), H2, H3. NO H4+
3. **2 newlines** - Giua header va content
4. **Footnote syntax** - `[^1]` voi definition cuoi file

**Export Command:**

```bash
# Dung script Textor tu .fong/tools/ hoac Projects/textor-doc-converter/
textor '{"command":"export-md-to-pdf","data":"RT7-{topic}-tan-cong-{datetime}.md"}'

# Hoac dung alias trong shell
# Xem: .fong/instructions/textor-mdlatex/02-command-reference.md
```

**Output:**

- `{output-file}.pdf` - PDF file
- `{output-file}_img/` - Embedded images (neu co diagrams)


---


## Output File Template (TIENG VIET)

**Filename:** `RT7-{topic}-tan-cong-{YYYYMMDD-HHMMSS}.md`

```markdown
---
title: "Tan Cong Red Team: {Topic}"
subtitle: "RT7 Kiem Chung Doi Khang Cuc Doan"
author: "Red Team Skill cho Thanh-Phong Lam"
date: "{YYYY-MM-DD}"
protocol: "RT7"
rounds_completed: 7
verdict: "DAT|THAT BAI|CAN LUU Y"
version: "1.0.0"
language: "Vietnamese"
---


# Tan Cong Red Team: {Topic}


## Tuyen bo mien tru

Tai lieu nay duoc tao bang phuong phap Red Team voi H0 = "CAI NAY SAI".
Tat ca tan cong la kiem chung doi khang, khong phai chi trich ca nhan.
Muc dich: Tim diem yeu truoc khi trien khai/xuat ban.

**Tao boi:** Red Team Skill cho Thanh-Phong Lam
**Giao thuc:** RT7 (7 vong, 5W1H + 6 Mu, Cong cu DSS)
**Ngay:** {YYYY-MM-DD HH:MM:SS} (+07)


## Tom tat

| Chi so | Gia tri |
|--------|---------|
| Tong tan cong | N |
| Dat | N |
| That bai | N |
| Can luu y | N |
| **Ket luan** | **DAT/THAT BAI/CAN LUU Y** |


## Muc tieu tan cong

> {Tuyen bo/gia thuyet/code bi tan cong}


## Ma tran tan cong


### Vong 1: Tan cong 5W1H

| Cau hoi | Tan cong | Bang chung | Ket qua |
|---------|----------|------------|---------|
| Cai gi (What) | {tan cong} | {bang chung}[^1] | DAT/THAT BAI |
| Tai sao (Why) | {tan cong} | {bang chung}[^2] | DAT/THAT BAI |
| O dau (Where) | {tan cong} | {bang chung} | DAT/THAT BAI |
| Khi nao (When) | {tan cong} | {bang chung} | DAT/THAT BAI |
| Ai (Who) | {tan cong} | {bang chung} | DAT/THAT BAI |
| Lam sao (How) | {tan cong} | {bang chung} | DAT/THAT BAI |


### Vong 2: Tan cong 3 cap do

| Cap | Phuong phap | Tan cong | Bang chung | Ket qua |
|-----|-------------|----------|------------|---------|
| L1 | Phan vi du (Counter-example) | {tan cong} | {bang chung}[^3] | DAT/THAT BAI |
| L2 | Mau thuan (Contradiction) | {tan cong} | {bang chung} | DAT/THAT BAI |
| L3 | Gia thuyet khong (Null Hypothesis) | {tan cong} | {bang chung} | DAT/THAT BAI |


### Vong 3: Xac minh bang cong cu DSS

| Cong cu | Truy van | Phat hien | Ket qua |
|---------|----------|-----------|---------|
| NewRAG | "{truy van}" | {phat hien}[^4] | DAT/THAT BAI |
| Perplexity | "{truy van}" | {phat hien}[^5] | DAT/THAT BAI |
| Copilot | "{truy van}" | {phat hien}[^6] | DAT/THAT BAI |
| Z.AI | "{truy van}" | {phat hien}[^7] | DAT/THAT BAI |
| Safe Math | {bieu thuc} | {ket qua} | DAT/THAT BAI |


### Vong 4-7: Tan cong sau

{Lap lai 5W1H + 3 cap do + DSS cho cac vong con lai}


## Van de can luu y (neu co)

1. **{Van de 1}**: {Mo ta}[^8]
2. **{Van de 2}**: {Mo ta}


## Khuyen nghi

1. {Khuyen nghi 1}
2. {Khuyen nghi 2}


## Ket luan

**{DAT|THAT BAI|CAN LUU Y}**

Ly do: {Tai sao ket luan nhu vay}

---

[^1]: Nguon1 (Nam). Tieu de. Nha xuat ban/URL.

[^2]: NewRAG: DKM-TenSach.pdf.P##.

[^3]: Perplexity (2026-01-24). Truy van: "tu khoa".

[^4]: NewRAG: DKM-TenSach.pdf.P##.

[^5]: Perplexity (2026-01-24). Truy van: "tu khoa".

[^6]: Copilot (2026-01-24). Truy van: "tu khoa".

[^7]: Z.AI (2026-01-24). Truy van: "tu khoa".

[^8]: Safe Math: ket qua tinh toan.
```


---


## Pre-Prompt Template (RCIFENI-O)

Khi user invoke `/red-team`, AI PHAI output response theo format sau:

```
`Think BIG, DO small steps`, `step by step`. Best effort to `get things done`. ULTRATHINK activated.
Skill: /red-team | Protocol: RT7 (7 rounds MANDATORY)
{YYYY-MM-DD HH:MM:SS} (+07)

# 1. Role:
Adversarial Validator + Red Team Attacker + DSS Researcher

# 2. Context:
Target: {user's claim/hypothesis/code}
Protocol: RT7 (7 rounds, NO shortcuts)
Output: .md file with footnote citations -> .pdf via Textor

# 3. Instructions:
1. READ all required files (DSS, mindsets, textor)
2. Assume H0 = "This is WRONG"
3. Execute 7 rounds:
   - Round 1-2: 5W1H + 3-Level Attack
   - Round 3-4: DSS Tool Verification
   - Round 5-7: Deep Attack + Cross-verification
4. Document ALL evidence with footnotes
5. Export .md to .pdf via Textor

# 4. Output Format:
- File: RT7-{topic}-attack-{datetime}.md
- Attack matrix with footnote citations [^N]
- NO emoji, Max H3, 2 newlines spacing
- Export: RT7-{topic}-attack-{datetime}.pdf

# 5. Cautions:
- anti: Trust without evidence
- anti: Mental math (use Safe Math MCP)
- anti: Single perspective (use 5W1H + 6 Hats)
- anti: Missing citations (use footnotes)
- anti: Shortcut (MUST complete 7 rounds)
- anti: Emoji in output (XeLaTeX fail)

# 6. OKR:
O: Attack {target} voi extreme adversarial validation
KR1: Complete 7 attack rounds
KR2: Use ALL DSS tools for verification
KR3: Output .md + .pdf with footnote citations
```


---


## AI Workflow

**STEP 0 - MANDATORY FIRST (Zero Skip):**

```
Read tool -> instructions-DSS-decision-support-system.md
Read tool -> mindset-proof-by-contradiction-null-hypothesis-adversarial-validation-red-team-exploratory-testing.md
Read tool -> mindset-brainstorm-5w1h-6-thinking-hats.md
Read tool -> textor-mdlatex/01-critical-rules.md
Read tool -> textor-mdlatex/12-footnote-citation.md
```

1. **Print Pre-Prompt** -> Show RCIFENI-O template above
2. **Nhan target** -> Confirm RT7 (7 rounds)
3. **Create output folder**: `.fong/docs/red-team-output/{YYYYMMDD-HHMMSS}/`
4. **Execute 7 rounds** (BAT BUOC):

```
FOR round = 1 to 7:
  # 5W1H Attack
  FOR each Q in [What, Why, Where, When, Who, How]:
    Attack with evidence
    Cite with footnote [^N]
    Mark PASS/FAIL

  # 3-Level Attack
  FOR each Level in [L1, L2, L3]:
    Apply attack method
    Document evidence with footnote
    Mark PASS/FAIL

  # DSS Tool Verification
  Query NewRAG for contradicting evidence
  Query Perplexity for counterarguments
  Query Copilot for alternative perspective
  Query Z.AI for cross-check
  Verify numbers with Safe Math
  Cite ALL findings with footnotes

  IF any FAIL:
    Document concern
    Continue to next round

  # NO early exit - MUST complete 7 rounds
```

5. **Create attack report** voi footnote citations
6. **Verify** all footnotes defined at end of file
7. **Read Textor rules** truoc khi export
8. **Export PDF** via Textor

**Output folder structure:**

```
.fong/docs/red-team-output/{YYYYMMDD-HHMMSS}/
|-- RT7-{topic}-attack.md      # Full attack matrix voi footnotes
|-- RT7-{topic}-attack.pdf     # PDF export via Textor
|-- RT7-{topic}-attack_img/    # Diagram images (neu co)
```


---


## Checklist (15 items - MANDATORY)

- [ ] DSS instructions read?
- [ ] Mindset files read?
- [ ] Textor rules read?
- [ ] H0 = "WRONG" assumed?
- [ ] 5W1H attack completed (ALL 6 questions)?
- [ ] 6 Hats considered (internal)?
- [ ] L1 counter-example tried?
- [ ] L2 contradiction tried?
- [ ] L3 null hypothesis tried?
- [ ] ALL DSS tools used (NewRAG, Perplexity, Copilot, Z.AI)?
- [ ] ALL numbers verified with Safe Math?
- [ ] ALL evidence cited with footnotes?
- [ ] 7 rounds completed (NO shortcuts)?
- [ ] Verdict documented with rationale?
- [ ] PDF exported via Textor?


---


## Cross-References

| Context | File |
|---------|------|
| **DSS Instructions** | `.fong/instructions/instructions-DSS-decision-support-system.md` |
| **Red Team Mindset** | `.fong/instructions/mindsets/mindset-proof-by-contradiction-null-hypothesis-adversarial-validation-red-team-exploratory-testing.md` |
| **5W1H + 6 Hats** | `.fong/instructions/mindsets/mindset-brainstorm-5w1h-6-thinking-hats.md` |
| **Step-by-Step** | `.fong/instructions/mindsets/mindset-step-by-step-exact-execution-no-skip.md` |
| **Slow is Better** | `.fong/instructions/mindsets/custom/custom-mindset-slow-is-better-good.md` |
| **DSS Skill** | `.claude/skills/dss/SKILL.md` |
| **Safe Math** | `.fong/instructions/instructions-mcp-safe-calculation-math-engine.md` |
| **Textor Main** | `.fong/instructions/textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md` |
| **Textor Critical Rules** | `.fong/instructions/textor-mdlatex/01-critical-rules.md` |
| **Textor Footnotes** | `.fong/instructions/textor-mdlatex/12-footnote-citation.md` |


---


## Additional Resources


### Reference Files

- **`references/attack-patterns.md`** - 5W1H attack templates
- **`references/hypothesis-templates.md`** - Null hypothesis formulations


### Example Files

- **`examples/red-team-code-review.md`** - Code attack example
- **`examples/red-team-paper-claims.md`** - Paper claims attack example
