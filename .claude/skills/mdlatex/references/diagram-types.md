# Diagram Types Reference


## Mermaid (13 Types)

| # | Type | Syntax | Use Case |
|---|------|--------|----------|
| 1 | Flowchart | `graph LR/TD` | Process flows, decision trees |
| 2 | Sequence | `sequenceDiagram` | API calls, interactions |
| 3 | Class | `classDiagram` | OOP structure |
| 4 | State | `stateDiagram-v2` | State machines |
| 5 | ER | `erDiagram` | Database schema |
| 6 | Gantt | `gantt` | Project schedules |
| 7 | Pie | `pie` | Distribution data |
| 8 | Mindmap | `mindmap` | Brainstorming, overview |
| 9 | Timeline | `timeline` | Historical events |
| 10 | Git | `gitGraph` | Git branching strategy |
| 11 | User Journey | `journey` | UX flow |
| 12 | Quadrant | `quadrantChart` | Priority matrix |
| 13 | Sankey | `sankey-beta` | Flow quantities |

**Full guide:** `.fong/instructions/textor-mdlatex/03-mermaid-guide.md`


## PlantUML (11 Types)

| # | Type | Best For |
|---|------|----------|
| 1 | Sequence | System interactions |
| 2 | Use Case | Requirements |
| 3 | Class | Architecture |
| 4 | Activity | Workflows |
| 5 | Component | System design |
| 6 | Deployment | Infrastructure |
| 7 | Object | Instances |
| 8 | Timing | Time-based |
| 9 | Salt (Wireframe) | UI mockups |
| 10 | JSON | Data structure |
| 11 | YAML | Config visualization |

**Full guide:** `.fong/instructions/textor-mdlatex/06-plantuml-guide.md`


## TikZ

| Feature | Detail |
|---------|--------|
| Output | Vector (native LaTeX) |
| Math | Full LaTeX math support |
| Precision | Manual coordinate placement |
| Best for | Mathematical diagrams, precise layouts |

**Full guide:** `.fong/instructions/textor-mdlatex/13-tikz-guide.md`


## Decision Matrix: Which Diagram Tool?

| Need | Tool | Why |
|------|------|-----|
| Quick flowchart | Mermaid | Simple syntax, fast |
| UML diagram | PlantUML | Full UML support |
| UI mockup | PlantUML Salt | Built-in widgets |
| Math diagram | TikZ | LaTeX native |
| Mindmap | Mermaid | Easy syntax |
| Sequence | Either | Both good |
| Precision layout | TikZ | Manual coordinates |


## Blue-Gray CUD Palette (PlantUML)

| Hex | Role |
|-----|------|
| #2C3E50 | Text/font |
| #34495E | Arrows |
| #5D6D7E | Borders |
| #85929E | Package borders |
| #D5DBDB | Database/notes |
| #E8ECED | Component backgrounds |
| #F4F6F6 | Package backgrounds |
| #FFFFFF | Main background |

**SSoT:** `.fong/instructions/LaTeX/color-CUD-palette.json`
