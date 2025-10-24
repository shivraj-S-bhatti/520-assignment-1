
# Report: Prompting, Debugging, and Innovation for Code Generation with LLMs

**Student:** <Your Name>  
**Models (families):** e.g., OpenAI GPT-4o-mini (GPT family), Anthropic Claude 3.5 Sonnet (Claude family)  
**Problems:** 10 custom problems (see repo)

---

## Methodology

- **Datasets/Problems:** Custom problems with comprehensive tests (happy + exceptional paths).
- **Prompting strategies:** CoT, Self-Edit (plus optional SCoT, Self-Debugging, Self-Repair).
- **Evaluation metric:** pass@k with k=3 (unless otherwise stated). A trial is success if any of the k generations passes all tests.
- **Environment:** Python 3.10+, temperature=0.6, max_tokens=1024.

## Part 1 — Prompt Design & Code Generation (8 pts)

### Problems
List all 10 problems with brief one-liners (or link to `problems/`).

### Exact Prompts Used
Attach or link to `generated/prompts_used.jsonl` (required). You may also paste representative prompts here.

### Results Table
Fill after running `eval/run_eval.py`:

| Problem | Model | Strategy | k | successes | pass@k |
|---|---|---:|---:|---:|---:|
| normalize_path | gpt-4o-mini | CoT | 3 | 2 | 1 |
| ... | ... | ... | ... | ... | ... |

**Discussion:** Briefly explain trends (e.g., Self-Edit outperforms CoT on parsing tasks).

## Part 2 — Debugging & Iterative Improvement (6 pts)

Select **≥2 failure cases** where initial code failed tests.

For each case:
- **Problem & Attempt:** e.g., `parse_csv_line` with CoT on Claude.
- **Failure Evidence:** paste failing messages from `history.failures`.
- **Refinements:** show modified prompts or provided hints.
- **What worked / What didn't:** concrete observations.
- **Why the model struggled:** reasoning gap, error handling, ambiguity, etc.
- **Cross-family comparison:** how did GPT vs Claude fail; which debugging loop helped.

> Include exact prompts for the failed and improved attempts.

## Part 3 — Innovation: Your Strategy (6 pts)

**Proposed Idea (example template):** *Spec-Then-Test (STT) + Minimal Patch Loop*  
1) Ask model to **extract a formal spec** (inputs, invariants, edge cases).  
2) Model writes **unit tests** (hidden/private).  
3) Model writes implementation.  
4) Harness runs **your** tests; returns failures.  
5) One-shot **patch** request with the failing traces.

**Rationale:** Forces the model to attend to constraints; patch loop fixes common off-by-one/edge handling errors.

**Experiment:** Apply to both families; summarize pass@k deltas vs. baseline.

**Outcome:** Did it improve? If not, analyze failure points and what you’d change next time.

## References
- Link to your GitHub repo.
- Note any libraries or APIs used.
