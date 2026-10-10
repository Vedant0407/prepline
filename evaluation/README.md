# Phase 13 — NLP Matching Evaluation

This folder evaluates how well Prepline maps syllabus/interview text to the existing, versioned taxonomy.

## Files

- `ground_truth.csv`: schema template for manually verified examples. It intentionally contains no fabricated labels.
- `evaluate_nlp.py`: compares keyword overlap, TF-IDF cosine similarity, and `all-MiniLM-L6-v2` sentence embeddings.
- `requirements.txt`: packages needed by the evaluation script.
- `results.json`: generated locally when the script runs; do not commit results until the dataset and experiment are reviewed.

## Ground-truth CSV

Required columns:

- `raw_text`: the original syllabus concept or interview question.
- `expected_topic_id`: the correct ID from `data/taxonomy/taxonomy_v1.0.json`.
- `taxonomy_version`: must match the taxonomy version used for evaluation (currently `v1.0`).

Optional columns such as `source_id`, `source_type`, `annotator`, and `notes` may be added. Each row must be checked by a human against the taxonomy. Do not fill the dataset with guessed labels or generated synthetic examples and call it ground truth.

The blueprint calls for **200+ manually verified mappings** and a 70% development / 15% validation / 15% final test split. The CSV in this package is only a template, not a completed benchmark.

## Run

From the repository root:

```bash
python -m pip install -r evaluation/requirements.txt
python evaluation/evaluate_nlp.py --data evaluation/ground_truth.csv
```

The sentence-embedding model is downloaded by `sentence-transformers` the first time it is used; after that, it can be loaded locally. If the package is unavailable, that method is reported as skipped.

## Evaluation discipline

- Tune similarity thresholds using validation data only.
- Keep the final test split untouched until method and threshold choices are frozen.
- Report accuracy, macro precision, macro recall, and macro F1.
- Inspect errors and per-topic class balance; aggregate metrics alone can hide weak topics.
- Record the taxonomy version, embedding model, and threshold in the final report.
- This module does not modify Prepline's scoring formulas or taxonomy.
