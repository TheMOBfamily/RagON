---
name: wp-php-code-review
description: This skill should be used when the user asks to "review code", "code review", "review PR", "check code quality", "validate codestyle", "review PHP", "review JS", "review CSS", uses {code-review}, {review}, or needs systematic code quality validation against Deutschfuns LMS standards.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
output_language: Vietnamese
---

# WP PHP Code Review - Deutschfuns LMS Code Quality Skill

Review code PHP/JS/CSS/HTML theo chuan Deutschfuns LMS. Output .md TIENG VIET CO DAU voi checklist matrix + evidence.


## Output Language: TIENG VIET CO DAU (MANDATORY)

- Output file .md = tieng Viet co dau day du
- Thuat ngu ky thuat = Inline: "Ten Viet (English term)"
- Viet khong dau = VIOLATION


## Input Types

| Input Type | Vi du | Review Focus |
|------------|-------|--------------|
| **PHP file(s)** | Helper, hook, class, service | Full PHP checklist (15 items) |
| **JS file(s)** | ES6 module, handler, init | Full JS checklist (15 items) |
| **CSS file(s)** | Component, page init | Full CSS checklist (15 items) |
| **HTML/DOM** | Template, BEM structure | BEM checklist (10 items) |
| **PR / Branch** | git diff, multiple files | All applicable checklists |
| **Module** | Folder with mixed files | All checklists per file type |

**Auto-Detection:**

```
IF input is .php file(s) -> PHP checklist
IF input is .js file(s) -> JS checklist
IF input is .css file(s) -> CSS checklist
IF input has HTML/DOM -> BEM checklist
IF input is PR/branch -> detect file types -> apply all relevant checklists
IF input is folder/module -> scan file types -> apply all relevant checklists
```


## CRITICAL - MANDATORY FIRST ACTIONS (Zero Skip)

```
READ .deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/99-quick-reference.md
READ .deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/02-enhanced-validation-checklist/00-validation-checklist-overview.md
READ .deutschfuns/docs/instructions-jsdoc-codestyle/99-quick-reference.md
READ .deutschfuns/docs/instructions-css-codestyle.md (Quick Checklist section)
READ .deutschfuns/docs/instructions-html-dom-BEM-codestyle.md (Quick Checklist section)
```

Use Read tool with ABSOLUTE PATH. Do NOT skip ANY step.


## Core Concept

Evidence-based review. Every PASS/FAIL must cite line number.
Checklist = law. No item skipped. No assumption.
Code speaks. Reviewer listens. Evidence decides.


## Review Protocol

| Scope | Checklist Items | When |
|-------|----------------|------|
| **Single PHP file** | 15 PHP items | Quick review |
| **Single JS file** | 15 JS items | Quick review |
| **Single CSS file** | 15 CSS items | Quick review |
| **HTML/DOM** | 10 BEM items | Quick review |
| **PR / Multi-file** | All applicable | Full review |
| **Module** | All + architecture | Deep review |

**Rules:**

- Every file reviewed individually with its checklist.
- Summary aggregates all files.
- FAIL items must have: file path, line number, violation description, fix suggestion.


---


## PHP Checklist (15 items) - CHK-PHP-01 to CHK-PHP-15

**Source:** `.deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/99-quick-reference.md`

### File Structure (4 items)

- **CHK-PHP-01**: Header: `<?php declare(strict_types=1); if (!defined('ABSPATH')) { exit; }`
- **CHK-PHP-02**: File size: helper <=150 LOC, class <=200 LOC
- **CHK-PHP-03**: Naming: `{function_name}-helper.php`, `{hook-name}-hook.php`, `{Class}-class.php`
- **CHK-PHP-04**: Prefix: `de_` functions, `DE_` constants

### Autoload and Dependencies (4 items)

- **CHK-PHP-05**: Trust autoload - NO `require_once` for internal files
- **CHK-PHP-06**: NO `function_exists()` for internal `de_*` functions
- **CHK-PHP-07**: ONLY check external plugin functions with `function_exists()`
- **CHK-PHP-08**: NO circular dependencies

### Code Quality (4 items)

- **CHK-PHP-09**: Use `de_time()` not `time()`, `de_time_mysql()` not `current_time('mysql')`
- **CHK-PHP-10**: NO `get_userdata()` in loops (memory leak)
- **CHK-PHP-11**: NO hardcode to pass unit test
- **CHK-PHP-12**: NO HTML in functions (use templates)

### PHPDoc and Standards (3 items)

- **CHK-PHP-13**: PHPDoc minimal: `@param`, `@return` - NO redundant info
- **CHK-PHP-14**: Anonymous function for WordPress hooks (inline if <=30 LOC)
- **CHK-PHP-15**: NO debug code in production (`var_dump`, `print_r`, `error_log`)


---


## JS Checklist (15 items) - CHK-JS-01 to CHK-JS-15

**Source:** `.deutschfuns/docs/instructions-jsdoc-codestyle/99-quick-reference.md`

### File Structure and Naming (4 items)

- **CHK-JS-01**: File name kebab-case (`quiz-handler.js`, NOT `quizHandler.js`)
- **CHK-JS-02**: File size <100 LOC (modularize if exceeded)
- **CHK-JS-03**: PHP enqueues ONLY 1 init file, modules import via ES6
- **CHK-JS-04**: Prefix `de-` or `fong-` for main modules

### Module Export/Import (4 items)

- **CHK-JS-05**: Named exports (NO default export)
- **CHK-JS-06**: Static imports at top (dynamic import only when needed)
- **CHK-JS-07**: Object Literal Pattern preferred (`export const FongXxxAPI = {...}`)
- **CHK-JS-08**: No circular imports

### Code Quality (4 items)

- **CHK-JS-09**: JSDoc minimal: `@param`, `@returns` - NO redundant info
- **CHK-JS-10**: No dead code (unused functions/variables)
- **CHK-JS-11**: No hardcode to pass unit test
- **CHK-JS-12**: Error handling with try-catch (async functions)

### Debug and Performance (3 items)

- **CHK-JS-13**: Debug logs format: `console.log('%c[FONG DEBUG] msg', 'color: #0073aa;')`
- **CHK-JS-14**: Remove ALL debug logs before production
- **CHK-JS-15**: Cache jQuery selectors (`const $container = $('#id');`)


---


## CSS Checklist (15 items) - CHK-CSS-01 to CHK-CSS-15

**Source:** `.deutschfuns/docs/instructions-css-codestyle.md`

### File Structure (4 items)

- **CHK-CSS-01**: Each page has ONLY 1 CSS init file (enqueue)
- **CHK-CSS-02**: Component files have `_` prefix (`_component-name.css`)
- **CHK-CSS-03**: Components import via `@import` in init file, NOT enqueued separately
- **CHK-CSS-04**: File size <100 LOC (split if exceeded)

### Naming Convention (4 items)

- **CHK-CSS-05**: BEM with `fong-` prefix (`.fong-component__element--modifier`)
- **CHK-CSS-06**: Block: `.fong-{component-name}`
- **CHK-CSS-07**: Element: `.fong-{component-name}__{element-name}`
- **CHK-CSS-08**: Modifier: `.fong-{component-name}--{modifier-name}`

### Code Quality (4 items)

- **CHK-CSS-09**: Low selector specificity (0,0,1,0 to 0,0,2,0), avoid `!important`
- **CHK-CSS-10**: Properties organized: Layout -> Visual -> Typography -> Interaction
- **CHK-CSS-11**: CSS Custom Properties for colors/spacing (`:root { --fong-* }`)
- **CHK-CSS-12**: Mobile-first responsive (`min-width` media queries)

### Performance and Accessibility (3 items)

- **CHK-CSS-13**: Focus states for accessibility (`:focus`, `:focus-visible`)
- **CHK-CSS-14**: No unused CSS rules
- **CHK-CSS-15**: Version caching (filemtime) when enqueue


---


## BEM/HTML Checklist (10 items) - CHK-BEM-01 to CHK-BEM-10

**Source:** `.deutschfuns/docs/instructions-html-dom-BEM-codestyle.md`

### Block (4 items)

- **CHK-BEM-01**: ID/class starts with `de-` prefix (namespace)
- **CHK-BEM-02**: Block name: `de-{block-name}` (kebab-case)
- **CHK-BEM-03**: Block is independent, reusable unit
- **CHK-BEM-04**: One element belongs to ONE block only

### Element (3 items)

- **CHK-BEM-05**: Element: `de-{block}__element` (double underscore)
- **CHK-BEM-06**: Element NEVER standalone (always belongs to block)
- **CHK-BEM-07**: Element name describes function, NOT position

### Modifier (3 items)

- **CHK-BEM-08**: Modifier: `de-{block}--{modifier}` (double hyphen)
- **CHK-BEM-09**: Modifier used WITH block/element class (not replacing)
- **CHK-BEM-10**: State modifiers: `--disabled`, `--active`, `--loading`, `--error`


---


## Review Methodology

### Step-by-Step (MANDATORY)

```
1. IDENTIFY file type(s) -> select checklist(s)
2. READ file(s) with Read tool (NEVER review without reading)
3. FOR each file:
   a. Run applicable checklist item by item
   b. Mark PASS / FAIL / WARNING with line number evidence
   c. Count score: X/N items (Y%)
4. AGGREGATE results across all files
5. PRODUCE summary table
6. LIST all FAIL items with fix suggestions
7. VERDICT: APPROVED / APPROVED WITH ISSUES / REJECTED
```

### Scoring

| Score | Rating | Verdict |
|-------|--------|---------|
| 90-100% | Excellent | APPROVED |
| 75-89% | Good | APPROVED WITH MINOR ISSUES |
| 60-74% | Needs Work | APPROVED WITH MAJOR ISSUES |
| <60% | Poor | REJECTED - Rework Required |

### Evidence Format

```
- [x] **CHK-PHP-01**: PASS - Line 1 correct header format
- [ ] **CHK-PHP-06**: FAIL - Line 37: `function_exists('de_get_user')` -> internal function, remove check
- [x] **CHK-PHP-09**: PASS - Line 52: uses `de_time()` correctly
```


---


## Output Location

**Default folder:** `.fong/docs/code-reviews/`

**File Naming Convention:**

| Pattern | Example |
|---------|---------|
| `REVIEW-{YYYY-MM-DD}_{scope}-{reviewer}.md` | `REVIEW-2026-01-26_PR3-OTP-Module-Fong.md` |
| `{YYYY-MM-DD}-{scope}-Checklist-Review.md` | `2026-01-26-PR3-Email-OTP-Full-Checklist-Review.md` |


---


## Output File Template (TIENG VIET CO DAU)

```markdown
---
title: "Code Review: {Scope}"
subtitle: "Deutschfuns LMS Code Quality Review"
author: "Fong (AI-assisted)"
date: "{YYYY-MM-DD}"
version: "1.0.0"
---


## Code Review: {Scope}


**Methodology:** Checklist-based review theo Deutschfuns LMS codestyle standards

**Source:** {PR URL / file path / branch name}


---


## Summary


| Category | Items | Pass | Fail | Score |
|----------|-------|------|------|-------|
| PHP Codestyle | 15 | N | N | N% |
| JS Codestyle | 15 | N | N | N% |
| CSS Codestyle | 15 | N | N | N% |
| BEM/HTML | 10 | N | N | N% |
| **TOTAL** | **N** | **N** | **N** | **N%** |


**Rating: {Rating}**

**Verdict: {APPROVED / APPROVED WITH ISSUES / REJECTED}**


---


## PHP Review (if applicable)


| # | Item | Status | Evidence |
|---|------|--------|----------|
| CHK-PHP-01 | Compact Header | PASS/FAIL | {line number + detail} |
| CHK-PHP-02 | File Size | PASS/FAIL | {N LOC} |
| ... | ... | ... | ... |


**Score: N/15 (N%)**


---


## JS Review (if applicable)

{Same format as PHP}


---


## CSS Review (if applicable)

{Same format as PHP}


---


## BEM/HTML Review (if applicable)

{Same format as PHP}


---


## Issues Found


### Critical (Must Fix)

1. **{File}:{Line}** - {Description} - {Fix suggestion}

### Warning (Should Fix)

1. **{File}:{Line}** - {Description} - {Fix suggestion}


---


## Conclusion

{Summary paragraph}

**Verdict: {APPROVED / APPROVED WITH ISSUES / REJECTED}**
```


---


## Pre-Prompt Template (RCIFENI-O)

Khi user invoke `/wp-php-code-review`, AI PHAI output response theo format sau:

```
`Think BIG, DO small steps`, `step by step`. Best effort to `get things done`. ULTRATHINK activated.
Skill: /wp-php-code-review
{YYYY-MM-DD HH:MM:SS} (+07)

# 1. Role:
Senior Code Reviewer + Deutschfuns LMS Standards Expert

# 2. Context:
Target: {files/PR/module to review}
Standards: Deutschfuns LMS codestyle (PHP 15 items, JS 15 items, CSS 15 items, BEM 10 items)
Output: .md review report with checklist matrix

# 3. Instructions:
1. READ all codestyle docs (PHP, JS, CSS, BEM quick references)
2. READ target file(s) with Read tool
3. Run checklist item by item with evidence
4. Score each category
5. List all FAIL items with fix suggestions
6. Produce verdict

# 4. Output Format:
- File: REVIEW-{date}_{scope}.md in .fong/docs/code-reviews/
- Checklist matrix with PASS/FAIL + line numbers
- Summary table with scores
- Issues list with fix suggestions

# 5. Cautions:
- anti: Review without reading file first
- anti: Skip checklist items
- anti: PASS without evidence (line number required)
- anti: Mental math for LOC count (use wc -l)
- anti: Assume patterns without checking

# 6. OKR:
O: Review {target} against Deutschfuns LMS standards
KR1: Run ALL applicable checklist items with evidence
KR2: Score >= calculated accurately
KR3: All FAIL items have fix suggestions
```


---


## AI Workflow

**STEP 0 - MANDATORY FIRST (Zero Skip):**

```
Read tool -> .deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/99-quick-reference.md
Read tool -> .deutschfuns/docs/instructions-jsdoc-codestyle/99-quick-reference.md
Read tool -> .deutschfuns/docs/instructions-css-codestyle.md (Quick Checklist)
Read tool -> .deutschfuns/docs/instructions-html-dom-BEM-codestyle.md (Quick Checklist)
```

1. **Print Pre-Prompt** -> Show RCIFENI-O template above
2. **Identify scope** -> Single file / PR / Module
3. **Read target files** -> NEVER review without reading
4. **Detect file types** -> Select applicable checklists
5. **Run checklists** -> Item by item with evidence
6. **Aggregate scores** -> Summary table
7. **List issues** -> Critical + Warning with fix suggestions
8. **Verdict** -> APPROVED / WITH ISSUES / REJECTED
9. **Write report** -> Save to `.fong/docs/code-reviews/`

**Quick Validation Commands (use Bash):**

```bash
# PHP header check
head -1 file.php

# LOC count (NEVER mental math)
wc -l file.php

# Pattern violations
rg -n "function_exists.*de_" file.php
rg -n "\btime\(\)" file.php
rg -n "current_time" file.php
rg -n "get_userdata" file.php
rg -n "var_dump\|print_r\|error_log" file.php

# JS checks
rg -n "export default" file.js
rg -n "console\.log" file.js

# CSS checks
rg -n "!important" file.css
```


---


## Checklist (12 items - MANDATORY)

- [ ] Codestyle docs read (PHP/JS/CSS/BEM)?
- [ ] Target file(s) read with Read tool?
- [ ] File type(s) detected correctly?
- [ ] ALL applicable checklist items run?
- [ ] Every PASS has line number evidence?
- [ ] Every FAIL has file:line + description?
- [ ] LOC counted with `wc -l` (not mental math)?
- [ ] Scores calculated correctly?
- [ ] Summary table produced?
- [ ] All FAIL items have fix suggestions?
- [ ] Verdict determined by score threshold?
- [ ] Report saved to `.fong/docs/code-reviews/`?


---


## Cross-References

| Context | File |
|---------|------|
| **PHP Codestyle Index** | `.deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/00-instructions-phpdoc-codestyle-deutschfuns-pattern.md` |
| **PHP Quick Reference** | `.deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/99-quick-reference.md` |
| **PHP Validation Checklist** | `.deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/02-enhanced-validation-checklist/` |
| **PHP Validation Tools** | `.deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/04-validation-tools-automation/` |
| **JS Codestyle Index** | `.deutschfuns/docs/instructions-jsdoc-codestyle/00-instructions-jsdoc-codestyle.md` |
| **JS Quick Reference** | `.deutschfuns/docs/instructions-jsdoc-codestyle/99-quick-reference.md` |
| **CSS Codestyle** | `.deutschfuns/docs/instructions-css-codestyle.md` |
| **HTML/BEM Codestyle** | `.deutschfuns/docs/instructions-html-dom-BEM-codestyle.md` |
| **Refactor Check** | `.deutschfuns/docs/refactoring/refactor-check-DRY-SSoT-SOLID-SRP.md` |
| **Code Review Examples** | `.fong/docs/code-reviews/` |
| **File Naming Conventions** | `.deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/17-file-naming-conventions.md` |
| **Time Architecture** | `.deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/29-time-architecture.md` |
| **Module V3 Template** | `.deutschfuns/docs/instructions-phpdoc-codestyle-deutschfuns-pattern/05-standard-module-v3-template/` |


---


## Additional Resources


### Reference Files

- **`references/checklist-quick-ref.md`** - All checklists in one page
- **`references/validation-commands.md`** - Bash commands for automated checks


### Example Files

- **`examples/review-php-helper.md`** - PHP helper file review example
- **`examples/review-pr-multi-file.md`** - Multi-file PR review example
