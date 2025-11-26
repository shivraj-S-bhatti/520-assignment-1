#!/usr/bin/env python3
"""
Generate tests using LLM for Part 2 of Assignment 2.
"""

import sys
import os
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent / 'eval'))
from model_clients import GoogleClient, ModelConfig
import time

def generate_tests_for_problem(problem: str, prompt: str) -> str:
    """Generate tests using Gemini."""
    cfg = ModelConfig(
        provider="google",
        model="gemini-2.0-flash",
        temperature=0.6,
        max_tokens=2048
    )
    
    client = GoogleClient(cfg)
    
    print(f"Generating tests for {problem}...")
    responses = client.generate(prompt, n=1)
    
    # Rate limiting
    time.sleep(1)
    
    return responses[0] if responses else ""

def main():
    """Generate tests for normalize_path and top_k_frequent."""
    
    # Prompt for normalize_path
    normalize_prompt = """You are helping improve test coverage for a Python function normalize_path(path: str) that normalizes Unix-style paths. Current tests cover only simple relative paths. Generate pytest unit tests that target: (1) paths with multiple ../ segments, (2) paths that end with a slash but are not absolute, (3) paths that reduce to the empty segment, and (4) non-string or empty inputs if the function is supposed to reject them. Each test must be named test_norm_<description>. Return only Python tests, no explanations."""
    
    # Prompt for top_k_frequent
    topk_prompt = """You are helping improve test coverage for a function top_k_frequent(nums: List[int], k: int) that returns the k most frequent elements. Current tests cover only happy paths. Generate pytest tests to target: (1) k == 0 (should raise), (2) k greater than number of unique elements (should raise), (3) ties in frequency that must be broken by smaller numeric value, and (4) negative numbers. Each test must be named test_kfreq_<description>. Return only Python tests, no explanations."""
    
    # Generate tests
    normalize_tests = generate_tests_for_problem("normalize_path", normalize_prompt)
    topk_tests = generate_tests_for_problem("top_k_frequent", topk_prompt)
    
    # Save to files
    os.makedirs("tests/improved/normalize_path", exist_ok=True)
    os.makedirs("tests/improved/top_k_frequent", exist_ok=True)
    
    with open("tests/improved/normalize_path/iteration_1.py", "w") as f:
        f.write(normalize_tests)
    
    with open("tests/improved/top_k_frequent/iteration_1.py", "w") as f:
        f.write(topk_tests)
    
    print("\nTests generated and saved to:")
    print("  tests/improved/normalize_path/iteration_1.py")
    print("  tests/improved/top_k_frequent/iteration_1.py")

if __name__ == "__main__":
    main()
