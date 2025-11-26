#!/usr/bin/env python3
"""
Innovation Strategy: Multi-Step Reasoning with Test-Driven Development
Novel strategies for LLM code generation.
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

def create_test_driven_prompt(problem_spec: str) -> str:
    """Create a test-driven development prompt."""
    return f"""
{problem_spec}

You are an expert software engineer following Test-Driven Development (TDD) principles.

Step 1: Analyze the problem and identify key test cases
- What are the happy path scenarios?
- What are the edge cases and boundary conditions?
- What error conditions should be handled?

Step 2: Write a test plan
- List 5-7 specific test cases you would write
- Include both positive and negative test cases
- Consider edge cases and error scenarios

Step 3: Implement the function
- Write clean, well-documented code
- Handle all the test cases you identified
- Include proper error handling and validation

Step 4: Self-review
- Walk through your test cases with your implementation
- Verify each test case would pass
- Identify any potential issues or improvements

Return your response in this format:

## Test Plan
[Your test cases here]

## Implementation
```python
[Your code here]
```

## Self-Review
[Your analysis here]
"""

def create_divide_and_conquer_prompt(problem_spec: str) -> str:
    """Create a divide-and-conquer approach prompt."""
    return f"""
{problem_spec}

You are solving this problem using a divide-and-conquer approach.

Step 1: Problem Decomposition
- Break the problem into smaller, manageable subproblems
- Identify the core algorithm or data structure needed
- List the main components and their responsibilities

Step 2: Subproblem Solutions
- Solve each subproblem individually
- Write helper functions for complex operations
- Ensure each component is testable in isolation

Step 3: Integration
- Combine the subproblem solutions
- Handle the interactions between components
- Ensure the overall solution is correct and efficient

Step 4: Optimization and Review
- Look for opportunities to optimize
- Check for edge cases and error conditions
- Verify the solution meets all requirements

Return your response in this format:

## Problem Decomposition
[Breakdown of the problem]

## Subproblem Solutions
[Helper functions and components]

## Main Implementation
```python
[Your main code here]
```

## Integration Notes
[How components work together]
"""

def create_innovation_strategy(problem_spec: str, strategy_name: str) -> str:
    """Create a prompt for the specified innovation strategy."""
    if strategy_name == "test_driven":
        return create_test_driven_prompt(problem_spec)
    elif strategy_name == "divide_conquer":
        return create_divide_and_conquer_prompt(problem_spec)
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")

def extract_code_from_response(response: str) -> str:
    """Extract Python code from the response."""
    import re
    # Look for code blocks
    fence = re.search(r"```(?:python)?\s*(.+?)```", response, re.DOTALL|re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    
    # If no code block, look for function definitions
    lines = response.split('\n')
    code_lines = []
    in_code = False
    
    for line in lines:
        if line.strip().startswith('def ') or line.strip().startswith('class '):
            in_code = True
        if in_code:
            code_lines.append(line)
    
    return '\n'.join(code_lines).strip()

def test_innovation_strategy(problem_name: str, strategy_name: str) -> Dict[str, Any]:
    """Test an innovation strategy on a specific problem."""
    print(f"\n{'='*60}")
    print(f"Testing Innovation Strategy: {strategy_name}")
    print(f"Problem: {problem_name}")
    print(f"{'='*60}")
    
    # Load problem specification
    problem_spec = (pathlib.Path(__file__).parent.parent / "problems" / f"{problem_name}.md").read_text()
    
    # Create prompt
    prompt = create_innovation_strategy(problem_spec, strategy_name)
    
    # Generate response
    client = get_client(ModelConfig(provider="google", model="gemini-2.0-flash", temperature=0.4))
    response = client.generate(prompt, n=1)
    
    # Extract code
    code = extract_code_from_response(response[0])
    
    print(f"Generated code:")
    print("-" * 40)
    print(code)
    print("-" * 40)
    
    # Test the code
    test_path = pathlib.Path(__file__).parent.parent / "tests" / f"test_{problem_name}.py"
    spec = importlib.util.spec_from_file_location(test_path.stem, str(test_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Execute code
    ns = {}
    try:
        exec(code, ns, ns)
    except Exception as e:
        return {
            "strategy": strategy_name,
            "problem": problem_name,
            "code": code,
            "response": response[0],
            "passed": False,
            "failures": [f"Code execution error: {e}"],
            "error_type": "execution"
        }
    
    # Find function and test
    func_name = problem_name
    if func_name not in ns:
        return {
            "strategy": strategy_name,
            "problem": problem_name,
            "code": code,
            "response": response[0],
            "passed": False,
            "failures": [f"Function {func_name} not found"],
            "error_type": "missing_function"
        }
    
    try:
        passed, failures = mod.run_tests(ns[func_name])
        return {
            "strategy": strategy_name,
            "problem": problem_name,
            "code": code,
            "response": response[0],
            "passed": passed,
            "failures": failures,
            "error_type": "test_failure" if not passed else None
        }
    except Exception as e:
        return {
            "strategy": strategy_name,
            "problem": problem_name,
            "code": code,
            "response": response[0],
            "passed": False,
            "failures": [f"Test execution error: {e}"],
            "error_type": "test_execution"
        }

def compare_strategies():
    """Compare innovation strategies against baseline."""
    print("LLM Code Generation - Innovation Strategy Testing")
    print("================================================")
    print("Part 3: Innovation - Propose Your Own Strategy")
    print()
    
    # Check API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not set!")
        return False
    
    # Test problems (select a few representative ones)
    test_problems = ["cosine_similarity", "normalize_path", "top_k_frequent"]
    strategies = ["test_driven", "divide_conquer"]
    
    results = []
    
    for problem in test_problems:
        print(f"\nTesting problem: {problem}")
        
        for strategy in strategies:
            result = test_innovation_strategy(problem, strategy)
            results.append(result)
            
            if result["passed"]:
                print(f"✅ {strategy}: PASSED")
            else:
                print(f"❌ {strategy}: FAILED ({len(result['failures'])} failures)")
                for failure in result['failures'][:3]:  # Show first 3 failures
                    print(f"    - {failure}")
            
            # Rate limiting
            time.sleep(12)
    
    # Save results
    with open("generated/innovation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Calculate statistics
    strategy_stats = {}
    for result in results:
        strategy = result["strategy"]
        if strategy not in strategy_stats:
            strategy_stats[strategy] = {"total": 0, "passed": 0}
        strategy_stats[strategy]["total"] += 1
        if result["passed"]:
            strategy_stats[strategy]["passed"] += 1
    
    print(f"\n{'='*60}")
    print("INNOVATION STRATEGY COMPARISON")
    print(f"{'='*60}")
    
    for strategy, stats in strategy_stats.items():
        pass_rate = stats["passed"] / stats["total"] if stats["total"] > 0 else 0
        print(f"{strategy}: {stats['passed']}/{stats['total']} ({pass_rate:.1%})")
    
    print(f"\nResults saved to: generated/innovation_results.json")
    
    return True

def main():
    return compare_strategies()

if __name__ == "__main__":
    import importlib.util
    success = main()
    sys.exit(0 if success else 1)
