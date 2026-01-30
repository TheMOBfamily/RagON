---
title: "Example: Multi-File PR Review"
date: "2026-01-26"
parent: "../SKILL.md"
---


## Review Example: PR Multi-File Review


### Target

PR #1: Email Verification Module (6 commits)
Files changed: 30 PHP, 8 JS


### Summary

| Category | Items | Pass | Fail | Score |
|----------|-------|------|------|-------|
| PHP Codestyle | 15 | 13 | 2 | 87% |
| JS Codestyle | 15 | 14 | 1 | 93% |
| **TOTAL** | **30** | **27** | **3** | **90%** |


**Rating: Excellent (90%)**

**Verdict: APPROVED WITH MINOR ISSUES**


---


### PHP Review - Aggregated


| # | Item | Status | Evidence |
|---|------|--------|----------|
| CHK-PHP-01 | Compact Header | PASS | All 30 files correct |
| CHK-PHP-02 | File Size | PASS | 0 files > 150 LOC |
| CHK-PHP-03 | Naming | FAIL | 3 files use `-model.php` instead of `-CRUD-class.php` |
| CHK-PHP-04 | Prefix | PASS | All functions use `de_` |
| CHK-PHP-05 | No require_once | PASS | 0 violations |
| CHK-PHP-06 | No function_exists internal | PASS | 0 violations |
| CHK-PHP-07 | External function_exists | PASS | LearnDash checked via wrapper |
| CHK-PHP-08 | No circular deps | PASS | Clean dependency graph |
| CHK-PHP-09 | Time functions | PASS | All use `de_time()` |
| CHK-PHP-10 | No get_userdata loop | PASS | Uses JOIN query |
| CHK-PHP-11 | No hardcode test | PASS | Logic genuine |
| CHK-PHP-12 | No HTML in function | PASS | Templates separated |
| CHK-PHP-13 | PHPDoc minimal | PASS | Minimal tags |
| CHK-PHP-14 | Anonymous hooks | FAIL | 2 hooks with named functions >30 LOC |
| CHK-PHP-15 | No debug code | PASS | Clean |


**Score: 13/15 (87%)**


---


### JS Review - Aggregated


| # | Item | Status | Evidence |
|---|------|--------|----------|
| CHK-JS-01 | Kebab-case | PASS | All 8 files correct |
| CHK-JS-02 | File size <100 | PASS | Max 87 LOC |
| CHK-JS-03 | Single init enqueue | PASS | Only init file enqueued |
| CHK-JS-04 | Prefix | PASS | All `de-` prefixed |
| CHK-JS-05 | Named exports | PASS | No default exports |
| CHK-JS-06 | Static imports | PASS | All at top |
| CHK-JS-07 | Object Literal | PASS | Pattern used |
| CHK-JS-08 | No circular imports | PASS | Clean graph |
| CHK-JS-09 | JSDoc minimal | PASS | Correct |
| CHK-JS-10 | No dead code | PASS | Clean |
| CHK-JS-11 | No hardcode test | PASS | Genuine logic |
| CHK-JS-12 | Error handling | PASS | try-catch on async |
| CHK-JS-13 | Debug format | PASS | `%c[FONG DEBUG]` |
| CHK-JS-14 | No debug prod | FAIL | `otp-timer.js:45` has `console.log` |
| CHK-JS-15 | Cache selectors | PASS | `$container` cached |


**Score: 14/15 (93%)**


---


### Issues Found


#### Warning (Should Fix)

1. **modules/otp/includes/models/otp-data-model.php** - Rename to `Otp-Data-CRUD-class.php` per naming convention
2. **modules/otp/includes/models/otp-log-model.php** - Same rename needed
3. **modules/otp/includes/models/otp-config-model.php** - Same rename needed
4. **modules/otp/includes/hooks/verify-email-hook.php:52** - Extract callback to named function (>30 LOC)
5. **modules/otp/includes/hooks/resend-otp-hook.php:38** - Same extraction needed
6. **modules/otp/src/public/js/otp-timer.js:45** - Remove `console.log` before production


---


### Conclusion

Module dat chat luong tot. 3 van de nho can fix truoc merge:
naming convention cho model files, hook callback extraction, va xoa debug log.

**Verdict: APPROVED WITH MINOR ISSUES**
