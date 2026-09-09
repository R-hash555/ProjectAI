# Mandatory Code Review & Verification Checklist for AI-Generated Code

## Overview
This checklist was derived empirically from defects actually introduced by AI coding assistants during evaluation across 10 software engineering development tasks. All AI-generated code MUST pass this checklist before PR approval.

---

## 1. Security & Compliance Verification
- [ ] **SQL Injection Prevention**: Verify all SQL queries use parameterized arguments (`?`, `%s`, `$1`) instead of f-string/string concatenation formatting. (Derived from `TASK-07` defect).
- [ ] **Secret Hardcoding**: Check for hardcoded API keys, JWT secrets, database passwords, or private certificates in AI code snippets.
- [ ] **License & Code Scraps**: Confirm no GPL/copyleft licensed snippet comments or proprietary copyright headers were hallucinated.

## 2. Concurrency & Resource Safety
- [ ] **Thread-Safety & Mutex Locks**: Verify that shared mutable state (counters, cache stores, lists) is explicitly guarded by `threading.Lock()` or async mutexes. (Derived from `TASK-02` and `TASK-05` defects).
- [ ] **Memory Leak & Unsubscription**: Confirm event listeners, RxJS streams, or callbacks implement explicit cleanup and unsubscription mechanisms. (Derived from `TASK-10` defect).

## 3. Logic & Boundary Checks
- [ ] **Numeric Precision**: Verify floating-point currency or financial operations are explicitly rounded (`round()`) or use Decimal data types. (Derived from `TASK-04` defect).
- [ ] **TTL & Stale Data Expiration**: Ensure timestamp expiry checks occur on data retrieval (`get()`), not just background cleanup. (Derived from `TASK-02` defect).
- [ ] **Input Sanitization**: Confirm string inputs are stripped and validated against empty/whitespace-only values (`if not name.strip()`). (Derived from `TASK-01` defect).

---

## 4. Verification Execution Protocol
1. **Never accept unreviewed AI code**: Treat AI code as untrusted submission from a junior contractor.
2. **Run Independent Tests**: Execute pytest suite written independently of the AI prompt/implementation.
3. **Log Review Time**: Always log review and debugging time separately from generation time to compute honest productivity metrics.
