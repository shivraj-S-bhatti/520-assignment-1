# Test Commands Guide

## Files Created

- `tests/test_gemini.py` - Tests for Gemini 2.0 Flash solutions (from `src/`)
- `tests/test_deepseek.py` - Tests for DeepSeek V3 solutions (from `solutions/`)

---

## Step 1: Run Pytest Tests (Get PASSED/FAILED Output)

### Run Gemini Tests
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_gemini.py -v
```

### Run DeepSeek Tests
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_deepseek.py -v
```

### Run Both Tests Together
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_gemini.py tests/test_deepseek.py -v
```

**Expected Output**: You'll see test results like:
```
tests/test_gemini.py::test_gemini_solution[cosine_similarity] PASSED [ 10%]
tests/test_gemini.py::test_gemini_solution[evaluate_rpn] PASSED [ 20%]
tests/test_gemini.py::test_gemini_solution[normalize_path] FAILED [ 70%]
...
==== 2 failed, 8 passed in 0.5s ====
```

---

## Step 2: Generate Coverage Reports (Get Coverage Screenshots)

### Option A: Terminal Coverage Report (Quick View)

#### For Gemini Solutions:
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_gemini.py --cov=src --cov-branch --cov-report=term
```

#### For DeepSeek Solutions:
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_deepseek.py --cov=solutions --cov-branch --cov-report=term
```

#### For Both Together:
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_gemini.py tests/test_deepseek.py --cov=src --cov=solutions --cov-branch --cov-report=term
```

**Expected Output**: Terminal table showing:
```
Name                  Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------
src/cosine_similarity.py      11      0      4      0   100%
src/evaluate_rpn.py           27      5     18      4    80%
...
-------------------------------------------------------
TOTAL                     XXX     XX    XXX     XX    86%   93%
```

---

### Option B: HTML Coverage Report (For Screenshots)

#### For Gemini Solutions:
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_gemini.py --cov=src --cov-branch --cov-report=html:coverage_reports/gemini_html
```

Then open the report:
```bash
open coverage_reports/gemini_html/index.html
```

#### For DeepSeek Solutions:
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_deepseek.py --cov=solutions --cov-branch --cov-report=html:coverage_reports/deepseek_html
```

Then open the report:
```bash
open coverage_reports/deepseek_html/index.html
```

#### For Both Together (Combined Report):
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_gemini.py tests/test_deepseek.py --cov=src --cov=solutions --cov-branch --cov-report=html:coverage_reports/combined_html
```

Then open:
```bash
open coverage_reports/combined_html/index.html
```

**Expected Output**: HTML page with:
- Coverage report table showing file-by-file coverage
- Overall coverage percentage (e.g., "Coverage report: 86%")
- Line coverage and branch coverage statistics
- Color-coded coverage indicators

---

### Option C: XML Coverage Report (For Automated Processing)

```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_gemini.py --cov=src --cov-branch --cov-report=xml:coverage_reports/gemini_coverage.xml
pytest tests/test_deepseek.py --cov=solutions --cov-branch --cov-report=xml:coverage_reports/deepseek_coverage.xml
```

---

## Step 3: Combined Command (Tests + Coverage in One)

### Gemini with HTML Report:
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_gemini.py -v --cov=src --cov-branch --cov-report=term --cov-report=html:coverage_reports/gemini_html
```

### DeepSeek with HTML Report:
```bash
cd /Users/apple/Downloads/520/llm-codegen-assignment
pytest tests/test_deepseek.py -v --cov=solutions --cov-branch --cov-report=term --cov-report=html:coverage_reports/deepseek_html
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest tests/test_gemini.py -v` | Run Gemini tests, verbose output |
| `pytest tests/test_deepseek.py -v` | Run DeepSeek tests, verbose output |
| `pytest tests/test_gemini.py --cov=src --cov-branch --cov-report=term` | Terminal coverage for Gemini |
| `pytest tests/test_gemini.py --cov=src --cov-branch --cov-report=html:coverage_reports/gemini_html` | HTML coverage for Gemini |
| `open coverage_reports/gemini_html/index.html` | Open HTML coverage report |

---

## Notes

- The `-v` flag provides verbose output showing each test case
- `--cov-branch` enables branch coverage tracking (important for meaningful metrics)
- HTML reports are best for screenshots as they show detailed tables and percentages
- Terminal reports are useful for quick checks
- XML reports are useful for automated processing and integration with CI/CD

