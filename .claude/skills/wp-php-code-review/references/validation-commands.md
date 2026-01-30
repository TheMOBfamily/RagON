---
title: "Validation Commands Reference"
date: "2026-01-26"
parent: "../SKILL.md"
---


## PHP Validation Commands

```bash
# CHK-PHP-01: Header check
head -1 file.php

# CHK-PHP-02: LOC count
wc -l file.php

# CHK-PHP-04: Prefix check
rg -n "^function " file.php
rg -n "^define\(" file.php

# CHK-PHP-05: require_once violations
rg -n "require_once" file.php

# CHK-PHP-06: function_exists for internal
rg -n "function_exists.*de_" file.php

# CHK-PHP-09: Time function violations
rg -n "\btime\(\)" file.php
rg -n "current_time" file.php

# CHK-PHP-10: Memory leak pattern
rg -n "get_userdata" file.php

# CHK-PHP-15: Debug code
rg -n "var_dump\|print_r\|error_log\|debug_backtrace" file.php
```


## JS Validation Commands

```bash
# CHK-JS-02: LOC count
wc -l file.js

# CHK-JS-05: Default export violation
rg -n "export default" file.js

# CHK-JS-06: Import analysis
rg -n "^import" file.js

# CHK-JS-14: Debug logs
rg -n "console\.(log|debug|info|warn)" file.js
```


## CSS Validation Commands

```bash
# CHK-CSS-04: LOC count
wc -l file.css

# CHK-CSS-09: !important violations
rg -n "!important" file.css

# CHK-CSS-05: BEM prefix check
rg -n "\.(fong|de)-" file.css

# CHK-CSS-12: Responsive approach
rg -n "min-width\|max-width" file.css

# CHK-CSS-13: Accessibility focus states
rg -n ":focus" file.css
```


## Bulk Validation (Multiple Files)

```bash
# Count LOC for all PHP files in a module
find modules/{module}/ -name "*.php" -exec wc -l {} + | sort -n

# Find ALL function_exists violations
rg -n "function_exists.*de_" modules/{module}/

# Find ALL time() violations
rg -n "\btime\(\)" modules/{module}/ --type php

# Find ALL debug code
rg -n "var_dump\|print_r\|error_log" modules/{module}/ --type php

# Find ALL console.log in JS
rg -n "console\.log" modules/{module}/ --type js
```


## PR Diff Review

```bash
# Get changed files
git diff --name-only main...HEAD

# Get PHP changes only
git diff --name-only main...HEAD -- '*.php'

# Get diff with context
git diff main...HEAD -- file.php

# Count LOC per changed file
git diff --name-only main...HEAD | xargs wc -l | sort -n
```
