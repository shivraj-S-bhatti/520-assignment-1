#!/usr/bin/env python3
"""
Debugging script for failed problems.
Analyzes and improves failed code generation attempts.
"""

import os
import sys
import json
import pathlib
import time
from typing import List, Dict, Any

# Import evaluation functions
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'eval'))
from model_clients import ModelConfig, get_client

def load_failed_problems():
    """Load the failed problems from the evaluation results."""
    results_file = "generated/results.jsonl"
    failed_problems = []
    
    with open(results_file, 'r') as f:
        for line in f:
            result = json.loads(line.strip())
            if result['pass_at_k'] == 0.0:  # Failed problem
                failed_problems.append(result)
    
    return failed_problems

def create_debug_prompt(problem_spec: str, failed_code: str, test_failures: List[str]) -> str:
    """Create a debugging prompt for the failed problem."""
    return f"""
{problem_spec}

The following code was generated but failed the test cases:

```python
{failed_code}
```

Test failures:
{chr(10).join(f"- {failure}" for failure in test_failures)}

Please analyze the failures and provide a corrected implementation. Focus on:
1. Understanding why the original code failed
2. Identifying the specific bugs or logic errors
3. Providing a corrected version that handles all test cases

Return only the corrected Python code block.
"""

def create_improved_prompt(problem_spec: str, original_failures: List[str]) -> str:
    """Create an improved prompt based on the original failures."""
    return f"""
{problem_spec}

IMPORTANT: Based on previous attempts, pay special attention to these common failure patterns:
{chr(10).join(f"- {failure}" for failure in original_failures)}

Please implement the function with extra care for these edge cases. Return only the Python code block.
"""

def debug_problem(problem_data: Dict[str, Any], strategy: str = "debug") -> Dict[str, Any]:
    """Debug a single failed problem."""
    print(f"\n{'='*60}")
    print(f"Debugging: {problem_data['problem']}")
    print(f"Strategy: {strategy}")
    print(f"{'='*60}")
    
    # Load problem specification
    problem_spec = pathlib.Path(problem_data['problem'] + '.md').read_text()
    
    # Get the failed code and test failures
    failed_code = problem_data['history'][0]['code']
    test_failures = problem_data['history'][0]['failures']
    
    print(f"Original failures: {len(test_failures)}")
    for failure in test_failures:
        print(f"  - {failure}")
    
    # Create appropriate prompt
    if strategy == "debug":
        prompt = create_debug_prompt(problem_spec, failed_code, test_failures)
    else:  # improved
        prompt = create_improved_prompt(problem_spec, test_failures)
    
    # Generate corrected code
    client = get_client(ModelConfig(provider="google", model="gemini-2.0-flash", temperature=0.3))
    response = client.generate(prompt, n=1)
    
    # Extract code
    import re
    fence = re.search(r"```(?:python)?\s*(.+?)```", response[0], re.DOTALL|re.IGNORECASE)
    if fence:
        corrected_code = fence.group(1).strip()
    else:
        corrected_code = response[0].strip()
    
    print(f"\nGenerated corrected code:")
    print("-" * 40)
    print(corrected_code)
    print("-" * 40)
    
    return {
        "problem": problem_data['problem'],
        "strategy": strategy,
        "original_code": failed_code,
        "corrected_code": corrected_code,
        "original_failures": test_failures,
        "prompt_used": prompt
    }

def test_corrected_code(problem_name: str, corrected_code: str) -> tuple[bool, List[str]]:
    """Test the corrected code against the test suite."""
    # Load test runner
    test_path = pathlib.Path(__file__).parent.parent / "tests" / f"test_{problem_name}.py"
    spec = importlib.util.spec_from_file_location(test_path.stem, str(test_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Execute corrected code
    ns = {}
    exec(corrected_code, ns, ns)
    
    # Find the function name
    func_name = problem_name
    if func_name not in ns:
        return False, [f"Function {func_name} not found in corrected code"]
    
    # Run tests
    try:
        passed, failures = mod.run_tests(ns[func_name])
        return passed, failures
    except Exception as e:
        return False, [f"Test execution error: {e}"]

def main():
    print("LLM Code Generation - Debugging Analysis")
    print("=======================================")
    print("Part 2: Debugging & Iterative Improvement")
    print()
    
    # Check API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not set!")
        return False
    
    # Load failed problems
    failed_problems = load_failed_problems()
    print(f"Found {len(failed_problems)} failed problems to debug")
    
    if not failed_problems:
        print("No failed problems found. All problems passed!")
        return True
    
    # Debug each failed problem
    debug_results = []
    
    for i, problem_data in enumerate(failed_problems):
        print(f"\nProblem {i+1}/{len(failed_problems)}: {problem_data['problem']}")
        
        # Try debugging strategy
        debug_result = debug_problem(problem_data, "debug")
        debug_results.append(debug_result)
        
        # Test the corrected code
        print("\nTesting corrected code...")
        passed, failures = test_corrected_code(problem_data['problem'], debug_result['corrected_code'])
        
        if passed:
            print("✅ CORRECTED CODE PASSES ALL TESTS!")
        else:
            print(f"❌ Corrected code still fails {len(failures)} tests:")
            for failure in failures:
                print(f"  - {failure}")
        
        # Rate limiting
        if i < len(failed_problems) - 1:
            print("Waiting 12 seconds for rate limiting...")
            time.sleep(12)
    
    # Save debug results
    with open("generated/debug_results.json", "w") as f:
        json.dump(debug_results, f, indent=2)
    
    print(f"\n{'='*60}")
    print("DEBUGGING COMPLETE")
    print(f"{'='*60}")
    print(f"Debugged problems: {len(debug_results)}")
    print(f"Results saved to: generated/debug_results.json")
    
    return True

if __name__ == "__main__":
    import importlib.util
    success = main()
    sys.exit(0 if success else 1)
