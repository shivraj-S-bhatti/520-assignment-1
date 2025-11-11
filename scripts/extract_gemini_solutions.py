#!/usr/bin/env python3
"""
Extract Gemini solution code from JSONL result files.
Prioritizes Gemini (google) solutions for baseline analysis.
"""

import json
import pathlib
import re
from typing import Dict, Optional

def extract_code_from_text(text: str) -> str:
    """Extract Python code from response, removing comments."""
    # Extract code block if present
    fence = re.search(r"```(?:python)?\s*(.+?)```", text, re.DOTALL|re.IGNORECASE)
    if fence:
        code = fence.group(1).strip()
    else:
        code = text.strip()
    
    # Remove self-review comments (lines starting with # Self-review)
    lines = code.split('\n')
    cleaned_lines = []
    skip_comment = False
    
    for line in lines:
        if '# Self-review' in line or '# Self-review:' in line:
            skip_comment = True
            continue
        if skip_comment and line.strip().startswith('#'):
            continue
        if skip_comment and line.strip() == '':
            continue
        if skip_comment and not line.strip().startswith('#'):
            skip_comment = False
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines).strip()

def load_solutions_from_jsonl(filepath: pathlib.Path) -> Dict[str, Dict]:
    """Load solutions from JSONL file, prioritizing Gemini (google) solutions."""
    solutions = {}
    
    with open(filepath, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            problem = data['problem']
            model = data['model']
            
            # Prioritize Gemini (google) over DeepSeek (huggingface)
            if problem not in solutions:
                solutions[problem] = {
                    'code': None,
                    'model': None,
                    'provider': None,
                    'strategy': data.get('strategy', 'unknown')
                }
            
            # Update if this is a Gemini solution, or if we don't have one yet
            current_provider = solutions[problem]['provider']
            new_provider = model['provider']
            
            if new_provider == 'google' or (current_provider != 'google' and current_provider is None):
                if data['history'] and len(data['history']) > 0:
                    code = data['history'][0]['code']
                    solutions[problem]['code'] = extract_code_from_text(code)
                    solutions[problem]['model'] = model['model']
                    solutions[problem]['provider'] = new_provider
    
    return solutions

def main():
    """Extract Gemini solutions from JSONL files and save to src/ directory."""
    BASE = pathlib.Path(__file__).resolve().parents[1]
    GENERATED_DIR = BASE / "generated"
    SRC_DIR = BASE / "src"
    
    # Create src directory
    SRC_DIR.mkdir(exist_ok=True)
    
    # Load solutions from result files
    all_solutions = {}
    
    # Try final_dual_results.jsonl first (Self-Edit strategy)
    final_dual_file = GENERATED_DIR / "final_dual_results.jsonl"
    if final_dual_file.exists():
        solutions = load_solutions_from_jsonl(final_dual_file)
        for problem, data in solutions.items():
            if problem not in all_solutions or data['code']:
                all_solutions[problem] = data
    
    # Try cot_results.jsonl (Chain-of-Thought strategy) as fallback
    cot_file = GENERATED_DIR / "cot_results.jsonl"
    if cot_file.exists():
        solutions = load_solutions_from_jsonl(cot_file)
        for problem, data in solutions.items():
            if problem not in all_solutions or not all_solutions[problem]['code']:
                if data['code']:
                    all_solutions[problem] = data
    
    # Write solution files to src/
    problems_written = 0
    for problem, data in sorted(all_solutions.items()):
        if data['code']:
            solution_file = SRC_DIR / f"{problem}.py"
            with open(solution_file, 'w') as f:
                f.write(data['code'])
            problems_written += 1
            print(f"✓ Extracted {problem} from {data['provider']}:{data['model']}")
        else:
            print(f"✗ No solution found for {problem}")
    
    print(f"\nExtracted {problems_written} Gemini solutions to {SRC_DIR}/")
    
    # Verify all 10 problems are present
    expected_problems = [
        "cosine_similarity", "evaluate_rpn", "int_to_roman", "is_palindrome_sentence",
        "merge_intervals", "min_window_substring", "normalize_path", "parse_csv_line",
        "sudoku_is_valid", "top_k_frequent"
    ]
    
    missing = [p for p in expected_problems if p not in all_solutions or not all_solutions[p]['code']]
    if missing:
        print(f"\n⚠ Warning: Missing solutions for: {', '.join(missing)}")
    else:
        print(f"\n✓ All 10 problems have Gemini solutions extracted")

if __name__ == "__main__":
    main()
