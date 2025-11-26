#!/usr/bin/env python3
"""
Run coverage iterations for Part 2.
Collects coverage before and after adding LLM-generated tests.
"""

import subprocess
import pathlib
import xml.etree.ElementTree as ET
import json
from typing import Dict, List

def get_coverage(problem: str, solution_module: str, test_files: List[pathlib.Path], base_dir: pathlib.Path) -> Dict:
    """Get coverage for a problem with given test files."""
    output_dir = base_dir / "coverage_reports" / "iterations" / problem
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build pytest command
    cmd = [
        "python3", "-m", "pytest",
        f"--cov={solution_module}",
        "--cov-branch",
        "--cov-report=xml:" + str(output_dir / "coverage.xml"),
        "--tb=no",
        "-q"
    ]
    
    # Add test files
    for test_file in test_files:
        if test_file.exists():
            cmd.append(str(test_file))
    
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
    """Run coverage iterations."""
    BASE = pathlib.Path(__file__).resolve().parents[1]
    
    problems = {
        "normalize_path": {
            "module": "src.normalize_path",
            "baseline_test": BASE / "tests" / "pytest_normalize_path.py",
            "iterations": [
                BASE / "tests" / "improved" / "normalize_path" / "iteration_1.py",
                BASE / "tests" / "improved" / "normalize_path" / "iteration_2.py",
            ]
        },
        "top_k_frequent": {
            "module": "src.top_k_frequent",
            "baseline_test": BASE / "tests" / "pytest_top_k_frequent.py",
            "iterations": [
                BASE / "tests" / "improved" / "top_k_frequent" / "iteration_1.py",
            ]
        }
    }
    
    results = {}
    
    for problem, config in problems.items():
        print(f"\n{'='*60}")
        print(f"Coverage Iterations for {problem}")
        print(f"{'='*60}\n")
        
        problem_results = []
        
        # Baseline (before LLM tests)
        baseline_tests = [config["baseline_test"]]
        baseline_cov = get_coverage(problem, config["module"], baseline_tests, BASE)
        problem_results.append({
            "iteration": 0,
            "tests": ["baseline"],
            "line": baseline_cov["line_coverage"],
            "branch": baseline_cov["branch_coverage"]
        })
        print(f"Baseline: {baseline_cov['line_coverage']:.1f}% line, {baseline_cov['branch_coverage']:.1f}% branch")
        
        # Iteration 1
        iter1_tests = baseline_tests + [config["iterations"][0]]
        iter1_cov = get_coverage(problem, config["module"], iter1_tests, BASE)
        problem_results.append({
            "iteration": 1,
            "tests": ["baseline", "iteration_1"],
            "line": iter1_cov["line_coverage"],
            "branch": iter1_cov["branch_coverage"]
        })
        print(f"Iteration 1: {iter1_cov['line_coverage']:.1f}% line, {iter1_cov['branch_coverage']:.1f}% branch")
        
        # Iteration 2 (if exists)
        if len(config["iterations"]) > 1:
            iter2_tests = iter1_tests + [config["iterations"][1]]
            iter2_cov = get_coverage(problem, config["module"], iter2_tests, BASE)
            problem_results.append({
                "iteration": 2,
                "tests": ["baseline", "iteration_1", "iteration_2"],
                "line": iter2_cov["line_coverage"],
                "branch": iter2_cov["branch_coverage"]
            })
            print(f"Iteration 2: {iter2_cov['line_coverage']:.1f}% line, {iter2_cov['branch_coverage']:.1f}% branch")
        
        results[problem] = problem_results
    
    # Save results
    results_file = BASE / "coverage_iterations_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    main()
