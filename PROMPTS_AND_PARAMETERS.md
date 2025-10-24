# Prompts and Parameters Used

This document contains all the prompts and query parameters used in the LLM code generation evaluation.

## Evaluation Configuration

### Models Used
- **Google Gemini 2.0 Flash** (via Google AI API)
- **DeepSeek V3** (via Hugging Face Inference API)

### Strategies Evaluated
1. **Self-Edit** - Asks model to write code then self-review
2. **Chain-of-Thought (CoT)** - Asks model to think step-by-step before coding

### Parameters
- **k=1** - Single attempt per problem per model
- **Temperature**: 0.6 for all models
- **Max Tokens**: 1024 for all models
- **Rate Limiting**: 12 seconds for Google, 3 seconds for Hugging Face

## Strategy Templates

### 1. Self-Edit Strategy

```
{PROBLEM_SPEC}

Write the function, then add a brief **self-review** comment at the bottom of the code explaining complexity and edge cases covered.
Return only one Python code block.
```

### 2. Chain-of-Thought (CoT) Strategy

```
{PROBLEM_SPEC}

Requirements:
- Implement only the required function with the exact signature.
- Include a brief docstring that lists handled edge-cases.
- Return only a Python code block; no prose.

Let's reason step-by-step, then write the code.
```

## Sample Prompts by Model and Strategy

### Google Gemini 2.0 Flash - Self-Edit

**Problem**: cosine_similarity

```
# Cosine Similarity

**Function signature:**

```python
from typing import List

def cosine_similarity(a: List[float], b: List[float]) -> float:
```

**Task:** Compute cosine similarity between two equal-length vectors.

**Details & Constraints:**

Return 0.0 if either vector has zero magnitude. Use float return. Raise ValueError if lengths differ.

Write the function, then add a brief **self-review** comment at the bottom of the code explaining complexity and edge cases covered.
Return only one Python code block.
```

### Google Gemini 2.0 Flash - Chain-of-Thought

**Problem**: cosine_similarity

```
# Cosine Similarity

**Function signature:**

```python
from typing import List

def cosine_similarity(a: List[float], b: List[float]) -> float:
```

**Task:** Compute cosine similarity between two equal-length vectors.

**Details & Constraints:**

Return 0.0 if either vector has zero magnitude. Use float return. Raise ValueError if lengths differ.

Requirements:
- Implement only the required function with the exact signature.
- Include a brief docstring that lists handled edge-cases.
- Return only a Python code block; no prose.

Let's reason step-by-step, then write the code.
```

### DeepSeek V3 - Self-Edit

**Problem**: cosine_similarity

```
# Cosine Similarity

**Function signature:**

```python
from typing import List

def cosine_similarity(a: List[float], b: List[float]) -> float:
```

**Task:** Compute cosine similarity between two equal-length vectors.

**Details & Constraints:**

Return 0.0 if either vector has zero magnitude. Use float return. Raise ValueError if lengths differ.

Write the function, then add a brief **self-review** comment at the bottom of the code explaining complexity and edge cases covered.
Return only one Python code block.
```

### DeepSeek V3 - Chain-of-Thought

**Problem**: cosine_similarity

```
# Cosine Similarity

**Function signature:**

```python
from typing import List

def cosine_similarity(a: List[float], b: List[float]) -> float:
```

**Task:** Compute cosine similarity between two equal-length vectors.

**Details & Constraints:**

Return 0.0 if either vector has zero magnitude. Use float return. Raise ValueError if lengths differ.

Requirements:
- Implement only the required function with the exact signature.
- Include a brief docstring that lists handled edge-cases.
- Return only a Python code block; no prose.

Let's reason step-by-step, then write the code.
```

## Complete Results Summary

### Self-Edit Strategy Results
- **Google Gemini 2.0 Flash**: 80% pass rate (8/10 problems)
- **DeepSeek V3**: 90% pass rate (9/10 problems)

### Chain-of-Thought Strategy Results
- **Google Gemini 2.0 Flash**: 80% pass rate (8/10 problems)
- **DeepSeek V3**: 90% pass rate (9/10 problems)

## Detailed Prompt Logs

All detailed prompts used in the evaluation are logged in:
- `generated/final_dual_prompts.jsonl` - Self-Edit prompts
- `generated/cot_prompts.jsonl` - Chain-of-Thought prompts

Each log entry contains:
- Timestamp
- Model information
- Strategy used
- Problem name
- Complete prompt text

## API Parameters

### Google Gemini 2.0 Flash
- **Provider**: google
- **Model**: gemini-2.0-flash
- **Temperature**: 0.6
- **Max Tokens**: 1024
- **Rate Limit**: 5 requests per minute

### DeepSeek V3
- **Provider**: huggingface
- **Model**: deepseek-ai/DeepSeek-V3-0324
- **Temperature**: 0.6
- **Max Tokens**: 1024
- **Rate Limit**: 20 requests per minute (faster than Google)

## Evaluation Methodology

1. **Problem Selection**: 10 custom programming problems covering various algorithmic challenges
2. **Strategy Application**: Each problem tested with both Self-Edit and Chain-of-Thought strategies
3. **Model Testing**: Each strategy tested on both Google Gemini and DeepSeek V3
4. **Result Validation**: Generated code tested against comprehensive test suites
5. **Pass@k Calculation**: Success rate calculated as pass@1 (single attempt per problem)

## Files Generated

- `generated/final_dual_results.jsonl` - Self-Edit evaluation results
- `generated/final_dual_summary.csv` - Self-Edit summary metrics
- `generated/final_dual_prompts.jsonl` - Self-Edit prompts log
- `generated/cot_results.jsonl` - Chain-of-Thought evaluation results
- `generated/cot_summary.csv` - Chain-of-Thought summary metrics
- `generated/cot_prompts.jsonl` - Chain-of-Thought prompts log
