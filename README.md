# LLM Code Generation Evaluation

This repository contains code and results for evaluating Large Language Models (LLMs) on programming problems.

## Overview

The evaluation compares multiple language models on a custom dataset of 10 programming problems, using various prompting strategies to assess code generation capabilities.

## Files

- `evaluate_models.py` - Main evaluation script
- `debug_failures.py` - Debugging analysis for failed problems
- `innovation_strategy.py` - Novel prompting strategies
- `problems/` - Programming problem specifications
- `tests/` - Test cases for each problem
- `generated/` - Evaluation results and generated code
- `eval/` - Model client implementations

## Results

- **Google Gemini 2.0 Flash**: 80% pass rate (8/10 problems)
- **DeepSeek V3**: 90% pass rate (9/10 problems)

## Usage

1. Set up API keys:
   ```bash
   export GOOGLE_API_KEY="your-key"
   export HUGGINGFACE_API_KEY="your-key"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run evaluation:
   ```bash
   python evaluate_models.py
   ```

## Generated Files

- `generated/final_dual_results.jsonl` - Complete results with generated code
- `generated/final_dual_summary.csv` - Pass@k metrics summary
- `generated/final_dual_prompts.jsonl` - All prompts used in evaluation