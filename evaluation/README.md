# Phase 13 — NLP Matching Evaluation

This folder contains the initial evaluation harness and a **392-row candidate annotation set** for Prepline's taxonomy matching.

## Files

- `ground_truth.csv`: 392 candidate mappings across the 56 topics in `data/taxonomy/taxonomy_v1.1.json`.
- `evaluate_nlp.py`: compares keyword overlap, TF-IDF cosine similarity, and `all-MiniLM-L6-v2` sentence embeddings.
- `requirements.txt`: packages needed by the evaluation script.

## Important: candidate set, not verified ground truth

Every current row is marked `source_type=synthetic_candidate` and `review_status=needs_human_review`. These are original draft prompts generated to exercise taxonomy coverage; they are **not represented as real questions collected from company interviews** and must not be reported as 392 manually verified mappings.

Before using this dataset for final benchmark metrics:
1. Replace or supplement the generic candidate prompts with examples drawn from permitted, recorded sources (course syllabi, openly accessible interview write-ups, or independently written examples).
2. Have a human reviewer confirm each `expected_topic_id` against the taxonomy and change `review_status` only after review.
3. Record source URLs or stable source identifiers for sourced examples and respect each source's terms and applicable copyright restrictions.
4. Ensure examples are varied and not merely templated from the target topic name. The current set is a pipeline smoke-test scaffold, not a reliable measure of real-world classification performance.

The project blueprint calls for 200+ manually verified mappings, with 70% development / 15% validation / 15% final test splits. The row count alone does not satisfy the manual-verification requirement.

## Taxonomy

The original `data/taxonomy/taxonomy_v1.0.json` is preserved. The expanded `data/taxonomy/taxonomy_v1.1.json` adds DSA, DBMS, OS, Computer Networks, and System Design topics. The evaluation script defaults to v1.1.

## Public references used to guide topic coverage

These references support the *choice of subject areas*, not the claim that the candidate prompts were copied from or asked in interviews:

- University of Delhi Computer Science syllabus listings: https://cs.du.ac.in/uploads/syllabus/NEP/ge2024.html
- IIT Delhi CSE curriculum: https://cse.iitd.ac.in/academics/btech_links/curriculum.shtml
- NITK CSE undergraduate courses: https://cse.nitk.ac.in/courses/ug
- GeeksforGeeks OS, DBMS, and Computer Networks interview-preparation overview: https://www.geeksforgeeks.org/interview-prep/os-cn-dbms-interview-questions/

## Run locally

From the repository root:

```bash
python -m pip install -r evaluation/requirements.txt
python evaluation/evaluate_nlp.py --data evaluation/ground_truth.csv --taxonomy data/taxonomy/taxonomy_v1.1.json
```

The sentence-embedding model is downloaded by `sentence-transformers` the first time it is used. If it cannot be loaded, that method is reported as skipped.

## Evaluation discipline

- Do not use rows marked `needs_human_review` for final benchmark claims.
- Tune thresholds on validation data only.
- Keep the final test split untouched until method and threshold choices are frozen.
- Report accuracy, macro precision, macro recall, and macro F1.
- Inspect per-topic errors and class balance; aggregate metrics alone can hide weak topics.
- Record taxonomy version, embedding model, threshold, data provenance, and reviewer status in the final report.
