
import os, json, pathlib, importlib.util, time, csv
from typing import Dict, Any, Tuple, List
from dataclasses import dataclass
from model_clients import ModelConfig, get_client
from strategies import extract_python_code, build_problem_spec, fill_template

BASE = pathlib.Path(__file__).resolve().parents[1]
PROBLEMS_DIR = BASE / "problems"
TESTS_DIR = BASE / "tests"
PROMPTS_DIR = BASE / "prompts"
OUT_DIR = BASE / "a1" / "generated"

# Load strategy templates segments
full = (PROMPTS_DIR / "strategy_templates.md").read_text()
def between(text, start, end):
    a = text.index(start) + len(start)
    b = text.index(end, a)
    return text[a:b]

TEMPLATES = {
    "cot": between(full, "## 1) Chain-of-Thought (CoT)", "## 2) Stepwise Chain-of-Thought (SCoT)").strip(),
    "scot_plan": between(full, "## 2) Stepwise Chain-of-Thought (SCoT)", "## 3) Self-Planning").strip(),
    "self_planning": between(full, "## 3) Self-Planning", "## 4) Self-Debugging").strip(),
    "self_debugging": between(full, "## 4) Self-Debugging", "## 5) Self-Edit").strip(),
    "self_edit": between(full, "## 5) Self-Edit", "## 6) Self-Repair (Iterative)").strip(),
    "self_repair": full.split("## 6) Self-Repair (Iterative)")[1].strip()
}

@dataclass
class EvalConfig:
    models: List[Dict[str, Any]]
    strategies: List[str]
    k: int = 3
    max_repairs: int = 2
    results_path: str = str(OUT_DIR / "results.jsonl")
    csv_summary_path: str = str(OUT_DIR / "summary.csv")
    log_prompts_path: str = str(OUT_DIR / "prompts_used.jsonl")

def load_test_runner(test_path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(test_path.stem, str(test_path))
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    assert spec and spec.loader
    spec.loader.exec_module(mod)  # type: ignore
    return mod.run_tests

def run_single_candidate(code: str, func_name: str, test_runner) -> Tuple[bool, List[str]]:
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

def iter_self_repair(client, base_prompt, func_name, test_runner, templates, max_repairs=2):
    texts = client.generate(base_prompt, n=1)
    code = extract_python_code(texts[0])
    passed, failures = run_single_candidate(code, func_name, test_runner)
    history = [{"code": code, "passed": passed, "failures": failures}]
    if passed:
        return code, history

    repair_tmpl = templates["self_repair"]
    for _ in range(max_repairs):
        repair_prompt = fill_template(repair_tmpl, "", CURRENT_CODE=code, TEST_ERRORS="\n".join(failures))
        texts = client.generate(repair_prompt, n=1)
        code = extract_python_code(texts[0])
        passed, failures = run_single_candidate(code, func_name, test_runner)
        history.append({"code": code, "passed": passed, "failures": failures})
        if passed:
            break
    return code, history

def main():
    cfg = EvalConfig(
        models=[
            {"provider":"openai", "model":"gpt-4o-mini"},
            {"provider":"anthropic", "model":"claude-3-5-sonnet"},
        ],
        strategies=["cot", "self_edit"],
        k=3
    )

    problems = []
    for md in sorted(PROBLEMS_DIR.glob("*.md")):
        func_name = md.stem
        problems.append({
            "name": md.stem,
            "md_path": str(md),
            "func_name": func_name,
            "test_path": str(TESTS_DIR / f"test_{md.stem}.py"),
        })

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(cfg.results_path, "w") as results_f, open(cfg.log_prompts_path, "w") as prompts_f:
        summary_rows = []
        for model_dict in cfg.models:
            client = get_client(ModelConfig(**model_dict))

            for strat in cfg.strategies:
                for p in problems:
                    test_runner = load_test_runner(pathlib.Path(p["test_path"]))
                    prob_spec = build_problem_spec(p["md_path"])

                    successes = 0
                    history_all = []
                    if strat == "self_repair":
                        base_prompt = fill_template(TEMPLATES["cot"], prob_spec)
                        code, history = iter_self_repair(client, base_prompt, p["func_name"], test_runner, TEMPLATES, max_repairs=cfg.max_repairs)
                        successes = int(history[-1]["passed"] if history else 0)
                        history_all = history
                        prompts_f.write(json.dumps({
                            "ts": time.time(), "model": model_dict, "strategy": strat,
                            "prompt": base_prompt
                        }) + "\n")
                    else:
                        prompt = fill_template(TEMPLATES[strat], prob_spec)
                        texts = client.generate(prompt, n=cfg.k)
                        prompts_f.write(json.dumps({
                            "ts": time.time(), "model": model_dict, "strategy": strat,
                            "prompt": prompt
                        }) + "\n")
                        for t in texts:
                            code = extract_python_code(t)
                            passed, failures = run_single_candidate(code, p["func_name"], test_runner)
                            history_all.append({"code": code, "passed": passed, "failures": failures})
                            if passed:
                                successes += 1

                    record = {
                        "ts": time.time(),
                        "problem": p["name"],
                        "model": model_dict,
                        "strategy": strat,
                        "k": cfg.k,
                        "successes": successes,
                        "pass_at_k": 1.0 if successes>0 else 0.0,
                        "history": history_all,
                    }
                    results_f.write(json.dumps(record)+"\n")
                    summary_rows.append([p["name"], f"{model_dict['provider']}:{model_dict['model']}", strat, cfg.k, successes, 1 if successes>0 else 0])

    # CSV summary
    with open(OUT_DIR / "summary.csv", "w", newline="") as f:
        import csv
        w = csv.writer(f)
        w.writerow(["problem","model","strategy","k","successes","pass@k (0/1)"])
        w.writerows(summary_rows)

    print("Done. See a1/generated/results.jsonl and a1/generated/summary.csv")

if __name__ == "__main__":
    main()
