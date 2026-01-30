---
name: write-paper
description: This skill should be used when the user asks to "write paper", "write academic paper", "viet bai bao", "viet luan van", "research paper", "Q1 paper", "journal article", uses {write-paper}, {paper}, or needs structured academic writing workflow.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: .fong/instructions/academic/
latex_instructions: .fong/instructions/LaTeX/
textor_instructions: .fong/instructions/textor-mdlatex/
dss_instructions: .fong/instructions/instructions-DSS-decision-support-system.md
output_language: Vietnamese
---

# Write Paper - Academic Paper Writing Skill

Viet bai bao hoc thuat voi LaTeX. Workflow tu Pre-writing den Submission. Output .tex chuan journal.

**CRITICAL - MANDATORY FIRST ACTIONS (Zero Skip)**:

```
READ .fong/instructions/academic/scientific-plain-vietnamese-checklist.md
READ .fong/instructions/academic/instructions-write-abstract.json
READ .fong/instructions/LaTeX/00-latex-principles.md
READ .fong/instructions/LaTeX/01-30-principles.md
READ .fong/instructions/textor-mdlatex/01-critical-rules.md
```

Use Read tool with ABSOLUTE PATH. Do NOT skip ANY step.


## Output Language

> **Phan biet ro paper tieng Anh va tieng Viet.**


### Paper TIENG ANH (International Journals)

**Rules:**

- Viet truc tiep bang tieng Anh
- KHONG dung VETA (khong can viet hoa)
- Follow journal style guide (APA, IEEE, etc.)
- Grammar check: LanguageTool, Grammarly, native speaker


### Paper TIENG VIET (Tap chi trong nuoc)

**Ref:** `.fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json`

**Rules:**

- Output file .md/.tex = TIENG VIET day du dau
- Thuat ngu ky thuat = Inline format: "Ten Viet (English term)"
- **VETA BAT BUOC** de viet hoa chinh xac thuat ngu
- Ref: `.fong/instructions/academic/scientific-plain-vietnamese-checklist.md`

**VETA Execution (chi cho paper tieng Viet):**

```bash
# Co file path
.fong/tools/veta-gemini.sh /path/to/file

# Fallback
.fong/tools/veta-copilot.sh /path/to/file
```


## Core Concept

Paper = Story. Gap → Solution → Evidence → Contribution.
Write body first. Abstract last.
One paragraph = One job. Every sentence fights.


## Protocol: WP5 (5 Phases)

| Phase | Description | Deliverables |
|-------|-------------|--------------|
| **WP1** | Pre-writing | Research question, outline, literature map |
| **WP2** | Drafting | v0 draft, sections complete |
| **WP3** | LaTeX Formatting | .tex file, figures, tables |
| **WP4** | Revision | v1-v3 revisions, language polish |
| **WP5** | Submission | Cover letter, supplementary, final check |


## WP1: Pre-writing Phase (CRITICAL)

| Task | Description | Output |
|------|-------------|--------|
| Target journal | Chon tap chi truoc khi viet | Journal name, guidelines URL |
| Research gap | Xac dinh khoang trong nghien cuu | Gap statement (1-2 sentences) |
| Main contribution | Dong gop chinh la gi? | Contribution statement |
| Storyline | Pha viet ke chuyen | Outline với flow |
| Literature map | Ban do tai lieu | Mind map or table |

**DSS Query Pattern (WP1):**
```
queryPerplexity: "{topic} research gap 2025"
queryNewRAG: ["literature review {topic}", "{topic} methodology"]
queryArXiv: "{topic}" (recent papers)
```


## WP2: Drafting Phase

| Section | Order | Key Points |
|---------|-------|------------|
| Methods | 1st | Replicable. Parameters. Software versions. |
| Results | 2nd | Primary finding first. Numbers. Effect size. |
| Discussion | 3rd | Interpret. Compare. Limitations. |
| Introduction | 4th | Gap. Contribution. Structure. |
| Conclusion | 5th | Brief. No repeat. Future work. |
| Abstract | LAST | Write AFTER paper done. 150-300 words. |

**Writing Rules:**

- 1 paragraph = 1 job. Topic sentence first.
- Van xuoi lien mach. Khong bullet points trong body.
- Moi khang dinh co trich dan.
- So lieu thay tinh tu ("15.4%" khong phai "tang manh").
- Hedging: "suggests", "indicates", not "proves".


## WP3: LaTeX Formatting

**Template Priority:**

1. Journal official template (REQUIRED if available)
2. elsarticle, IEEEtran, acmart (common)
3. Local template: `.fong/instructions/LaTeX/templates/article-hub/`

**LaTeX Best Practices:**

| Rule | Description |
|------|-------------|
| Modular structure | main.tex + sections/ + figs/ + bib/ |
| Font | XeLaTeX + New Computer Modern |
| Bibliography | BibLaTeX + Biber (or natbib nếu journal yêu cầu) |
| Figures | Vector (PDF/SVG). >=300 DPI for raster. |
| Tables | booktabs + siunitx. Không đường kẻ dày. |
| References | cleveref/hyperref cho cross-reference |
| Version control | Git. Commit mỗi thay đổi nội dung. |

**Build Command:**
```bash
# XeLaTeX build
xelatex main.tex && biber main && xelatex main.tex && xelatex main.tex

# Or use latexmk
latexmk -xelatex main.tex
```

**Ref:** `.fong/instructions/LaTeX/07-build-watch-debug.md`


## WP4: Revision Phase

| Version | Focus | Reviewer |
|---------|-------|----------|
| v0 | Outline | Self |
| v1 | Content complete | Self |
| v2 | Structure + flow | Co-author/Supervisor |
| v3 | Language polish | Native speaker/Editor |
| v4 | Submission-ready | Final check |

**Revision Checklist:**

- [ ] Story arc clear? (Gap → Solution → Evidence)
- [ ] Every paragraph has one job?
- [ ] All claims cited?
- [ ] Numbers accurate? (Use Safe Math MCP)
- [ ] Hedging appropriate?
- [ ] Terminology consistent?
- [ ] Grammar/spelling checked? (LanguageTool)

**Red Team Each Section:**

Ref: `.claude/skills/red-team/SKILL.md`

```
H0 = "This section is WRONG"
Attack: 5W1H + 3 Levels
Verify: Numbers, claims, citations
```


## WP5: Submission Phase

| Task | Description |
|------|-------------|
| Cover letter | Ngắn gọn. Đóng góp mới. Phù hợp tạp chí. |
| Supplementary | Methods, code, data, long tables |
| Format check | Page limit, font, figure size, file types |
| Author info | ORCID, affiliations, contributions |
| Preprint | Upload arXiv nếu policy cho phép |

**Submission Checklist (15 items):**

- [ ] Journal guidelines read?
- [ ] Word/page limit OK?
- [ ] All figures high quality?
- [ ] All tables formatted?
- [ ] Bibliography complete?
- [ ] Abstract <= word limit?
- [ ] Keywords selected?
- [ ] Cover letter written?
- [ ] Author order confirmed?
- [ ] ORCID linked?
- [ ] Conflict of interest declared?
- [ ] Data availability stated?
- [ ] Supplementary prepared?
- [ ] PDF compiles without errors?
- [ ] Final read-through done?


---


## DSS Integration (MANDATORY)

**Ref:** `.fong/instructions/instructions-DSS-decision-support-system.md`

| Phase | DSS Tools |
|-------|-----------|
| WP1 | NewRAG, Perplexity, ArXiv, SLR |
| WP2 | NewRAG (writing guides), Copilot |
| WP3 | Context7 (LaTeX packages) |
| WP4 | Safe Math (verify numbers), Red Team |
| WP5 | Perplexity (journal policies) |

**Rule:** Every major decision → Query >=2 sources.


## Tools Reference

| Tool | Purpose | Ref |
|------|---------|-----|
| **LaTeX** | Paper formatting | `.fong/instructions/LaTeX/` |
| **Textor** | MD → PDF conversion | `.fong/instructions/textor-mdlatex/` |
| **DSS** | Multi-source research | `.claude/skills/dss/SKILL.md` |
| **Red Team** | Adversarial validation | `.claude/skills/red-team/SKILL.md` |
| **Safe Math** | Number verification | `.fong/instructions/instructions-mcp-safe-calculation-math-engine.md` |
| **BibTeX** | Bibliography management | biber/natbib |


---


## Output Location

**Default folder:** Project root or specified by user

**File Naming Convention:**

| Pattern | Example |
|---------|---------|
| `{author}-{year}-{short-title}.tex` | `lam-2026-bank-diversification.tex` |
| `{author}-{year}-{short-title}.bib` | `lam-2026-bank-diversification.bib` |

**Folder Structure:**

```
paper-{short-title}/
├── main.tex              # Main document
├── sections/
│   ├── 01-introduction.tex
│   ├── 02-literature.tex
│   ├── 03-methodology.tex
│   ├── 04-results.tex
│   ├── 05-discussion.tex
│   └── 06-conclusion.tex
├── figs/                 # Figures (PDF/PNG)
├── tables/               # Tables (if separate)
├── references.bib        # Bibliography
├── supplementary/        # Supplementary materials
└── build.sh              # Build script
```


---


## Pre-Prompt Template (RCIFENI-O)

Khi user invoke `/write-paper`, AI PHAI output response theo format sau:

```
`Think BIG, DO small steps`, `step by step`. Best effort to `get things done`. ULTRATHINK activated.
Skill: /write-paper | Protocol: WP5 (5 phases)
{YYYY-MM-DD HH:MM:SS} (+07)

# 1. Role:
Academic Paper Writer + LaTeX Expert + DSS Researcher

# 2. Context:
Topic: {user's topic}
Target Journal: {journal name or TBD}
Protocol: WP5 (Pre-writing → Drafting → LaTeX → Revision → Submission)
Output: .tex file with proper structure

# 3. Instructions:
1. READ all required files (academic, LaTeX, textor)
2. Execute WP1: Define gap, contribution, outline
3. Execute WP2: Draft sections in order
4. Execute WP3: Format with LaTeX template
5. Execute WP4: Revise with Red Team validation
6. Execute WP5: Prepare submission package

# 4. Output Format:
- Folder: paper-{short-title}/
- Files: main.tex, sections/*.tex, references.bib
- Build: xelatex + biber pipeline

# 5. Cautions:
- anti: Write abstract before paper
- anti: Mental math (use Safe Math MCP)
- anti: Single-source claims (use DSS)
- anti: Bullet points in body text
- anti: Overclaiming causality

# 6. OKR:
O: Write {topic} paper for {journal}
KR1: Complete all 5 phases
KR2: LaTeX compiles without errors
KR3: All claims cited and numbers verified
```


---


## AI Workflow

**STEP 0 - MANDATORY FIRST (Zero Skip):**

```
Read tool → .fong/instructions/academic/scientific-plain-vietnamese-checklist.md
Read tool → .fong/instructions/LaTeX/00-latex-principles.md
Read tool → .fong/instructions/LaTeX/01-30-principles.md
```

1. **Print Pre-Prompt** → Show RCIFENI-O template above
2. **Nhận topic** → Confirm target journal
3. **Execute WP1** → DSS research, define gap/contribution
4. **Execute WP2** → Draft sections (Methods → Results → Discussion → Intro → Conclusion → Abstract)
5. **Execute WP3** → Apply LaTeX template, format figures/tables
6. **Execute WP4** → Red Team each section, verify numbers
7. **Execute WP5** → Prepare submission package
8. **Verify** → Build LaTeX, check errors


---


## Checklist (21 items - MANDATORY)

**Kill Items (abort if fail):**

- [ ] Target journal identified?
- [ ] Research gap defined?
- [ ] Main contribution stated?

**Pre-writing:**

- [ ] Literature search done (DSS)?
- [ ] Outline created?
- [ ] Storyline clear?

**Drafting:**

- [ ] Methods written (replicable)?
- [ ] Results written (numbers)?
- [ ] Discussion written (interpretation)?
- [ ] Introduction written (gap + contribution)?
- [ ] Conclusion written (brief)?
- [ ] Abstract written LAST?

**LaTeX:**

- [ ] Template applied?
- [ ] Figures formatted (vector/high DPI)?
- [ ] Tables formatted (booktabs)?
- [ ] Bibliography complete?
- [ ] Build successful?

**Revision:**

- [ ] Red Team validation done?
- [ ] Numbers verified (Safe Math)?
- [ ] Language polished?

**Submission:**

- [ ] All files prepared?


---


## Cross-References

| Context | File |
|---------|------|
| **Academic Writing VN** | `.fong/instructions/academic/scientific-plain-vietnamese-checklist.md` |
| **Abstract Writing** | `.fong/instructions/academic/instructions-write-abstract.json` |
| **LaTeX Principles** | `.fong/instructions/LaTeX/00-latex-principles.md` |
| **30 LaTeX Rules** | `.fong/instructions/LaTeX/01-30-principles.md` |
| **LaTeX Templates** | `.fong/instructions/LaTeX/templates/` |
| **LaTeX Build** | `.fong/instructions/LaTeX/07-build-watch-debug.md` |
| **Textor** | `.fong/instructions/textor-mdlatex/` |
| **DSS Skill** | `.claude/skills/dss/SKILL.md` |
| **Red Team Skill** | `.claude/skills/red-team/SKILL.md` |
| **Safe Math** | `.fong/instructions/instructions-mcp-safe-calculation-math-engine.md` |


---


## Additional Resources


### Reference Files

- **`references/paper-structure.md`** - IMRaD structure guide
- **`references/latex-packages.md`** - Common LaTeX packages


### Example Files

- **`examples/paper-outline-template.md`** - Outline template
- **`examples/cover-letter-template.md`** - Cover letter template


### Scripts

- **`scripts/build-paper.sh`** - LaTeX build script
- **`scripts/validate-bib.sh`** - Bibliography validation


---


**References:**

[1] Perplexity-2026-01-24: Academic paper writing best practices 2025
[2] Copilot-2026-01-24: LaTeX paper writing workflow
[3] DKM-Academic-Writing-for-Graduate-Student.PDF
[4] DKM-Writing-In-English-Svobodova.pdf
[5] scientific-plain-vietnamese-checklist.md
[6] instructions-write-abstract.json
