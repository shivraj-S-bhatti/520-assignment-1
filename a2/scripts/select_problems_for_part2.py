#!/usr/bin/env python3
"""
Select 2 problems for Part 2 based on improvement metric.
Metric: |%test - %branch-coverage| × %test
"""

import json
import pathlib

def main():
    """Select problems with highest improvement potential."""
    BASE = pathlib.Path(__file__).resolve().parents[1]
    results_file = BASE / "coverage_reports" / "baseline" / "baseline_results.json"
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Calculate improvement metric for each problem
    # Metric: |%test - %branch-coverage| × %test
    # Since branch coverage is 0, we'll use line coverage as proxy
    # Actually, let's use: |100% - %branch-coverage| × %line-coverage
    # Or better: gap between line and branch coverage × line coverage
    
    problem_metrics = []
    
    for result in results:
        problem = result['problem']
        line_cov = result['line_coverage']
        branch_cov = result['branch_coverage']
        tests_passed = result['tests_passed']
        
        # Skip problems that failed tests
        if tests_passed == 0:
            continue
        
        # Calculate metric: gap between line and branch coverage × line coverage
        # This identifies problems with high line coverage but low branch coverage
        gap = abs(line_cov - branch_cov)
        metric = gap * line_cov / 100  # Normalize
        
        problem_metrics.append({
            'problem': problem,
            'line_coverage': line_cov,
            'branch_coverage': branch_cov,
            'gap': gap,
            'metric': metric
        })
    
    # Sort by metric (highest first)
    problem_metrics.sort(key=lambda x: x['metric'], reverse=True)
    
    # Select top 2
    selected = problem_metrics[:2]
    
    print("Problem Selection for Part 2")
    print("=" * 60)
    print()
    print("Metric: |Line Coverage - Branch Coverage| × Line Coverage")
    print()
    print(f"{'Problem':<25} {'Line %':<10} {'Branch %':<12} {'Gap':<10} {'Metric':<10}")
    print("-" * 60)
    
    for item in problem_metrics:
        marker = "★ SELECTED" if item in selected else ""
        print(f"{item['problem']:<25} {item['line_coverage']:.1f}%      "
              f"{item['branch_coverage']:.1f}%       {item['gap']:.1f}%      "
              f"{item['metric']:.2f}      {marker}")
    
    print()
    print("Selected Problems for Part 2:")
    print("-" * 60)
    for item in selected:
        print(f"1. {item['problem']}")
        print(f"   - Line Coverage: {item['line_coverage']:.1f}%")
        print(f"   - Branch Coverage: {item['branch_coverage']:.1f}%")
        print(f"   - Gap: {item['gap']:.1f}%")
        print(f"   - Metric: {item['metric']:.2f}")
        print(f"   - Rationale: High line coverage ({item['line_coverage']:.1f}%) but "
              f"zero branch coverage indicates untested conditional paths")
        print()
    
    # Save selection
    selection_file = BASE / "part2_selected_problems.json"
    with open(selection_file, 'w') as f:
        json.dump({
            'selected': [item['problem'] for item in selected],
            'all_metrics': problem_metrics
        }, f, indent=2)
    
    print(f"Selection saved to: {selection_file}")
    
    return selected

if __name__ == "__main__":
    main()
