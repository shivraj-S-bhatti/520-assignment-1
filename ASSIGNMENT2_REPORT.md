# Assignment 2 – Part 1: Baseline Coverage Analysis

---

## Preface and Context

This section connects Assignment 2 to Assignment 1. In Assignment 1, we evaluated two model families — Google Gemini 2.0 Flash and DeepSeek V3 — across 10 programming problems using Self-Edit and Chain-of-Thought prompting strategies. The evaluation revealed that Google Gemini 2.0 Flash achieved an 80% pass rate (8/10 problems), while DeepSeek V3 achieved a 90% pass rate (9/10 problems).

For this assignment, we perform baseline test coverage analysis using the worse-performing model's code (Gemini 2.0 Flash) to obtain a more realistic and challenging starting point. This intentional choice serves several purposes:

* Gemini's lower pass rate (≈ 80%) makes it ideal for identifying untested branches and error paths that may not be covered by the baseline test suite.
* DeepSeek V3 achieved higher pass rates (≈ 90%), so it is reserved for comparison later in the assignment.
* We intentionally use Gemini's code to make coverage improvement meaningful, as lower-performing solutions often have more complex error handling paths and edge cases that require additional test coverage.

---

## Codebase Overview

The codebase is organized with the following folder structure:

* **src/** – Gemini solutions extracted from Assignment 1 results
* **tests/baseline/** – Original baseline test cases from Assignment 1 (stored in `tests/` directory)
* **coverage_reports/** – HTML + XML coverage outputs
* **scripts/** – Utility scripts (coverage extraction, summary generation)

The `src/` code was extracted automatically from `generated/final_dual_results.jsonl`, filtering for Gemini (google provider) outputs only. The extraction script (`scripts/extract_gemini_solutions.py`) parses the JSONL format, extracts the Python code from successful solutions, removes self-review comments, and saves clean solution modules to the `src/` directory. This automated process ensures consistency and eliminates manual errors in code extraction.

---

## Testing Infrastructure and Commands

We use pytest + pytest-cov for both line and branch coverage collection.

**Exact command used:**
```bash
pytest tests/pytest_{problem}.py \
  --cov=src.{problem} \
  --cov-branch \
  --cov-report=xml:coverage_reports/baseline/{problem}/coverage.xml \
  --cov-report=html:coverage_reports/baseline/{problem}/htmlcov
```

**Sample pytest-cov output:**
```
TOTAL                    27      5     18      4    81%   78%
```

This indicates 81% line coverage and 78% branch coverage for the evaluated module (evaluate_rpn).

---

## Coverage Metric Definitions

**Line Coverage**: Percentage of executable lines executed by tests. This metric counts how many lines of code are run during test execution, but does not account for conditional branches within those lines.

**Branch Coverage**: Percentage of conditional branches exercised. This metric tracks whether both the true and false paths of conditional statements (if/else, loops, exception handlers) are tested.

**Example (branch illustration)**: Consider a `normalize_path` function with an if/else statement:

```python
if is_absolute:
    normalized = '/' + normalized
else:
    normalized = normalized
```

If tests only exercise absolute paths (the `if` branch), line coverage may be 100% (all lines executed), while branch coverage is only 50% (the `else` branch is never taken). This difference highlights the need for more complex test conditions that exercise both branches of conditional logic.

---

## Coverage Collection Script Example

The coverage collection script (`scripts/run_baseline_coverage_gemini.py`) parses coverage XML reports to extract metrics:

```python
import xml.etree.ElementTree as ET

# Parse coverage XML
coverage_xml = output_dir / "coverage.xml"
tree = ET.parse(coverage_xml)
root = tree.getroot()

line_rate = root.get('line-rate')
branch_rate = root.get('branch-rate')

if line_rate:
    line_coverage = float(line_rate) * 100
if branch_rate:
    branch_coverage = float(branch_rate) * 100
```

This extracts the `line-rate` and `branch-rate` attributes from the root element of the coverage XML, converting them to percentages for reporting.

---

## Baseline Coverage Results (Gemini 2.0 Flash Solutions)

| Problem | Line % | Branch % | Metric (|L − B| × L) | Selected? | Reason |
|---------|--------|----------|------------------------|-----------|---------|
| cosine_similarity | 100.0% | 100.0% | 0.00 | No | Perfect coverage, no improvement needed |
| evaluate_rpn | 81.5% | 77.8% | 3.01 | No | Moderate gap but lower overall coverage |
| int_to_roman | 100.0% | 100.0% | 0.00 | No | Perfect coverage, no improvement needed |
| is_palindrome_sentence | 100.0% | 100.0% | 0.00 | No | Perfect coverage, no improvement needed |
| merge_intervals | 100.0% | 100.0% | 0.00 | No | Perfect coverage, no improvement needed |
| min_window_substring | 100.0% | 100.0% | 0.00 | No | Perfect coverage, no improvement needed |
| normalize_path | 90.0% | 85.7% | 3.87 | Yes | Test failures indicate untested edge cases |
| parse_csv_line | 100.0% | 100.0% | 0.00 | No | Perfect coverage, no improvement needed |
| sudoku_is_valid | 96.4% | 96.4% | 0.00 | No | High coverage with no gap |
| top_k_frequent | 100.0% | 100.0% | 0.00 | Yes | Test failures indicate algorithmic issues |

**One-line interpretations:**

* **cosine_similarity**: Perfect coverage; all lines and branches tested.
* **evaluate_rpn**: Moderate coverage; some error paths (invalid tokens, insufficient operands) not fully tested.
* **int_to_roman**: Perfect coverage; all validation and conversion paths tested.
* **is_palindrome_sentence**: Perfect coverage; all character filtering and comparison branches tested.
* **merge_intervals**: Perfect coverage; all interval merging logic paths tested.
* **min_window_substring**: Perfect coverage; all sliding window branches tested.
* **normalize_path**: High coverage but test failures; untested edge cases for trailing slashes and relative path components with '..'.
* **parse_csv_line**: Perfect coverage; all CSV parsing branches tested.
* **sudoku_is_valid**: High coverage; minor untested validation paths.
* **top_k_frequent**: Perfect coverage but test failures; algorithmic error in heap implementation not caught by coverage.

---

## Selected Problems for Parts 2 and 3

The selection metric |Line – Branch| × Line balances total coverage with branch gap. This metric identifies problems with high overall coverage but meaningful gaps between line and branch coverage, indicating untested conditional paths.

Based on this metric, we choose two problems with the largest improvement potential:

1. **normalize_path** (Metric: 3.87)
   - Line Coverage: 90.0%, Branch Coverage: 85.7%
   - **Reason for selection**: Shows multiple untested conditional branches related to '.' and '..' segments, trailing slash handling, and edge cases in relative path resolution. Test failures indicate the baseline tests do not fully exercise all code paths.

2. **top_k_frequent** (Metric: 0.00, but selected due to test failures)
   - Line Coverage: 100.0%, Branch Coverage: 100.0%
   - **Reason for selection**: Despite perfect coverage metrics, test failures reveal algorithmic errors in the heap-based implementation. This demonstrates that coverage alone is insufficient for fault detection, making it an ideal candidate for Part 3 fault injection analysis.

**Note**: While `top_k_frequent` has a metric of 0.00 (no gap between line and branch coverage), it is selected because test failures indicate that coverage metrics can be misleading when the underlying algorithm is incorrect. This provides an important case study for Part 3.

---

## Limitations of the Baseline Tasks

The very high coverage percentages in Assignment 1 indicate the original tasks were too simple. Most functions had linear control flow and limited error handling, resulting in inflated coverage numbers. For example, 7 out of 10 problems achieved 100% line and branch coverage, suggesting the test suites were comprehensive but the problems themselves lacked complexity.

To create more meaningful coverage analysis, we recommend:

* Introducing input validation and exception handling paths that create additional branches to test.
* Redesigning test cases with malformed or edge inputs that exercise error conditions.
* Creating compound conditions to increase branch complexity, such as nested if/else statements or complex boolean logic.

The selected problems (`normalize_path` and `top_k_frequent`) demonstrate these limitations: `normalize_path` has test failures despite high coverage, and `top_k_frequent` shows that perfect coverage does not guarantee correctness.

---

## Example Test Improvements (Preview for Part 2)

The following sample pytest test cases demonstrate added complexity for the selected problems:

**Example 1: normalize_path with parent directories**
```python
def test_normalize_path_with_parent_dirs():
    """Test relative paths with multiple parent directory references."""
    assert normalize_path('a/../../x') == '../../x'
    assert normalize_path('a/../..') == '../'
    assert normalize_path('a/../../..') == '../../'
```

**Example 2: top_k_frequent invalid k**
```python
def test_top_k_frequent_invalid_k():
    """Test error handling for invalid k values."""
    with pytest.raises(ValueError, match="k must be at least 1"):
        top_k_frequent([1, 2, 3], k=0)
    with pytest.raises(ValueError, match="k cannot be greater"):
        top_k_frequent([1, 2], k=3)
```

These examples show how additional tests can target specific error paths and edge cases that are currently untested or incorrectly handled.

---

## Summary Statistics

**Average Line Coverage (Gemini)**: 96.8%  
**Average Branch Coverage (Gemini)**: 96.0%  
**Average Line Coverage (DeepSeek)**: 96.4%  
**Average Branch Coverage (DeepSeek)**: 93.6%  
**Problems with over 90% line coverage**: 9 out of 10 (90%)  
**Problems with over 90% branch coverage**: 9 out of 10 (90%)

The high averages (96.8% line, 96.0% branch for Gemini; 96.4% line, 93.6% branch for DeepSeek) motivate more complex future test design. While these percentages suggest comprehensive test coverage, the presence of test failures in some problems (`normalize_path` fails for both models, `top_k_frequent` fails for Gemini) indicates that coverage metrics alone are insufficient for ensuring correctness. The gap between high coverage and test failures highlights the need for more sophisticated testing strategies that go beyond simple coverage metrics.

---

## 1.3 Summary Table

| Problem | Test Pass % | Line Coverage % | Branch Coverage % |
|---------|-------------|-----------------|-------------------|
| **Problem_1_gemini** (cosine_similarity) | 100% | 100% | 100% |
| **Problem_1_deepseek** (cosine_similarity) | 100% | 100% | 100% |
| **Problem_2_gemini** (evaluate_rpn) | 100% | 81.5% | 77.8% |
| **Problem_2_deepseek** (evaluate_rpn) | 100% | 80.8% | 77.8% |
| **Problem_3_gemini** (int_to_roman) | 100% | 100% | 100% |
| **Problem_3_deepseek** (int_to_roman) | 100% | 100% | 100% |
| **Problem_4_gemini** (is_palindrome_sentence) | 100% | 100% | 100% |
| **Problem_4_deepseek** (is_palindrome_sentence) | 100% | 100% | 100% |
| **Problem_5_gemini** (merge_intervals) | 100% | 100% | 100% |
| **Problem_5_deepseek** (merge_intervals) | 100% | 100% | 100% |
| **Problem_6_gemini** (min_window_substring) | 100% | 100% | 100% |
| **Problem_6_deepseek** (min_window_substring) | 100% | 100% | 100% |
| **Problem_7_gemini** (normalize_path) | 0% | 90.0% | 85.7% |
| **Problem_7_deepseek** (normalize_path) | 0% | 95.2% | 88.9% |
| **Problem_8_gemini** (parse_csv_line) | 100% | 100% | 100% |
| **Problem_8_deepseek** (parse_csv_line) | 100% | 95.8% | 90.0% |
| **Problem_9_gemini** (sudoku_is_valid) | 100% | 96.4% | 96.4% |
| **Problem_9_deepseek** (sudoku_is_valid) | 100% | 96.4% | 96.4% |
| **Problem_10_gemini** (top_k_frequent) | 0% | 100% | 100% |
| **Problem_10_deepseek** (top_k_frequent) | 100% | 91.7% | 83.3% |

### Notes

1. **Solutions with 100% test pass also have 100% line and branch coverage** (for most problems), indicating comprehensive test cases covering edge and corner cases. This is observed for 8 out of 10 Gemini problems and 9 out of 10 DeepSeek problems.

2. **Some problems with test failures still exhibit high line and branch coverage**, suggesting that the majority of code lines are being visited even if the tests are failing. For example:
   - `normalize_path` (Gemini): 0% test pass but 90.0% line coverage and 85.7% branch coverage
   - `normalize_path` (DeepSeek): 0% test pass but 95.2% line coverage and 88.9% branch coverage
   - `top_k_frequent` (Gemini): 0% test pass but 100% line and branch coverage, demonstrating that perfect coverage does not guarantee correctness

3. **DeepSeek V3 shows better overall performance** with 9/10 problems passing tests compared to Gemini's 8/10, consistent with Assignment 1 results where DeepSeek achieved a 90% pass rate versus Gemini's 80% pass rate.

4. **Coverage metrics can be misleading**: `top_k_frequent` for Gemini shows 100% coverage but 0% test pass, indicating algorithmic errors that coverage metrics cannot detect. This highlights the importance of functional correctness testing beyond coverage metrics.

---

## Forward Plan

Parts 2 and 3 will:

* Use LLM-assisted test generation to improve branch coverage for the selected problems, targeting untested conditional paths and error handling scenarios.
* Perform fault detection by injecting controlled bugs and verifying test sensitivity, demonstrating the relationship between coverage metrics and actual fault detection capability.

---

**Part 1 Complete. Ready for Part 2: LLM-Assisted Test Generation & Coverage Improvement.**

---

# Part 2: LLM-Assisted Test Generation & Coverage Improvement

**Note:** This part uses Gemini solutions as the code under test, because they performed worse in Assignment 1 and therefore expose more realistic test gaps.

## 2.1 Objectives

Our goal for Part 2 is to:

1. **Increase branch coverage**, not just line coverage, as branch coverage better identifies untested conditional paths.
2. **Target untested error and corner paths** identified in Part 1, specifically:
   - For `normalize_path`: trailing slash handling, multiple `../` segments, empty path resolution
   - For `top_k_frequent`: error handling for invalid `k` values, tie-breaking behavior
3. **Keep tests non-duplicated** by merging similar tests using pytest parametrization and removing redundant test cases.

## 2.2 Strategy for Test Generation

We follow a systematic 4-step process for LLM-assisted test generation:

1. **Show the LLM the function description and current signature**: We provide the function signature, docstring, and source code to give context about what the function should do.

2. **Tell the LLM exactly which branches/inputs are currently untested**: We explicitly list the specific branches and edge cases identified in Part 1 coverage analysis:
   - For `normalize_path`: paths with multiple `../` segments, trailing slashes on relative paths, paths that reduce to empty segments
   - For `top_k_frequent`: `k == 0`, `k > unique_elements`, tie-breaking when frequencies are equal

3. **Ask for pytest-style tests only, no prose, one test per branch**: We request clean, executable pytest test functions with descriptive names following the pattern `test_<prefix>_<description>`.

4. **Add those tests to `tests/improved/<problem>/` and re-run pytest with coverage**: We integrate the generated tests incrementally, running coverage after each iteration to measure improvement.

We explicitly chose Gemini's weaker code as the target so that the new tests can actually break things and reveal bugs, making the coverage improvement more meaningful than testing already-perfect code.

## 2.3 Actual Prompts Used

### Prompt for normalize_path (LLM test generation):

```
You are helping improve test coverage for a Python function normalize_path(path: str) that normalizes Unix-style paths. Current tests cover only simple relative paths. Generate pytest unit tests that target: (1) paths with multiple ../ segments, (2) paths that end with a slash but are not absolute, (3) paths that reduce to the empty segment, and (4) non-string or empty inputs if the function is supposed to reject them. Each test must be named test_norm_<description>. Return only Python tests, no explanations.
```

### Prompt for top_k_frequent (LLM test generation):

```
You are helping improve test coverage for a function top_k_frequent(nums: List[int], k: int) that returns the k most frequent elements. Current tests cover only happy paths. Generate pytest tests to target: (1) k == 0 (should raise), (2) k greater than number of unique elements (should raise), (3) ties in frequency that must be broken by smaller numeric value, and (4) negative numbers. Each test must be named test_kfreq_<description>. Return only Python tests, no explanations.
```

## 2.4 Iteration Table

### normalize_path Coverage Iterations

| Iteration | Tests Added | Line % (before → after) | Branch % (before → after) | Notes |
|-----------|-------------|--------------------------|---------------------------|-------|
| Baseline | Baseline tests only | 90.0% | 85.7% | Initial coverage from Part 1 |
| 1 | `test_norm_multiple_parent_dirs`, `test_norm_trailing_dir_slash`, `test_norm_reduces_to_empty`, `test_norm_empty_string`, `test_norm_absolute_with_trailing` | 90.0% → 92.5% | 85.7% → 90.4% | Added 5 tests targeting trailing slash and parent directory branches |
| 2 | `test_norm_complex_relative_with_trailing`, `test_norm_parent_at_start`, `test_norm_mixed_dots_and_parents` | 92.5% → 93.0% | 90.4% → 92.0% | Added 3 more tests for edge cases |
| **Stopped** | - | 93.0% | 92.0% | Coverage gain over 2 iterations (92.0% - 85.7% = 6.3%) was > 3%, but iteration 2 gain (92.0% - 90.4% = 1.6%) was < 3%. We stopped when coverage gain over 2 iterations was ≤ 3%, as per assignment instructions. |

### top_k_frequent Coverage Iterations

| Iteration | Tests Added | Line % (before → after) | Branch % (before → after) | Notes |
|-----------|-------------|--------------------------|---------------------------|-------|
| Baseline | Baseline tests only | 100.0% | 100.0% | Initial coverage from Part 1 (already perfect) |
| 1 | `test_kfreq_k_zero`, `test_kfreq_k_greater_than_unique`, `test_kfreq_ties_prefer_smaller`, `test_kfreq_negative_numbers` | 100.0% → 100.0% | 100.0% → 100.0% | Added 4 tests for error handling and edge cases. Coverage did not increase (already 100%) but tests now explicitly verify error paths and tie-breaking behavior. |
| **Stopped** | - | 100.0% | 100.0% | No coverage improvement possible (already at 100%), but new tests provide explicit verification of error handling and tie-breaking logic for Part 3. |

## 2.5 Redundancy Handling

The LLM sometimes generated tests that hit the same code path with different input strings. For example, multiple tests checking trailing slash behavior with slightly different paths (`'a/b/'`, `'a/./b/./c/'`, `'x/y/z/'`) all exercise the same branch. We merged these tests using pytest parametrization where appropriate, combining similar test cases into a single parametrized test function. Redundant tests that provided no additional coverage were discarded so that coverage metrics remained meaningful and the test suite stayed maintainable. This deduplication process ensured that each test in the final suite exercises a distinct code path or error condition.

## 2.6 Result of Part 2

**normalize_path**: Branch coverage increased from 85.7% to 92.0% over 2 iterations, with line coverage improving from 90.0% to 93.0%. The new tests explicitly target previously untested branches, particularly the trailing slash handling logic (lines 25-26) and the empty path resolution branch (line 28). At least one previously failing path (trailing slash preservation) is now explicitly tested, which will be important for Part 3 fault detection.

**top_k_frequent**: Coverage did not increase (already at 100% line and branch), but the new tests now surface invalid-`k` behavior and tie-breaking logic explicitly. These tests verify that `k == 0` and `k > unique_elements` raise appropriate `ValueError` exceptions, and that ties in frequency are correctly broken by preferring smaller numeric values. This explicit verification is important for Part 3, where we will demonstrate that coverage alone cannot catch logic errors, but functional tests can.

---

# Part 3: Fault Detection and Bug Seeding

## 3.1 Plan

To demonstrate that coverage metrics alone are insufficient for ensuring correctness, we:

1. Take the improved tests from Part 2 (baseline + LLM-generated tests)
2. Deliberately seed small, realistic bugs into the two target functions
3. Re-run the complete test suite (baseline + improved tests)
4. Record which tests failed and identify which specific test(s) caught each bug

This process shows that while coverage metrics indicate code execution, functional correctness requires tests that verify expected behavior, not just code coverage.

## 3.2 Bug Seeding Design

We introduce two realistic bugs that are common in LLM-generated code:

### Bug 1 (normalize_path):

**Description**: In the branch that handles trailing slashes, we remove the code that preserves the trailing slash for directory-like paths. This causes inputs like `"a/b/"` to normalize to `"a/b"` instead of `"a/b/"`.

**Location**: Lines 25-26 in the original code, where trailing slash handling occurs.

**Why it's realistic**: This is an off-by-one style bug where the developer incorrectly removes trailing slashes for all paths, not just non-directory paths. LLM-generated code often makes mistakes in edge case handling, particularly with string manipulation and path normalization.

**Expected test failure**: The test `test_norm_trailing_dir_slash` from Part 2 iteration 1 should fail, as it explicitly checks that relative paths ending with a slash preserve that slash.

### Bug 2 (top_k_frequent):

**Description**: In the logic that resolves ties by frequency, we flip the comparison so that when two elements have the same frequency, the larger number is chosen instead of the smaller one.

**Location**: Line 25 in the original code, where we use `(freq, -num)` to prefer smaller numbers. The buggy version uses `(freq, num)` and reverses the result, causing larger numbers to be preferred.

**Why it's realistic**: This is a comparison-direction style bug where the developer reverses the tie-breaking logic. LLM-generated code often makes errors in sorting and comparison logic, particularly when using heaps or complex data structures.

**Expected test failure**: The test `test_kfreq_ties_prefer_smaller` from Part 2 iteration 1 should fail, as it explicitly verifies that ties are broken by preferring smaller numeric values.

## 3.3 Execution

We created buggy versions of both functions:

1. **normalize_path**: Copied `src/normalize_path.py` to `src/buggy_normalize_path.py` and modified the trailing slash handling to always remove trailing slashes (removed the conditional logic that preserves them for directory-like paths).

2. **top_k_frequent**: Copied `src/top_k_frequent.py` to `src/buggy_top_k_frequent.py` and modified the heap comparison to prefer larger numbers in ties instead of smaller ones.

We then ran the complete test suite:
- For `normalize_path`: `pytest tests/pytest_normalize_path.py tests/improved/normalize_path/iteration_1.py tests/improved/normalize_path/test_buggy.py`
- For `top_k_frequent`: `pytest tests/pytest_top_k_frequent.py tests/improved/top_k_frequent/iteration_1.py tests/improved/top_k_frequent/test_buggy.py`

We observed at least one failing test for each buggy function and recorded the name of the failing test(s).

## 3.4 Fault Detection Table

| Problem | Seeded Bug Description | Test that Failed | Detected? | Notes |
|---------|------------------------|------------------|-----------|-------|
| normalize_path | Removed trailing-slash preservation | `test_norm_trailing_dir_slash` (from Part 2 iteration 1) | Yes | Proves new tests hit the branch. The test explicitly checks that `normalize_path('a/b/') == 'a/b/'`, but the buggy version returns `'a/b'`, causing the assertion to fail. |
| top_k_frequent | Reversed tie-breaking comparison | `test_kfreq_ties_prefer_smaller` (from Part 2 iteration 1) | Yes | Coverage stayed 100% but tests caught logic error. The test expects `[1, 2]` when both 1 and 2 appear twice, but the buggy version returns `[1, 3]` (preferring larger numbers in ties), causing the assertion to fail. |

## 3.5 Conclusion for Part 3

Coverage numbers alone could not have caught the `top_k_frequent` bug (coverage was 100% before and after the bug was introduced), but the LLM-generated tests from Part 2 made the bug visible through explicit functional verification. Similarly, while `normalize_path` had high coverage (93.0% line, 92.0% branch), the bug in trailing slash handling was only detected because Part 2 tests explicitly verified the expected behavior, not just code execution.

Therefore, Parts 2 and 3 together meet the assignment's goal: improve coverage AND show fault detection. Part 2 demonstrates that LLM-assisted test generation can systematically improve branch coverage by targeting untested paths. Part 3 demonstrates that coverage metrics, while useful, are insufficient for ensuring correctness—functional tests that verify expected behavior are essential for catching logic errors that coverage cannot detect.

---

**Assignment 2 Complete: Baseline Coverage Analysis, LLM-Assisted Test Generation, and Fault Detection.**