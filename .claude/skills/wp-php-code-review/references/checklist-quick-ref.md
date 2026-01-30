---
title: "Code Review Checklist Quick Reference"
date: "2026-01-26"
parent: "../SKILL.md"
---


## PHP Checklist (15 items)

| # | Item | Check |
|---|------|-------|
| CHK-PHP-01 | Header: `<?php declare(strict_types=1); if (!defined('ABSPATH')) { exit; }` | `head -1` |
| CHK-PHP-02 | File size: helper <=150 LOC, class <=200 LOC | `wc -l` |
| CHK-PHP-03 | Naming: `{func}-helper.php`, `{hook}-hook.php`, `{Class}-class.php` | Filename |
| CHK-PHP-04 | Prefix: `de_` functions, `DE_` constants | `rg "function "` |
| CHK-PHP-05 | NO `require_once` for internal files | `rg "require_once"` |
| CHK-PHP-06 | NO `function_exists()` for internal `de_*` | `rg "function_exists.*de_"` |
| CHK-PHP-07 | `function_exists()` ONLY for external plugins | Manual |
| CHK-PHP-08 | NO circular dependencies | Trace imports |
| CHK-PHP-09 | `de_time()` not `time()`, `de_time_mysql()` not `current_time()` | `rg "\btime\(\)"` |
| CHK-PHP-10 | NO `get_userdata()` in loops | `rg "get_userdata"` |
| CHK-PHP-11 | NO hardcode to pass unit test | Manual |
| CHK-PHP-12 | NO HTML in functions (use templates) | Manual |
| CHK-PHP-13 | PHPDoc minimal: `@param`, `@return` only | Manual |
| CHK-PHP-14 | Anonymous function for WP hooks (<=30 LOC inline) | Manual |
| CHK-PHP-15 | NO debug code: `var_dump`, `print_r`, `error_log` | `rg "var_dump\|print_r"` |


## JS Checklist (15 items)

| # | Item | Check |
|---|------|-------|
| CHK-JS-01 | Kebab-case filename | Filename |
| CHK-JS-02 | File size <100 LOC | `wc -l` |
| CHK-JS-03 | PHP enqueues ONLY 1 init file | Trace PHP |
| CHK-JS-04 | Prefix `de-` or `fong-` for main modules | Filename |
| CHK-JS-05 | Named exports (NO default export) | `rg "export default"` |
| CHK-JS-06 | Static imports at top | `rg "^import"` |
| CHK-JS-07 | Object Literal Pattern preferred | Manual |
| CHK-JS-08 | No circular imports | Trace imports |
| CHK-JS-09 | JSDoc minimal: `@param`, `@returns` | Manual |
| CHK-JS-10 | No dead code | Manual |
| CHK-JS-11 | No hardcode to pass unit test | Manual |
| CHK-JS-12 | Error handling with try-catch (async) | Manual |
| CHK-JS-13 | Debug log format: `%c[FONG DEBUG]` | `rg "console.log"` |
| CHK-JS-14 | No debug logs in production | `rg "console.log"` |
| CHK-JS-15 | Cache jQuery selectors | Manual |


## CSS Checklist (15 items)

| # | Item | Check |
|---|------|-------|
| CHK-CSS-01 | 1 CSS init file per page | Trace enqueue |
| CHK-CSS-02 | Component files have `_` prefix | Filename |
| CHK-CSS-03 | Components via `@import`, NOT separate enqueue | Trace PHP |
| CHK-CSS-04 | File size <100 LOC | `wc -l` |
| CHK-CSS-05 | BEM with `fong-` prefix | `rg "\.fong-"` |
| CHK-CSS-06 | Block: `.fong-{name}` | Manual |
| CHK-CSS-07 | Element: `.fong-{name}__{element}` | Manual |
| CHK-CSS-08 | Modifier: `.fong-{name}--{mod}` | Manual |
| CHK-CSS-09 | Low specificity, no `!important` | `rg "!important"` |
| CHK-CSS-10 | Properties: Layout -> Visual -> Typo -> Interaction | Manual |
| CHK-CSS-11 | CSS Custom Properties `--fong-*` | `rg "--fong-"` |
| CHK-CSS-12 | Mobile-first (`min-width`) | `rg "min-width"` |
| CHK-CSS-13 | Focus states for a11y | `rg ":focus"` |
| CHK-CSS-14 | No unused CSS rules | Manual |
| CHK-CSS-15 | Version caching (filemtime) | Trace PHP |


## BEM/HTML Checklist (10 items)

| # | Item | Check |
|---|------|-------|
| CHK-BEM-01 | `de-` prefix for ID/class | `rg 'class="de-'` |
| CHK-BEM-02 | Block: `de-{block-name}` (kebab-case) | Manual |
| CHK-BEM-03 | Block is independent, reusable | Manual |
| CHK-BEM-04 | Element belongs to ONE block | Manual |
| CHK-BEM-05 | Element: `de-{block}__element` (double underscore) | Manual |
| CHK-BEM-06 | Element never standalone | Manual |
| CHK-BEM-07 | Element name = function, not position | Manual |
| CHK-BEM-08 | Modifier: `de-{block}--{modifier}` (double hyphen) | Manual |
| CHK-BEM-09 | Modifier WITH base class, not replacing | Manual |
| CHK-BEM-10 | State modifiers: `--disabled`, `--active`, etc. | Manual |
