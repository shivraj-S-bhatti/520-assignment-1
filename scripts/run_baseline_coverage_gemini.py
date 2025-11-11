#!/usr/bin/env python3
"""
Run baseline coverage for all 10 problems using Gemini solutions in src/.
"""

import subprocess
import pathlib
import json
import xml.etree.ElementTree as ET
import re
from typing import Dict

def run_coverage_for_problem(problem_name: str, base_dir: pathlib.Path) -> Dict:
    """Run pytest with coverage for a single problem."""
    test_file = base_dir / "tests" / f"pytest_{problem_name}.py"
    solution_module = f"src.{problem_name}"
    output_dir = base_dir / "coverage_reports" / "baseline" / problem_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run pytest with coverage (including branch coverage)
    cmd = [
        "python3", "-m", "pytest",
        str(test_file),
        f"--cov={solution_module}",
        "--cov-branch",  # Enable branch coverage tracking
        "--cov-report=html:" + str(output_dir / "htmlcov"),
        "--cov-report=xml:" + str(output_dir / "coverage.xml"),
        "--cov-report=term",
        "-v"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(base_dir)
        )
        
        # Parse test results
        tests_passed = 0
        tests_failed = 0
        for line in result.stdout.split('\n'):
            if 'passed' in line.lower() and 'failed' not in line.lower():
                match = re.search(r'(\d+)\s+passed', line)
                if match:
                    tests_passed = int(match.group(1))
            if 'failed' in line.lower():
                match = re.search(r'(\d+)\s+failed', line)
                if match:
                    tests_failed = int(match.group(1))
        
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
            "problem": problem_name,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "line_coverage": round(line_coverage, 2),
            "branch_coverage": round(branch_coverage, 2),
            "success": result.returncode == 0
        }
    
    except Exception as e:
        print(f"Error running coverage for {problem_name}: {e}")
        return {
            "problem": problem_name,
            "tests_passed": 0,
            "tests_failed": 0,
            "line_coverage": 0.0,
            "branch_coverage": 0.0,
            "success": False,
            "error": str(e)
        }

def main():
    """Run baseline coverage for all problems."""
    BASE = pathlib.Path(__file__).resolve().parents[1]
    
    problems = [
        "cosine_similarity", "evaluate_rpn", "int_to_roman", "is_palindrome_sentence",
        "merge_intervals", "min_window_substring", "normalize_path", "parse_csv_line",
        "sudoku_is_valid", "top_k_frequent"
    ]
    
    print("Running Baseline Coverage Analysis (Gemini Solutions)")
    print("=" * 60)
    print()
    
    results = []
    
    for i, problem in enumerate(problems, 1):
        print(f"[{i}/10] Processing {problem}...")
        result = run_coverage_for_problem(problem, BASE)
        results.append(result)
        
        status = "✓" if result["success"] else "✗"
        print(f"  {status} Line: {result['line_coverage']:.1f}%, Branch: {result['branch_coverage']:.1f}%, Tests: {result['tests_passed']} passed")
        print()
    
    # Save results to JSON
    results_file = BASE / "coverage_reports" / "baseline" / "baseline_results.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("=" * 60)
    print("Baseline Coverage Complete!")
    print(f"Results saved to: {results_file}")
    
    # Calculate summary statistics
    total_line = sum(r['line_coverage'] for r in results)
    total_branch = sum(r['branch_coverage'] for r in results)
    avg_line = total_line / len(results)
    avg_branch = total_branch / len(results)
    
    print(f"\nSummary Statistics:")
    print(f"  Average Line Coverage: {avg_line:.1f}%")
    print(f"  Average Branch Coverage: {avg_branch:.1f}%")
    
    return results

if __name__ == "__main__":
    main()
