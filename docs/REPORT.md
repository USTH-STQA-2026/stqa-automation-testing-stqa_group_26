# PROJECT REPORT: AUTOMATED WEB UI TESTING

**System:** Library Book Borrowing Management ABC (https://stqa.rbc.vn)
**Subject:** Software Testing and Quality Assurance (STQA)
**Execution Team:** Group 26 (Class: 252ICT2012.L1)

---

## 👥 1. Member List & Task Allocation Matrix

The system recognizes the fair contribution of all 4 members through Work Breakdown Structure (WBS) and cross-checking:

| No. | Full Name | Role | Automation Code Tasks | Theory & Responsibility Tasks | 
| :--- | :--- | :--- | :--- | :--- | 
| 1 | Nguyễn Huy Quang | Team Leader | Completed all tests/test_borrow_return.py (TC-08, TC-09, TC-10) | Git Setup, BT4 (FSM Book Lifecycle), Final Code Review | 
| 2 | Nguyễn Phan Hồng Anh | QA Lead | Completed all tests/test_general.py (TC-11, TC-12) | Gatekeeper (Review PR, time.sleep() traps, Weak Oracle), BT5 & BT9, Compiled REPORT.md | 
| 3 | Nguyễn Tiến Dũng | Member 3 | Completed tests/test_login.py (TC-02, TC-03) | Researched test-accounts.md, applied Data-driven technique, Documented test data, writing REPORT.md | 
| 4 | Đặng Quang Nam Anh | Member 4 | Assisted in test execution and verification scripts | Supported REPORT.md formatting, cross-checked issues, tracked tasks | 

---

## 📊 2. Test Execution Report

The automated test suite covers the core system requirements defined in `SRS-library-system.md`, mapping functional criteria to strict automated validation scripts. The regression test suite consists of **15 comprehensive test scenarios** targeting core business logic flows.

### 2.1. Overview Statistics

* **Total designed scenarios:** 15
* **Number of PASSED scenarios:** 15
* **Number of FAILED scenarios:** 0
* **Success Rate:** 100%
* **Execution Framework:** Pytest + Playwright Python (Synchronous API)

### 2.2. Detailed Results per Scenario

Every test execution is configured with an automated artifact capture system to record visual proof inside the `screenshots/` directory immediately upon reaching the **Propagation** phase.

| TC Code | Test Scenario Name | Status | Artifacts | Technical Notes |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Login success with valid credentials | ✅ PASSED | `login_success.png` | Verified application state via successful extraction of `TEST_DISPLAY_NAME` from the Flutter Semantics Tree. |
| **TC-02** | Login fail – wrong password | ✅ PASSED | `login_fail_wrong_password.png` | Validated application denial and boundary error string `"Mật khẩu không đúng."`. |
| **TC-03** | Login fail – wrong email | ✅ PASSED | `login_fail_wrong_email.png` | Validated identity exception and checked system response for error message `"Không tìm thấy thành viên."`. |
| **TC-04** | Login fail – empty fields | ✅ PASSED | `login_fail_empty_fields.png` | Negative boundary test; validated system constraint string `"Vui lòng nhập email và mật khẩu."` when both inputs are null. |
| **TC-05** | Login fail – empty email | ✅ PASSED | `login_fail_empty_email.png` | Validated missing identity handler when password field is present but email is left blank. |
| **TC-06** | Login fail – empty password | ✅ PASSED | `login_fail_empty_password.png` | Validated missing credential handler when email field is present but password is left blank. |
| **TC-07** | Search book by name – results found | ✅ PASSED | `test_search_book_by_name.png` | Searched query `"Flutter"`. Asserted structural visibility of matching elements utilizing custom dynamic semantic locators. |
| **TC-08** | Search book – no results | ✅ PASSED | `test_search_book_no_result.png` | Validated zero-state handler with non-existent query string. Checked that book grid components dropped to `count() == 0`. |
| **TC-09** | Filter books by category | ✅ PASSED | `test_filter_by_category.png` | Iterated through all rendered book elements using a bounded loop to confirm strict classification under category `"Công nghệ"`. |
| **TC-10** | Search book by author name | ✅ PASSED | `test_search_by_author.png` | Extracted semantics layout to match strict pattern criteria targeting author keyword `"Nguyễn Minh Đức"`. |
| **TC-11** | Borrow an available book | ✅ PASSED | `test_borrow_book.png` | Simulates user click sequence on dynamic modal view templates. Validated successful mutation to status `"Đang mượn"`. |
| **TC-12** | View borrowed books list | ✅ PASSED | `test_view_borrowed_books.png` | Navigated to tab interaction element `"Mượn / Trả"`. Confirmed persistent visual display of current active user transactions. |
| **TC-13** | Return a borrowed book | ✅ PASSED | `test_return_book.png` | Executed transactional data reversal loop. Verified state transition to `"Đã trả"` via complete DOM tree text aggregation. |
| **TC-14** | Logout success | ✅ PASSED | `test_logout.png` | Validated session clearance. Combined explicit true assertion for login elements with a negative constraint check against user-exclusive layouts. |
| **TC-15** | Switch language to English | ✅ PASSED | `test_switch_language_to_english.png` | Triggered immediate localization update via internationalization UI toggle element (`EN`). Verified text translation to target language layout. |

---

## 🛠 3. Technical Solutions & Test Harness Infrastructure Optimization

Addressing the specific characteristics of the **Flutter Web (CanvasKit renderer)** application, the team thoroughly applied advanced infrastructure techniques to achieve perfect optimization criteria:

1. **Complete removal of `time.sleep()` anti-pattern:** Based on research results, the team clearly recognized that `time.sleep()` creates an indeterminate state (non-deterministic), unnecessarily slowing down the CI/CD infrastructure. The team implemented an event-driven **Smart Wait** (`wait_for_flutter()`) function in `conftest.py` operating on a polling mechanism to synchronize precisely when the Flutter Semantics Tree (`flt-semantics`) finishes re-rendering or when specific text/selectors are safely attached.
2. **Elimination of LLM-proposed `wait_for_timeout()` traps:** During development, the team proactively audited and stripped out all volatile `page.wait_for_timeout()` functions suggested by AI tools. Replacing these hardcoded delays with dynamic, condition-based synchronization guarantees the **deterministic nature** of the test suite and prevents flaky executions in headless CI environments.
3. **Adaptive Universal Automation Strategy (`WebTech`):** To avoid rigid scripting, the team designed a decoupled layer leveraging `detect_technology(page)`. Utilities like `smart_fill()` and `smart_click()` automatically adapt their execution logic: if the engine detects CanvasKit, it initializes accessibility trees via `enable_flutter_semantics()` and interacts via `flt-text-editing-host`; otherwise, it gracefully falls back to native HTML locators (`get_by_label`, `get_by_placeholder`).
4. **Building a Strong Oracle Strategy:** To increase the Revealability of the RIPR model, all checkpoints (`assert`) do not stop at just checking the URL or crash-free status (Null/Weak Oracle). The team implemented extraction and aggregation of all text strings exposed on the accessibility layer into a unified searchable text context to simultaneously validate precise state mutations and SRS error criteria via:
```python
sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
assert "Expected message from SRS" in sem_text


```


## 🛠 4. AI Usage Declaration

## Tooling & Quality Control (AI Utilization)

While **Gemini** was incorporated to accelerate boilerplate drafting and Playwright library syntax referencing, the technical integrity of the project was strictly governed by the team.

All AI-assisted outputs underwent a rigorous human review process:
1. **Validation:** Assertions were manually validated and standardized to match the exact criteria in `SRS-library-system.md`.
2. **Refinement:** The team engineered custom solutions for unique target behaviors, discarding incorrect AI-generated selectors that failed due to the framework's **CanvasKit** architecture.
3. **Optimization:** Standard anti-patterns like `wait_for_timeout()` were entirely removed by team members to guarantee test suite determinism and prevent flakiness.
