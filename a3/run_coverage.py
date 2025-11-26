#!/usr/bin/env python3
"""
Run coverage analysis for Assignment 3 spec-guided tests.
"""

import subprocess
import pathlib
import json
import xml.etree.ElementTree as ET
from typing import Dict

def get_coverage(problem: str, test_files: list, base_dir: pathlib.Path) -> Dict:
    """Get coverage for a problem with given test files."""
    output_dir = base_dir / "a3" / "coverage_reports" / problem
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build pytest command
    # Need to run from a2/ directory to test a2/src/
    a2_dir = base_dir / "a2"
    cmd = [
        "python3", "-m", "pytest",
        f"--cov=src.{problem}",
        "--cov-branch",
        "--cov-report=xml:" + str(output_dir / "coverage.xml"),
        "--cov-report=html:" + str(output_dir / "htmlcov"),
        "--tb=no",
        "-q"
    ]
    
    # Add test files - convert to relative paths from a2/
    for test_file in test_files:
        if test_file.exists():
            # Convert absolute path to relative from a2/
            if test_file.is_relative_to(base_dir):
                rel_path = test_file.relative_to(base_dir)
            else:
                rel_path = test_file
            cmd.append(f"../{rel_path}" if str(rel_path).startswith("tests") or str(rel_path).startswith("a3") else str(rel_path))
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(a2_dir)  # Run from a2/ so src imports work
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
            "problem": problem,
            "line_coverage": round(line_coverage, 2),
            "branch_coverage": round(branch_coverage, 2),
            "success": result.returncode == 0
        }
    
    except Exception as e:
        print(f"Error running coverage for {problem}: {e}")
        return {
            "problem": problem,
            "line_coverage": 0.0,
            "branch_coverage": 0.0,
            "success": False,
            "error": str(e)
        }

def main():
    """Run coverage for both problems."""
    BASE = pathlib.Path(__file__).resolve().parents[1]
    
    # Baseline coverage from A2
    baseline = {
        "normalize_path": {"line": 90.0, "branch": 85.7},
        "evaluate_rpn": {"line": 81.5, "branch": 77.8}
    }
    
    results = {}
    
    # normalize_path
    print("Running coverage for normalize_path...")
    norm_tests = [
        BASE / "tests" / "test_normalize_path.py",  # Baseline
        BASE / "a3" / "tests" / "spec_guided" / "normalize_path" / "test_spec_norm.py"  # Spec-guided
    ]
    norm_result = get_coverage("normalize_path", norm_tests, BASE)
    results["normalize_path"] = {
        "baseline": baseline["normalize_path"],
        "new": norm_result,
        "improvement": {
            "line": norm_result["line_coverage"] - baseline["normalize_path"]["line"],
            "branch": norm_result["branch_coverage"] - baseline["normalize_path"]["branch"]
        }
    }
    print(f"  Baseline: {baseline['normalize_path']['line']}% line, {baseline['normalize_path']['branch']}% branch")
    print(f"  New: {norm_result['line_coverage']}% line, {norm_result['branch_coverage']}% branch")
    print(f"  Improvement: +{results['normalize_path']['improvement']['line']:.1f}% line, +{results['normalize_path']['improvement']['branch']:.1f}% branch")
    
    # evaluate_rpn
    print("\nRunning coverage for evaluate_rpn...")
    rpn_tests = [
        BASE / "tests" / "test_evaluate_rpn.py",  # Baseline
        BASE / "a3" / "tests" / "spec_guided" / "evaluate_rpn" / "test_spec_rpn.py"  # Spec-guided
    ]
    rpn_result = get_coverage("evaluate_rpn", rpn_tests, BASE)
    results["evaluate_rpn"] = {
        "baseline": baseline["evaluate_rpn"],
        "new": rpn_result,
        "improvement": {
            "line": rpn_result["line_coverage"] - baseline["evaluate_rpn"]["line"],
            "branch": rpn_result["branch_coverage"] - baseline["evaluate_rpn"]["branch"]
        }
    }
    print(f"  Baseline: {baseline['evaluate_rpn']['line']}% line, {baseline['evaluate_rpn']['branch']}% branch")
    print(f"  New: {rpn_result['line_coverage']}% line, {rpn_result['branch_coverage']}% branch")
    print(f"  Improvement: +{results['evaluate_rpn']['improvement']['line']:.1f}% line, +{results['evaluate_rpn']['improvement']['branch']:.1f}% branch")
    
    # Save results
    results_file = BASE / "a3" / "coverage_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {results_file}")
    
    return results

if __name__ == "__main__":
    main()

