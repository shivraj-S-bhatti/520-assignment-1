#!/usr/bin/env python3
"""
Generate baseline coverage summary table with interpretations.
"""

import json
import pathlib
import csv
from typing import Dict, List

def generate_interpretation(problem: str, line_cov: float, branch_cov: float, tests_passed: int) -> str:
    """Generate one-line interpretation of coverage results."""
    interpretations = []
    
    if line_cov < 50:
        interpretations.append("low line coverage")
    elif line_cov < 80:
        interpretations.append("moderate line coverage")
    else:
        interpretations.append("high line coverage")
    
    if branch_cov == 0:
        interpretations.append("no branch coverage measured")
    elif branch_cov < 50:
        interpretations.append("low branch coverage")
    elif branch_cov < 80:
        interpretations.append("moderate branch coverage")
    else:
        interpretations.append("high branch coverage")
    
    # Problem-specific interpretations
    if problem == "normalize_path" and line_cov < 100:
        interpretations.append("untested edge cases for path normalization")
    elif problem == "evaluate_rpn" and line_cov < 100:
        interpretations.append("some error paths untested")
    elif problem == "parse_csv_line" and line_cov < 100:
        interpretations.append("some CSV parsing edge cases untested")
    elif problem == "top_k_frequent" and line_cov < 100:
        interpretations.append("some error handling paths untested")
    
    if branch_cov == 0 and line_cov > 0:
        interpretations.append("branch coverage not measured (may need --cov-branch flag)")
    
    return "; ".join(interpretations)

def main():
    """Generate baseline coverage summary."""
    BASE = pathlib.Path(__file__).resolve().parents[1]
    results_file = BASE / "coverage_reports" / "baseline" / "baseline_results.json"
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Generate summary table
    summary_rows = []
    for result in sorted(results, key=lambda x: x['problem']):
        problem = result['problem']
        line_cov = result['line_coverage']
        branch_cov = result['branch_coverage']
        tests_passed = result['tests_passed']
        tests_failed = result.get('tests_failed', 0)
        
        interpretation = generate_interpretation(problem, line_cov, branch_cov, tests_passed)
        
        summary_rows.append({
            'problem': problem,
            'line_coverage': f"{line_cov:.1f}%",
            'branch_coverage': f"{branch_cov:.1f}%",
            'tests_passed': tests_passed,
            'tests_failed': tests_failed,
            'interpretation': interpretation
        })
    
    # Write CSV
    csv_file = BASE / "baseline_coverage_summary.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['problem', 'line_coverage', 'branch_coverage', 'tests_passed', 'tests_failed', 'interpretation'])
        writer.writeheader()
        writer.writerows(summary_rows)
    
    # Write Markdown
    md_file = BASE / "baseline_coverage_summary.md"
    with open(md_file, 'w') as f:
        f.write("# Baseline Coverage Summary\n\n")
        f.write("## Overview\n\n")
        f.write("This table shows baseline code coverage for all 10 problems from Exercise 1.\n\n")
        f.write("| Problem | Line Coverage | Branch Coverage | Tests Passed | Tests Failed | Interpretation |\n")
        f.write("|---------|---------------|-----------------|--------------|--------------|-----------------|\n")
        
        for row in summary_rows:
            f.write(f"| {row['problem']} | {row['line_coverage']} | {row['branch_coverage']} | "
                   f"{row['tests_passed']} | {row['tests_failed']} | {row['interpretation']} |\n")
        
        f.write("\n## Notes\n\n")
        f.write("- Line coverage measures the percentage of executable lines covered by tests.\n")
        f.write("- Branch coverage measures the percentage of conditional branches (if/else, loops) covered.\n")
        f.write("- Branch coverage may show 0% if not properly configured; this will be addressed in Part 2.\n")
        f.write("- All baseline tests should pass; failures indicate issues with the solution code.\n")
    
    print("Baseline Coverage Summary Generated")
    print("=" * 50)
    print(f"CSV: {csv_file}")
    print(f"Markdown: {md_file}")
    print()
    print("Summary Table:")
    print("-" * 50)
    print(f"{'Problem':<25} {'Line %':<10} {'Branch %':<12} {'Tests':<10} {'Status':<10}")
    print("-" * 50)
    
    for row in summary_rows:
        status = "✓ PASS" if row['tests_failed'] == 0 else "✗ FAIL"
        print(f"{row['problem']:<25} {row['line_coverage']:<10} {row['branch_coverage']:<12} "
              f"{row['tests_passed']:<10} {status:<10}")
    
    return summary_rows

if __name__ == "__main__":
    main()
