# Baseline Coverage Summary

## Overview

This table shows baseline code coverage for all 10 problems from Exercise 1.

| Problem | Line Coverage | Branch Coverage | Tests Passed | Tests Failed | Interpretation |
|---------|---------------|-----------------|--------------|--------------|-----------------|
| cosine_similarity | 100.0% | 100.0% | 1 | 0 | high line coverage; high branch coverage |
| evaluate_rpn | 80.8% | 77.8% | 1 | 0 | high line coverage; moderate branch coverage; some error paths untested |
| int_to_roman | 100.0% | 100.0% | 1 | 0 | high line coverage; high branch coverage |
| is_palindrome_sentence | 100.0% | 100.0% | 1 | 0 | high line coverage; high branch coverage |
| merge_intervals | 100.0% | 100.0% | 1 | 0 | high line coverage; high branch coverage |
| min_window_substring | 100.0% | 100.0% | 1 | 0 | high line coverage; high branch coverage |
| normalize_path | 95.2% | 88.9% | 0 | 1 | high line coverage; high branch coverage; untested edge cases for path normalization |
| parse_csv_line | 95.8% | 90.0% | 1 | 0 | high line coverage; high branch coverage; some CSV parsing edge cases untested |
| sudoku_is_valid | 96.4% | 96.4% | 1 | 0 | high line coverage; high branch coverage |
| top_k_frequent | 91.7% | 83.3% | 1 | 0 | high line coverage; high branch coverage; some error handling paths untested |

## Notes

- Line coverage measures the percentage of executable lines covered by tests.
- Branch coverage measures the percentage of conditional branches (if/else, loops) covered.
- Branch coverage may show 0% if not properly configured; this will be addressed in Part 2.
- All baseline tests should pass; failures indicate issues with the solution code.
