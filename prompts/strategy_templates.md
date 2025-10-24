
# Prompt Strategy Templates

These templates are designed for **Python** coding tasks. Replace `{PROBLEM_SPEC}` with the full text of the selected problem (title, signature, details). Always ask the model to return **only one Python code block** that defines the required function, with no extra text.

---

## 1) Chain-of-Thought (CoT)
**Instruction to model:**
> You are a senior Python engineer. Think step-by-step about edge cases and the algorithm. Then implement the function.

**Prompt:**
```
{PROBLEM_SPEC}

Requirements:
- Implement only the required function with the exact signature.
- Include a brief docstring that lists handled edge-cases.
- Return only a Python code block; no prose.

Let's reason step-by-step, then write the code.
```

## 2) Stepwise Chain-of-Thought (SCoT)
Run as **two turns**:
- **Turn A (planning):**
```
{PROBLEM_SPEC}

First, write a numbered high-level plan (bullet points only) covering data structures, edge cases, and complexity. Do NOT write code yet.
```
- **Turn B (implementation):**
```
Using the plan above, now implement the function exactly as specified.

Return only a single Python code block with the implementation.
```

## 3) Self-Planning
```
{PROBLEM_SPEC}

Before coding, write a short plan with:
- Inputs/outputs
- Invariants and constraints
- Test ideas (unit tests we should pass)
Then write the function implementation.
Return a single Python code block only.
```

## 4) Self-Debugging
Run as **two (or more) turns**:
- **Turn A (implementation):** Use a simple direct implementation.
- Run tests; collect failure messages.
- **Turn B (debug):**
```
{PROBLEM_SPEC}

Here are the failing tests and error messages:
{TEST_ERRORS}

Revise the function to fix the failures. Return only the updated Python code block.
```

## 5) Self-Edit
Single turn; ask model to write, then self-review within the message:
```
{PROBLEM_SPEC}

Write the function, then add a brief **self-review** comment at the bottom of the code explaining complexity and edge cases covered.
Return only one Python code block.
```

## 6) Self-Repair (Iterative)
Multi-turn loop:
- Generate an initial solution.
- Execute tests.
- Provide errors back to the model and ask for a patch.
- Repeat up to N iterations or until all tests pass.
Use the following patch-style prompt:
```
{PROBLEM_SPEC}

Current code:
```python
{CURRENT_CODE}
```

Test errors:
{TEST_ERRORS}

Please provide a corrected full implementation. Return only one Python code block.
```
