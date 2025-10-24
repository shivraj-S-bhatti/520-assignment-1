#!/usr/bin/env python3
"""
Chain-of-Thought (CoT) Evaluation
Evaluates both models using Chain-of-Thought prompting strategy.
"""

import os
import sys
import json
import pathlib
import time
import importlib.util
import re
import csv
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List

# Import model client directly
sys.path.append('eval')
from model_clients import ModelConfig, get_client

@dataclass
class EvalConfig:
    models: List[Dict[str, Any]]
    strategies: List[str]
    k: int = 1
    max_repairs: int = 1
    results_path: str = "generated/cot_results.jsonl"
    csv_summary_path: str = "generated/cot_summary.csv"
    log_prompts_path: str = "generated/cot_prompts.jsonl"

def load_test_runner(test_path: pathlib.Path):
    """Load test runner from test file."""
    spec = importlib.util.spec_from_file_location(test_path.stem, str(test_path))
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod.run_tests

def run_single_candidate(code: str, func_name: str, test_runner) -> Tuple[bool, List[str]]:
    """Test a single code candidate."""
    ns = {}
    try:
        exec(code, ns, ns)
    except Exception as e:
        return False, [f"Code failed to import: {e}"]
    if func_name not in ns or not callable(ns[func_name]):
        return False, [f"Function {func_name} not found after exec"]
    try:
        passed, failures = test_runner(ns[func_name])
        return passed, failures
    except Exception as e:
        return False, [f"Test runner error: {e}"]

def extract_python_code(text: str) -> str:
    """Extract Python code from response."""
    fence = re.search(r"```(?:python)?\s*(.+?)```", text, re.DOTALL|re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    return text.strip()

def build_problem_spec(md_path: str) -> str:
    """Load problem specification from markdown file."""
    return pathlib.Path(md_path).read_text()

def fill_template(tmpl: str, problem_spec: str, **kwargs) -> str:
    """Fill template with problem spec and other variables."""
    out = tmpl.replace("{PROBLEM_SPEC}", problem_spec)
    for k, v in kwargs.items():
        out = out.replace("{" + k + "}", v)
    return out

def run_cot_evaluation():
    """Run Chain-of-Thought evaluation for both models."""
    
    # Configuration for CoT evaluation
    cfg = EvalConfig(
        models=[
            {"provider": "google", "model": "gemini-2.0-flash", "temperature": 0.6},
            {"provider": "huggingface", "model": "deepseek-ai/DeepSeek-V3-0324", "temperature": 0.6},
        ],
        strategies=["cot"],  # Chain-of-Thought strategy
        k=1,  # 1 sample per problem per model
        max_repairs=1
    )
    
    print("Chain-of-Thought (CoT) Evaluation")
    print("=================================")
    model_names = [f"{m['provider']}:{m['model']}" for m in cfg.models]
    print(f"Models: {model_names}")
    print(f"Strategy: {cfg.strategies[0]}")
    print(f"k={cfg.k}")
    print()
    
    # Setup paths
    BASE = pathlib.Path(__file__).resolve().parents[0]
    PROBLEMS_DIR = BASE / "problems"
    TESTS_DIR = BASE / "tests"
    PROMPTS_DIR = BASE / "prompts"
    OUT_DIR = BASE / "generated"
    
    # Load strategy templates
    full = (PROMPTS_DIR / "strategy_templates.md").read_text()
    def between(text, start, end):
        a = text.index(start) + len(start)
        b = text.index(end, a)
        return text[a:b]
    
    TEMPLATES = {
        "cot": between(full, "## 1) Chain-of-Thought (CoT)", "## 2) Stepwise Chain-of-Thought (SCoT)").strip(),
    }
    
    # Load problems
    problems = []
    for md in sorted(PROBLEMS_DIR.glob("*.md")):
        func_name = md.stem
        problems.append({
            "name": md.stem,
            "md_path": str(md),
            "func_name": func_name,
            "test_path": str(TESTS_DIR / f"test_{md.stem}.py"),
        })
    
    print(f"Found {len(problems)} problems to evaluate")
    print()
    
    # Create output directory
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # Run evaluation with faster rate limiting for Hugging Face
    results = []
    summary_rows = []
    
    with open(cfg.results_path, "w") as results_f, open(cfg.log_prompts_path, "w") as prompts_f:
        for i, model_dict in enumerate(cfg.models):
            print(f"Testing model {i+1}/{len(cfg.models)}: {model_dict['provider']}:{model_dict['model']}")
            client = get_client(ModelConfig(**model_dict))
            
            for j, strat in enumerate(cfg.strategies):
                print(f"  Strategy {j+1}/{len(cfg.strategies)}: {strat}")
                
                for k, p in enumerate(problems):
                    print(f"    Problem {k+1}/{len(problems)}: {p['name']}")
                    
                    # Faster rate limiting for Hugging Face (5 seconds)
                    if k > 0 or i > 0:
                        wait_time = 3 if model_dict['provider'] == 'huggingface' else 12
                        print(f"      Waiting {wait_time} seconds for rate limiting...")
                        time.sleep(wait_time)
                    
                    test_runner = load_test_runner(pathlib.Path(p["test_path"]))
                    prob_spec = build_problem_spec(p["md_path"])
                    
                    # Generate code
                    prompt = fill_template(TEMPLATES[strat], prob_spec)
                    texts = client.generate(prompt, n=cfg.k)
                    
                    # Log prompt
                    prompts_f.write(json.dumps({
                        "ts": time.time(), 
                        "model": model_dict, 
                        "strategy": strat,
                        "problem": p["name"],
                        "prompt": prompt
                    }) + "\n")
                    
                    # Test generated code
                    successes = 0
                    history_all = []
                    
                    for t in texts:
                        code = extract_python_code(t)
                        passed, failures = run_single_candidate(code, p["func_name"], test_runner)
                        history_all.append({"code": code, "passed": passed, "failures": failures})
                        if passed:
                            successes += 1
                    
                    # Record results
                    record = {
                        "ts": time.time(),
                        "problem": p["name"],
                        "model": model_dict,
                        "strategy": strat,
                        "k": cfg.k,
                        "successes": successes,
                        "pass_at_k": 1.0 if successes > 0 else 0.0,
                        "history": history_all,
                    }
                    results_f.write(json.dumps(record) + "\n")
                    results.append(record)
                    summary_rows.append([
                        p["name"], 
                        f"{model_dict['provider']}:{model_dict['model']}", 
                        strat, 
                        cfg.k, 
                        successes, 
                        1 if successes > 0 else 0
                    ])
                    
                    print(f"      Result: {'✓ PASS' if successes > 0 else '✗ FAIL'}")
    
    # Write CSV summary
    with open(OUT_DIR / "cot_summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["problem", "model", "strategy", "k", "successes", "pass@k (0/1)"])
        w.writerows(summary_rows)
    
    # Calculate statistics by model
    model_stats = {}
    for result in results:
        model_key = f"{result['model']['provider']}:{result['model']['model']}"
        if model_key not in model_stats:
            model_stats[model_key] = {"total": 0, "passed": 0, "problems": []}
        model_stats[model_key]["total"] += 1
        if result["pass_at_k"] > 0:
            model_stats[model_key]["passed"] += 1
        model_stats[model_key]["problems"].append({
            "problem": result["problem"],
            "passed": result["pass_at_k"] > 0
        })
    
    print()
    print("CoT Evaluation Complete!")
    print("=======================")
    print()
    
    for model_key, stats in model_stats.items():
        pass_rate = stats["passed"] / stats["total"] if stats["total"] > 0 else 0
        print(f"{model_key}:")
        print(f"  Pass Rate: {stats['passed']}/{stats['total']} ({pass_rate:.1%})")
        
        # Show which problems each model passed/failed
        passed_problems = [p["problem"] for p in stats["problems"] if p["passed"]]
        failed_problems = [p["problem"] for p in stats["problems"] if not p["passed"]]
        
        if passed_problems:
            print(f"  Passed: {', '.join(passed_problems)}")
        if failed_problems:
            print(f"  Failed: {', '.join(failed_problems)}")
        print()
    
    print(f"\nResults saved to: {cfg.results_path}")
    print(f"Summary saved to: {cfg.csv_summary_path}")
    print(f"Prompts saved to: {cfg.log_prompts_path}")
    
    return results

def main():
    print("Chain-of-Thought (CoT) Evaluation")
    print("=================================")
    print("Evaluating both models using Chain-of-Thought strategy")
    print()
    
    # Check API keys
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not set!")
        return False
    
    if not os.environ.get("HUGGINGFACE_API_KEY"):
        print("Error: HUGGINGFACE_API_KEY not set!")
        return False
    
    try:
        results = run_cot_evaluation()
        return True
    except Exception as e:
        print(f"Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
