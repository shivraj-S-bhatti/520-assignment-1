#!/usr/bin/env python3
"""
Generate summary table with test pass percentage, line coverage, and branch coverage
for both Gemini and DeepSeek solutions.
"""

import subprocess
import pathlib
import json
import xml.etree.ElementTree as ET
import re
from typing import Dict, List

def run_tests_for_problem(problem_name: str, test_file: pathlib.Path, base_dir: pathlib.Path) -> Dict:
    """Run tests for a single problem and count pass/fail."""
    cmd = [
        "python3", "-m", "pytest",
        str(test_file),
        "-v",
        "--tb=no"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(base_dir)
        )
        
        # Parse test results
        output = result.stdout + result.stderr
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for line in output.split('\n'):
            if f'[{problem_name}]' in line or f'test_{problem_name}' in line:
                if 'PASSED' in line:
                    passed_tests += 1
                    total_tests += 1
                elif 'FAILED' in line:
                    failed_tests += 1
                    total_tests += 1
        
        # Also check summary line
        summary_match = re.search(r'(\d+)\s+passed', output)
        if summary_match:
            passed_tests = int(summary_match.group(1))
        
        summary_match = re.search(r'(\d+)\s+failed', output)
        if summary_match:
            failed_tests = int(summary_match.group(1))
        
        total_tests = passed_tests + failed_tests
        pass_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "pass_percentage": round(pass_percentage, 1)
        }
    
    except Exception as e:
        return {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "pass_percentage": 0.0,
            "error": str(e)
        }

def get_coverage_for_problem(problem_name: str, solution_module: str, base_dir: pathlib.Path) -> Dict:
    """Get coverage metrics for a single problem."""
    test_file = base_dir / "tests" / f"pytest_{problem_name}.py"
    output_dir = base_dir / "coverage_reports" / "summary" / problem_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "python3", "-m", "pytest",
        str(test_file),
        f"--cov={solution_module}",
        "--cov-branch",
        "--cov-report=xml:" + str(output_dir / "coverage.xml"),
        "--tb=no"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(base_dir)
        )
        
        # Parse coverage XML
        coverage_xml = output_dir / "coverage.xml"
        line_coverage = 0.0
        branch_coverage = 0.0
        
        if coverage_xml.exists():
            tree = ET.parse(coverage_xml)
            root = tree.getroot()
            
            line_rate = root.get('line-rate')
            branch_rate = root.get('branch-rate')
            
            if line_rate:
                line_coverage = float(line_rate) * 100
            if branch_rate:
                branch_coverage = float(branch_rate) * 100
        
        return {
            "line_coverage": round(line_coverage, 1),
            "branch_coverage": round(branch_coverage, 1)
        }
    
    except Exception as e:
        return {
            "line_coverage": 0.0,
            "branch_coverage": 0.0,
            "error": str(e)
        }

def main():
    """Generate summary table for both Gemini and DeepSeek."""
    BASE = pathlib.Path(__file__).resolve().parents[1]
    
    problems = [
        "cosine_similarity", "evaluate_rpn", "int_to_roman", "is_palindrome_sentence",
        "merge_intervals", "min_window_substring", "normalize_path", "parse_csv_line",
        "sudoku_is_valid", "top_k_frequent"
    ]
    
    print("Generating Summary Table...")
    print("=" * 60)
    
    results = []
    
    for i, problem in enumerate(problems, 1):
        print(f"[{i}/10] Processing {problem}...")
        
        # Gemini results
        gemini_test_file = BASE.parent / "a1" / "tests" / "test_gemini.py"
        gemini_tests = run_tests_for_problem(problem, gemini_test_file, BASE)
        gemini_coverage = get_coverage_for_problem(problem, f"src.{problem}", BASE)
        
        # DeepSeek results
        deepseek_test_file = BASE.parent / "a1" / "tests" / "test_deepseek.py"
        deepseek_tests = run_tests_for_problem(problem, deepseek_test_file, BASE)
        deepseek_coverage = get_coverage_for_problem(problem, f"solutions.{problem}", BASE)
        
        results.append({
            "problem": problem,
            "gemini": {
                "pass_percentage": gemini_tests["pass_percentage"],
                "line_coverage": gemini_coverage["line_coverage"],
                "branch_coverage": gemini_coverage["branch_coverage"]
            },
            "deepseek": {
                "pass_percentage": deepseek_tests["pass_percentage"],
                "line_coverage": deepseek_coverage["line_coverage"],
                "branch_coverage": deepseek_coverage["branch_coverage"]
            }
        })
        
        print(f"  Gemini: {gemini_tests['pass_percentage']:.1f}% pass, {gemini_coverage['line_coverage']:.1f}% line, {gemini_coverage['branch_coverage']:.1f}% branch")
        print(f"  DeepSeek: {deepseek_tests['pass_percentage']:.1f}% pass, {deepseek_coverage['line_coverage']:.1f}% line, {deepseek_coverage['branch_coverage']:.1f}% branch")
    
    # Save to JSON
    results_file = BASE / "summary_table_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"Results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    main()
