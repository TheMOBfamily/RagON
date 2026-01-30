# LaTeX Packages - Quick Reference

> Cac package thuong dung cho bai bao khoa hoc.


## Essential Packages

| Package | Purpose | Usage |
|---------|---------|-------|
| `fontspec` | Font selection (XeLaTeX) | `\setmainfont{}` |
| `geometry` | Page margins | `\usepackage[margin=2.54cm]{geometry}` |
| `setspace` | Line spacing | `\onehalfspacing` |
| `graphicx` | Include figures | `\includegraphics{}` |
| `booktabs` | Professional tables | `\toprule`, `\midrule`, `\bottomrule` |
| `amsmath` | Math equations | `\begin{equation}` |
| `hyperref` | Hyperlinks | Auto-links |


## Bibliography

| Package | Style | Usage |
|---------|-------|-------|
| `biblatex` | Modern, flexible | `\usepackage[style=apa]{biblatex}` |
| `natbib` | Classic, wide support | `\usepackage{natbib}` |

**Recommendation:** biblatex + biber (modern). natbib if journal requires.


## Figures & Tables

| Package | Purpose |
|---------|---------|
| `graphicx` | Include images |
| `tikz` | Draw diagrams |
| `pgfplots` | Data plots |
| `booktabs` | Professional tables |
| `tabularx` | Flexible table width |
| `siunitx` | Numbers and units |
| `subcaption` | Subfigures |


## Cross-referencing

| Package | Purpose | Syntax |
|---------|---------|--------|
| `hyperref` | Clickable links | `\ref{}`, `\cite{}` |
| `cleveref` | Smart references | `\cref{}` |

**Example:**
```latex
\cref{fig:results}  % → "Figure 1"
\cref{tab:data}     % → "Table 2"
```


## Typography

| Package | Purpose |
|---------|---------|
| `microtype` | Better typography |
| `fontspec` | Font selection |
| `unicode-math` | Unicode math symbols |


## Common Templates

| Template | Journal Type |
|----------|--------------|
| `elsarticle` | Elsevier journals |
| `IEEEtran` | IEEE journals |
| `acmart` | ACM journals |
| `article` | Generic |


## Minimal Preamble

```latex
\documentclass[12pt, a4paper]{article}

% Font (XeLaTeX)
\usepackage{fontspec}
\setmainfont{New Computer Modern}

% Layout
\usepackage[margin=2.54cm]{geometry}
\usepackage{setspace}
\onehalfspacing

% Math
\usepackage{amsmath}

% Graphics
\usepackage{graphicx}
\usepackage{booktabs}

% Bibliography
\usepackage[style=apa, backend=biber]{biblatex}
\addbibresource{references.bib}

% Links
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black}
```


---

**Ref:** `.fong/instructions/LaTeX/05a-template-preamble.md`
