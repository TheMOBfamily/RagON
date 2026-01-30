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

<!-- ╔═══════════════════════════════════════════════════════════════════════════╗
     ║  ⛔ CRITICAL: TIẾNG VIỆT CÓ DẦU - ZERO TOLERANCE                          ║
     ║                                                                            ║
     ║  ❌ VIẾT KHÔNG DẤU = VIOLATION = TASK FAILURE                              ║
     ║  ✅ "Tấn công" KHÔNG PHẢI "Tan cong"                                       ║
     ║  ✅ "Kiểm chứng" KHÔNG PHẢI "Kiem chung"                                   ║
     ║  ✅ "Kết luận" KHÔNG PHẢI "Ket luan"                                       ║
     ║                                                                            ║
     ║  AI: ĐỌC BLOCK NÀY TRƯỚC. VIẾT FILE .md PHẢI CÓ DẦU ĐẦY ĐỦ.              ║
     ║  YAML frontmatter + content + footnotes = TẤT CẢ CÓ DẤU.                  ║
     ║  XeLaTeX + Textor hỗ trợ Unicode 100%. KHÔNG CÓ LÝ DO VIẾT KHÔNG DẤU.    ║
     ╚═══════════════════════════════════════════════════════════════════════════╝ -->

# Red Team - Adversarial Validation Skill

Kiểm chứng CỰC ĐOAN với H0 = "CÁI NÀY SAI". Output .md TIẾNG VIỆT CÓ DẤU với attack matrix + footnote citations. Export PDF qua Textor.


## Output Language: TIẾNG VIỆT CÓ DẤU (MANDATORY)

> **VIỆT HÓA CỰC ĐOAN** - Tất cả output phải bằng tiếng Việt CÓ DẤU đầy đủ.

**Ref:** `.fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json`

**Rules:**

- Output file .md/.pdf = TIẾNG VIỆT CÓ DẤU (không được viết không dấu)
- Thuật ngữ kỹ thuật = Inline format: "Tên Việt (English term)"
- KHÔNG tạo bảng thuật ngữ riêng (render xấu trong PDF)
- Dùng VETA để Việt hóa chính xác
- **CRITICAL:** Viết không dấu = VIOLATION. Phải có đầy đủ dấu tiếng Việt.

**VETA Execution:**

```
# Co file path
.fong/tools/veta-gemini.sh /path/to/file

# Fallback
.fong/tools/veta-copilot.sh /path/to/file

# Khong co file path
mcp__dkm-knowledgebase__queryCopilot
```


## Input Types: GENERAL (Mọi loại đều được)

> **KHÔNG FIX CỨNG** - Skill nhận BẤT KỲ loại input nào.

| Input Type | Ví dụ | Attack Focus |
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

**Rule:** Mỗi tool PHẢI retry tối thiểu 3 lần trước khi chuyển sang fallback.

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

| File | Mục đích |
|------|----------|
| `RT7-{topic}-attack-{datetime}.md` | Full attack matrix với footnote citations |
| `RT7-{topic}-attack-{datetime}.pdf` | PDF export via Textor |
| `RT7-{topic}-attack-{datetime}_img/` | Diagram images (nếu có) |


---


## Footnote Citation Format (MANDATORY)

**Ref:** `.fong/instructions/textor-mdlatex/12-footnote-citation.md`

**In text:**

```markdown
Claim này có vấn đề[^1]. Evidence cho thấy sai[^2].
```

**End of file:**

```markdown
[^1]: Author (Year). Title. Publisher, p.XX.

[^2]: NewRAG: DKM-BookName.pdf.P##.

[^3]: Perplexity (2026-01-24). Query: "keyword".

[^4]: Copilot (2026-01-24). Query: "keyword".
```

**Rule:** Bắt buộc dấu `^`. `[^1]` KHÔNG phải `[1]`.


---


## Textor PDF Export (MANDATORY)

**Ref:** `.fong/instructions/textor-mdlatex/*`

**CRITICAL - AI PHẢI ĐỌC CÁC FILE TEXTOR TRƯỚC KHI EXPORT:**

```
READ .fong/instructions/textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md
READ .fong/instructions/textor-mdlatex/01-critical-rules.md
READ .fong/instructions/textor-mdlatex/12-footnote-citation.md
```

**Textor Critical Rules:**

1. **NO EMOJI** - XeLaTeX không render emoji
2. **Max 3 heading levels** - H1 (YAML only), H2, H3. NO H4+
3. **2 newlines** - Giữa header và content
4. **Footnote syntax** - `[^1]` với definition cuối file

**Export Command:**

```bash
# Dùng script Textor từ .fong/tools/ hoặc Projects/textor-doc-converter/
textor '{"command":"export-md-to-pdf","data":"RT7-{topic}-tan-cong-{datetime}.md"}'

# Hoặc dùng alias trong shell
# Xem: .fong/instructions/textor-mdlatex/02-command-reference.md
```

**Output:**

- `{output-file}.pdf` - PDF file
- `{output-file}_img/` - Embedded images (nếu có diagrams)


---


## Output File Template (TIẾNG VIỆT CÓ DẤU)

**Filename:** `RT7-{topic}-tan-cong-{YYYYMMDD-HHMMSS}.md`

```markdown
---
title: "Tấn Công Red Team: {Topic}"
subtitle: "RT7 Kiểm Chứng Đối Kháng Cực Đoan"
author: "Red Team Skill cho Thanh-Phong Lam"
date: "{YYYY-MM-DD}"
protocol: "RT7"
rounds_completed: 7
verdict: "ĐẠT|THẤT BẠI|CẦN LƯU Ý"
version: "1.0.0"
language: "Vietnamese"
---


# Tấn Công Red Team: {Topic}


## Tuyên bố miễn trừ

Tài liệu này được tạo bằng phương pháp Red Team với H0 = "CÁI NÀY SAI".
Tất cả tấn công là kiểm chứng đối kháng, không phải chỉ trích cá nhân.
Mục đích: Tìm điểm yếu trước khi triển khai/xuất bản.

**Tạo bởi:** Red Team Skill cho Thanh-Phong Lam
**Giao thức:** RT7 (7 vòng, 5W1H + 6 Mũ, Công cụ DSS)
**Ngày:** {YYYY-MM-DD HH:MM:SS} (+07)


## Tóm tắt

| Chỉ số | Giá trị |
|--------|---------|
| Tổng tấn công | N |
| Đạt | N |
| Thất bại | N |
| Cần lưu ý | N |
| **Kết luận** | **ĐẠT/THẤT BẠI/CẦN LƯU Ý** |


## Mục tiêu tấn công

> {Tuyên bố/giả thuyết/code bị tấn công}


## Ma trận tấn công


### Vòng 1: Tấn công 5W1H

| Câu hỏi | Tấn công | Bằng chứng | Kết quả |
|---------|----------|------------|---------|
| Cái gì (What) | {tấn công} | {bằng chứng}[^1] | ĐẠT/THẤT BẠI |
| Tại sao (Why) | {tấn công} | {bằng chứng}[^2] | ĐẠT/THẤT BẠI |
| Ở đâu (Where) | {tấn công} | {bằng chứng} | ĐẠT/THẤT BẠI |
| Khi nào (When) | {tấn công} | {bằng chứng} | ĐẠT/THẤT BẠI |
| Ai (Who) | {tấn công} | {bằng chứng} | ĐẠT/THẤT BẠI |
| Làm sao (How) | {tấn công} | {bằng chứng} | ĐẠT/THẤT BẠI |


### Vòng 2: Tấn công 3 cấp độ

| Cấp | Phương pháp | Tấn công | Bằng chứng | Kết quả |
|-----|-------------|----------|------------|---------|
| L1 | Phản ví dụ (Counter-example) | {tấn công} | {bằng chứng}[^3] | ĐẠT/THẤT BẠI |
| L2 | Mâu thuẫn (Contradiction) | {tấn công} | {bằng chứng} | ĐẠT/THẤT BẠI |
| L3 | Giả thuyết không (Null Hypothesis) | {tấn công} | {bằng chứng} | ĐẠT/THẤT BẠI |


### Vòng 3: Xác minh bằng công cụ DSS

| Công cụ | Truy vấn | Phát hiện | Kết quả |
|---------|----------|-----------|---------|
| NewRAG | "{truy vấn}" | {phát hiện}[^4] | ĐẠT/THẤT BẠI |
| Perplexity | "{truy vấn}" | {phát hiện}[^5] | ĐẠT/THẤT BẠI |
| Copilot | "{truy vấn}" | {phát hiện}[^6] | ĐẠT/THẤT BẠI |
| Z.AI | "{truy vấn}" | {phát hiện}[^7] | ĐẠT/THẤT BẠI |
| Safe Math | {biểu thức} | {kết quả} | ĐẠT/THẤT BẠI |


### Vòng 4-7: Tấn công sâu

{Lặp lại 5W1H + 3 cấp độ + DSS cho các vòng còn lại}


## Vấn đề cần lưu ý (nếu có)

1. **{Vấn đề 1}**: {Mô tả}[^8]
2. **{Vấn đề 2}**: {Mô tả}


## Khuyến nghị

1. {Khuyến nghị 1}
2. {Khuyến nghị 2}


## Kết luận

**{ĐẠT|THẤT BẠI|CẦN LƯU Ý}**

Lý do: {Tại sao kết luận như vậy}

---

[^1]: Nguồn1 (Năm). Tiêu đề. Nhà xuất bản/URL.

[^2]: NewRAG: DKM-TênSách.pdf.P##.

[^3]: Perplexity (2026-01-24). Truy vấn: "từ khóa".

[^4]: NewRAG: DKM-TênSách.pdf.P##.

[^5]: Perplexity (2026-01-24). Truy vấn: "từ khóa".

[^6]: Copilot (2026-01-24). Truy vấn: "từ khóa".

[^7]: Z.AI (2026-01-24). Truy vấn: "từ khóa".

[^8]: Safe Math: kết quả tính toán.
```


---


## Pre-Prompt Template (RCIFENI-O)

Khi user invoke `/red-team`, AI PHẢI output response theo format sau:

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
O: Attack {target} với extreme adversarial validation
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
2. **Nhận target** -> Confirm RT7 (7 rounds)
3. **Create output folder**: `.fong/docs/red-team-output/{YYYYMMDD-HHMMSS}/`
4. **Execute 7 rounds** (BẮT BUỘC):

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

5. **Create attack report** với footnote citations
6. **Verify** all footnotes defined at end of file
7. **Read Textor rules** trước khi export
8. **Export PDF** via Textor

**Output folder structure:**

```
.fong/docs/red-team-output/{YYYYMMDD-HHMMSS}/
|-- RT7-{topic}-attack.md      # Full attack matrix với footnotes
|-- RT7-{topic}-attack.pdf     # PDF export via Textor
|-- RT7-{topic}-attack_img/    # Diagram images (nếu có)
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
