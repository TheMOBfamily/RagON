---
title: "Example: PHP Helper File Review"
date: "2026-01-26"
parent: "../SKILL.md"
---


## Review Example: PHP Helper File


### Target

File: `modules/otp/includes/helpers/de_generate_otp_code-helper.php`


### PHP Checklist Review

| # | Item | Status | Evidence |
|---|------|--------|----------|
| CHK-PHP-01 | Compact Header | PASS | Line 1: `<?php declare(strict_types=1); if (!defined('ABSPATH')) { exit; }` |
| CHK-PHP-02 | File Size | PASS | 42 LOC < 150 LOC limit |
| CHK-PHP-03 | Naming Convention | PASS | `de_generate_otp_code-helper.php` follows `{function}-helper.php` |
| CHK-PHP-04 | Prefix | PASS | Function `de_generate_otp_code()` uses `de_` prefix |
| CHK-PHP-05 | No require_once | PASS | 0 instances found |
| CHK-PHP-06 | No function_exists internal | PASS | 0 violations |
| CHK-PHP-07 | External function_exists | N/A | No external dependencies |
| CHK-PHP-08 | No circular deps | PASS | Single helper, no imports |
| CHK-PHP-09 | Time functions | PASS | Line 28: uses `de_time()` |
| CHK-PHP-10 | No get_userdata in loop | PASS | No loops with user data |
| CHK-PHP-11 | No hardcode for test | PASS | Logic is genuine |
| CHK-PHP-12 | No HTML in function | PASS | Pure logic, no HTML |
| CHK-PHP-13 | PHPDoc minimal | PASS | Only `@param` and `@return` |
| CHK-PHP-14 | Anonymous hooks | N/A | No hooks in helper |
| CHK-PHP-15 | No debug code | PASS | 0 debug statements |


**Score: 13/13 applicable (100%)**

**Verdict: APPROVED**
