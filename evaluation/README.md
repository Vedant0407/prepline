# Phase 13 — Ground-Truth Benchmark

## Files

- `SOURCE_REVIEW_LOG.md` at repository root (`evaluation/SOURCE_REVIEW_LOG.md`): source discovery log and candidate taxonomy mappings. These are not legally cleared sources or human-verified labels.

- `ground_truth.csv`: empty schema template for examples that have been reviewed by a human.
- `candidate_mappings_for_review.csv`: 392 draft candidate mappings covering 56 topics in `data/taxonomy/taxonomy_v1.1.json`. All are synthetic coverage prompts, not actual interview questions and not verified ground truth.
- `evaluate_nlp.py`: compares keyword overlap, TF-IDF cosine similarity, and `all-MiniLM-L6-v2` sentence embeddings.
- `requirements.txt`: required Python packages.

## Ground-truth standard

The blueprint requires 200+ manually verified mappings. A row qualifies only after a reviewer checks the original text and expected taxonomy node, confirms source/provenance, and records review status, reviewer, and review date. Synthetic candidates can help test the workflow but must not be included in final benchmark metrics.

Required columns in `ground_truth.csv`:
- `raw_text`
- `expected_topic_id`
- `taxonomy_version`
- `source_id`
- `source_type`
- `source_url`
- `review_status`
- `reviewer`
- `review_date`
- `notes`

The source can be a permitted interview-experience page or syllabus item. Do not copy large passages from copyrighted sites. Store a short question/topic summary where needed and preserve provenance. Review source terms before bulk collection.

## Taxonomy

The original `data/taxonomy/taxonomy_v1.0.json` is preserved. The expanded `data/taxonomy/taxonomy_v1.1.json` contains 56 topics spanning DSA, DBMS, OS, Computer Networks, and System Design.

## Readiness check

From the repository root, run:

```bash
python scripts/check_phase_readiness.py
```

This check reports whether explicit Phase 2 and Phase 13 acceptance fields pass. It does not itself establish source legality or validate the quality of a human review.

## Run

From the repository root:

```bash
python -m pip install -r evaluation/requirements.txt
python evaluation/evaluate_nlp.py --data evaluation/ground_truth.csv --taxonomy data/taxonomy/taxonomy_v1.1.json
```

The script intentionally refuses to produce metrics on a tiny placeholder dataset. Sentence embeddings require downloading `all-MiniLM-L6-v2` on first use.

## Evaluation protocol

- Split into 70% development, 15% validation, 15% final test.
- Tune similarity thresholds on validation only.
- Do not use the final test set to choose the model, threshold, or preprocessing.
- Report accuracy, macro precision, macro recall, and macro F1.
- Record taxonomy version, model version, threshold, data provenance, and review status.
- Review class balance and per-topic errors before making claims.

## Current status

The candidate annotation scaffold is committed. The verified benchmark is **not complete** until 200+ sourced mappings have passed human review. The interview index in `data/raw/interviews/` is a discovery list whose source eligibility and deduplication still need review.
