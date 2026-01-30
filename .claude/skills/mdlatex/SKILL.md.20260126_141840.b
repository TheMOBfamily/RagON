---
name: mdlatex
description: This skill should be used when the user asks to "create document", "write markdown", "export PDF", "tao tai lieu", "xuat PDF", "add diagram", "Mermaid", "PlantUML", "TikZ", "mdlatex", "textor", uses {mdlatex}, {textor}, or needs markdown-to-PDF conversion with diagrams.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: .fong/instructions/textor-mdlatex/
script_path: /home/fong/Projects/textor-doc-converter/run-807f321188c6.sh
veta_instructions: .fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json
output_language: Vietnamese
---

# MD LaTeX - Markdown Document & PDF Export Skill

Tao tai lieu Markdown chuan voi diagram (Mermaid, PlantUML, TikZ) va export PDF qua Textor.


## Output Language: TIENG VIET CO DAU (MANDATORY)

> **VIET HOA CUC DOAN** - Tat ca output phai bang tieng Viet CO DAU day du.

**Ref:** `.fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json`

**Rules:**

- Output file .md/.pdf = TIENG VIET CO DAU (khong duoc viet khong dau)
- Thuat ngu ky thuat = Inline format: "Ten Viet (English term)"
- KHONG tao bang thuat ngu rieng (render xau trong PDF)
- Dung VETA de Viet hoa chinh xac
- **CRITICAL:** Viet khong dau = VIOLATION. Phai co day du dau tieng Viet.

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

| Input Type | Vi du | Output |
|------------|-------|--------|
| **Document** | Tai lieu, bao cao, huong dan | .md + .pdf |
| **Diagram** | Flowchart, sequence, mindmap | .md voi diagram blocks |
| **Template** | Skeleton document | .md tu skeleton |
| **Existing .md** | File can export | .pdf qua Textor |
| **Mixed** | Text + diagrams + math | .md + .pdf day du |


**CRITICAL - MANDATORY FIRST ACTIONS (Zero Skip)**:

```
READ .fong/instructions/textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md
READ .fong/instructions/textor-mdlatex/01-critical-rules.md
READ .fong/instructions/textor-mdlatex/01b-critical-rules-diagrams.md
READ .fong/instructions/textor-mdlatex/01c-critical-rules-plantuml-quality.md
READ .fong/instructions/textor-mdlatex/12-footnote-citation.md
READ .fong/instructions/textor-mdlatex/99-skeleton-template.md
```

Use Read tool with ABSOLUTE PATH. Do NOT skip ANY step.


## Core Concept

MD LaTeX = Markdown LaTeX. Markdown with diagrams to PDF.
Textor converts Mermaid/PlantUML/TikZ to images, embeds in PDF.
Pandoc alone CANNOT render diagrams. Textor CAN.


---


## Critical Rules (6 Rules - MANDATORY)


### Rule 1: NO EMOJI

XeLaTeX khong render emoji. Professional docs khong co emoji.
Exception: Chi khi user EXPLICITLY yeu cau.


### Rule 2: Max 3 Heading Levels

- H1 (#): YAML title only - KHONG dung trong content
- H2 (##): Main sections
- H3 (###): Sub-sections
- KHONG DUNG H4 (####) tro xuong
- Thay the H4: dung **bold text**


### Rule 3: 2 Newlines Spacing

Header hoac bold text -> 2 newlines -> Content.
1 newline = SAI. 2 newlines = DUNG.


### Rule 4: YAML Frontmatter (MANDATORY)

```yaml
---
title: "Tieu de tai lieu"
subtitle: "Mo ta ngan"
author: "Fong"
date: "YYYY-MM-DD"
version: "1.0.0"
---
```


### Rule 5: Footnote Citation

```markdown
Trong text: Ket qua nghien cuu[^1]. Nguon khac xac nhan[^2].

Cuoi file:
[^1]: Author (Year). Title. Publisher, p.XX.
[^2]: Author (Year). Title. arXiv:XXXX.
```

Bat buoc dau `^`. `[^1]` KHONG phai `[1]`.


### Rule 6: Diagram Quality

- PlantUML: `skinparam dpi 300` BAT BUOC
- Bang mau Blue-Gray CUD (colorblind-friendly)
- Mermaid: 13 loai diagram ho tro
- TikZ: Full LaTeX math, vector output


---


## Diagram Types


### Mermaid (13 Types)

| Type | Syntax | Best For |
|------|--------|----------|
| Flowchart | `graph LR/TD` | Process flows |
| Sequence | `sequenceDiagram` | API interactions |
| Class | `classDiagram` | OOP structure |
| State | `stateDiagram-v2` | State machines |
| ER | `erDiagram` | Database design |
| Gantt | `gantt` | Project timeline |
| Pie | `pie` | Distribution |
| Mindmap | `mindmap` | Brainstorming |
| Timeline | `timeline` | History |
| Git | `gitGraph` | Branch strategy |

**Ref:** `.fong/instructions/textor-mdlatex/03-mermaid-guide.md`


### PlantUML (11 Types)

| Type | Syntax | Best For |
|------|--------|----------|
| Sequence | `@startuml` | Interactions |
| Use Case | `@startuml` | Requirements |
| Class | `@startuml` | Architecture |
| Activity | `@startuml` | Workflows |
| Component | `@startuml` | System design |
| Salt | `@startsalt` | UI mockups |

**Ref:** `.fong/instructions/textor-mdlatex/06-plantuml-guide.md`

**PlantUML Skeleton (Blue-Gray CUD):**

```plantuml
@startuml diagram-name
skinparam dpi 300
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontColor #2C3E50
skinparam shadowing false
skinparam component {
  BackgroundColor #E8ECED
  BorderColor #5D6D7E
}
title Tieu de Diagram
' [Content here]
@enduml
```


### TikZ (LaTeX Native)

```markdown
```tikz
\draw[->] (0,0) -- (2,0);
\node at (1,0.5) {Hello TikZ};
```
```

**Ref:** `.fong/instructions/textor-mdlatex/13-tikz-guide.md`


### Mermaid vs PlantUML vs TikZ

| Criteria | Mermaid | PlantUML | TikZ |
|----------|---------|----------|------|
| Output | PNG | PNG | Vector |
| Syntax | Simple | Verbose | LaTeX |
| Math | No | No | Full LaTeX |
| Positioning | Auto | Auto | Manual |
| Best for | Quick diagrams | UML, Salt UI | Math, precision |


---


## Textor Export Commands


### Basic Export

```bash
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"/absolute/path/file.md"}'
```


### Landscape

```bash
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","page_size":"A4","orientation":"landscape"}'
```


### Brand Logo Watermark

| Preset | Alias | Logo |
|--------|-------|------|
| `hub` | `buh` | HUB University |
| `deutschfuns` | `de` | DeutschFuns |
| `irontan` | - | IronTan |
| `nexiumlab` | - | NexiumLab |

```bash
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","icon":"hub"}'
```


### Validate Before Export

```bash
# Validate PlantUML
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"validate-plantuml","data":"@startuml\nAlice->Bob\n@enduml"}'

# Validate Mermaid
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"validate-mermaid","data":"graph LR\nA-->B"}'

# Validate MD with PlantUML
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"validate-md-plantuml","data":"file.md"}'

# Validate MD with Mermaid
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"validate-md-mermaid","data":"file.md"}'
```


### Show Full Help

```bash
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh --help
```


---


## Output Location

**Default:** Same folder as input .md file.

**Output files:**

| File | Purpose |
|------|---------|
| `{filename}.pdf` | PDF output |
| `{filename}_img/` | Diagram images (PNG + SVG) |


---


## Blue-Gray CUD Palette (Quick Reference)

| Hex | Usage |
|-----|-------|
| #2C3E50 | Text, font |
| #34495E | Arrows |
| #5D6D7E | Borders |
| #85929E | Package borders |
| #D5DBDB | Database, notes |
| #E8ECED | Component backgrounds |
| #F4F6F6 | Package backgrounds |
| #FFFFFF | Main background |

**SSoT:** `.fong/instructions/LaTeX/color-CUD-palette.json`


---


## Document Skeleton Template

```markdown
---
title: "Tieu de tai lieu"
subtitle: "Mo ta ngan"
author: "Fong"
date: "YYYY-MM-DD"
version: "1.0.0"
updated: "YYYY-MM-DD"
---


## Tom tat


[Giai thich don gian 1-2 cau, dung vi du doi thuong]


## Tong quan


[Mo ta chung ve noi dung]


## Noi dung chinh


### Phan 1


[Noi dung]


### Phan 2


[Noi dung]


## Ghi chu


[Cac luu y quan trong]


[^1]: Nguon tham khao 1.

[^2]: Nguon tham khao 2.
```


---


## Pre-Prompt Template (RCIFENI-O)

Khi user invoke `/mdlatex`, AI PHAI output response theo format sau:

```
`Think BIG, DO small steps`, `step by step`. Best effort to `get things done`. ULTRATHINK activated.
Skill: /mdlatex | Tool: Textor Doc Converter
{YYYY-MM-DD HH:MM:SS} (+07)

# 1. Role:
Document Creator + Diagram Designer + Textor Expert

# 2. Context:
Topic: {user's topic}
Output: .md file with diagrams -> .pdf via Textor
Diagrams: {Mermaid / PlantUML / TikZ / None}

# 3. Instructions:
1. READ all required textor-mdlatex instruction files
2. Create .md with YAML frontmatter
3. Add diagrams if needed (Mermaid/PlantUML/TikZ)
4. Add footnote citations [^N]
5. Validate diagrams
6. Export .md to .pdf via Textor

# 4. Output Format:
- File: {filename}.md
- YAML frontmatter required
- Max H3, NO emoji, 2 newlines spacing
- Footnote citations [^N]
- Export: {filename}.pdf via Textor

# 5. Cautions:
- anti: Emoji in content (XeLaTeX fail)
- anti: H4+ headings (Textor fail)
- anti: 1 newline spacing (must be 2)
- anti: Endnote [1] (must be footnote [^1])
- anti: Missing YAML frontmatter
- anti: Low DPI diagrams (must be 300)
- anti: Pandoc for files with diagrams (use Textor)

# 6. OKR:
O: Create {topic} document with diagrams and export PDF
KR1: .md file with correct formatting
KR2: Diagrams rendered correctly
KR3: .pdf exported via Textor without errors
```


---


## AI Workflow

**STEP 0 - MANDATORY FIRST (Zero Skip):**

```
Read tool -> textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md
Read tool -> textor-mdlatex/01-critical-rules.md
Read tool -> textor-mdlatex/01b-critical-rules-diagrams.md
Read tool -> textor-mdlatex/01c-critical-rules-plantuml-quality.md
Read tool -> textor-mdlatex/12-footnote-citation.md
Read tool -> textor-mdlatex/99-skeleton-template.md
```

1. **Print Pre-Prompt** -> Show RCIFENI-O template above
2. **Nhan yeu cau** -> Xac dinh loai document va diagrams can thiet
3. **Chon diagram type**: Mermaid (quick) / PlantUML (UML) / TikZ (math) / None
4. **Create .md file** voi:
   - YAML frontmatter (title, subtitle, author, date, version)
   - Content theo skeleton template
   - Diagrams (neu co)
   - Footnote citations
5. **Validate** diagrams truoc khi export
6. **Export PDF** via Textor
7. **Verify** PDF output

**Validation workflow:**

```
IF has PlantUML -> validate-plantuml FIRST
IF has Mermaid -> validate-mermaid FIRST
IF has both -> validate-md-plantuml + validate-md-mermaid
THEN -> export-md-to-pdf
```


---


## Checklist (13 items - MANDATORY)

- [ ] Textor instruction files read?
- [ ] YAML frontmatter complete (title, subtitle, author, date, version)?
- [ ] Max H3 heading depth (no H4+)?
- [ ] NO emoji in content?
- [ ] 2 newlines between headers and content?
- [ ] Tieng Viet co dau day du?
- [ ] Diagram DPI = 300 (PlantUML)?
- [ ] Blue-Gray CUD palette used (PlantUML)?
- [ ] Footnote citations correct (`[^N]` not `[N]`)?
- [ ] Diagrams validated before export?
- [ ] PDF exported via Textor?
- [ ] PDF renders correctly (diagrams, footnotes)?
- [ ] Output files documented (pdf + _img/ folder)?


---


## Cross-References

| Context | File |
|---------|------|
| **Main Index** | `.fong/instructions/textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md` |
| **Critical Rules 1** | `.fong/instructions/textor-mdlatex/01-critical-rules.md` |
| **Critical Rules 2** | `.fong/instructions/textor-mdlatex/01b-critical-rules-diagrams.md` |
| **Critical Rules 3** | `.fong/instructions/textor-mdlatex/01c-critical-rules-plantuml-quality.md` |
| **VETA Localization** | `.fong/instructions/textor-mdlatex/01d-critical-rules-veta-localization.md` |
| **Command Reference** | `.fong/instructions/textor-mdlatex/02-command-reference.md` |
| **Mermaid Guide** | `.fong/instructions/textor-mdlatex/03-mermaid-guide.md` |
| **Mermaid Examples** | `.fong/instructions/textor-mdlatex/04-mermaid-examples.md` |
| **Mermaid Advanced** | `.fong/instructions/textor-mdlatex/05-mermaid-examples-advanced.md` |
| **PlantUML Guide** | `.fong/instructions/textor-mdlatex/06-plantuml-guide.md` |
| **PlantUML Examples** | `.fong/instructions/textor-mdlatex/07-plantuml-examples.md` |
| **Salt Guide** | `.fong/instructions/textor-mdlatex/08-plantuml-salt-guide.md` |
| **Salt Advanced** | `.fong/instructions/textor-mdlatex/09-plantuml-salt-advanced.md` |
| **XeLaTeX Alternative** | `.fong/instructions/textor-mdlatex/11-xelatex-alternative.md` |
| **Footnote Citation** | `.fong/instructions/textor-mdlatex/12-footnote-citation.md` |
| **TikZ Guide** | `.fong/instructions/textor-mdlatex/13-tikz-guide.md` |
| **Quick Reference** | `.fong/instructions/textor-mdlatex/99-quick-reference.md` |
| **Skeleton Template** | `.fong/instructions/textor-mdlatex/99-skeleton-template.md` |
| **CUD Palette** | `.fong/instructions/LaTeX/color-CUD-palette.json` |
| **VETA Analyzer** | `.fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json` |


---


## Additional Resources


### Reference Files

- **`references/diagram-types.md`** - Mermaid vs PlantUML vs TikZ comparison


### Example Files

- **`examples/basic-document.md`** - Basic document with skeleton template


### Scripts

- **`scripts/export-pdf.sh`** - Quick export helper script
