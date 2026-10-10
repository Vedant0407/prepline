# Prepline Phase 2 + Phase 13 Status

Updated: 2026-10-10

## Phase 2 — Dataset construction

Implemented in repository:
- Source-linked Amazon SDE-I interview experience discovery CSV with round/question-topic summaries and review fields.
- Official VIT CSE 2024-25 syllabus manifest with the official PDF URL and course-code scope.
- Downloader script that fetches the PDF from VIT's official host, validates the PDF signature, and prints SHA-256.
- Phase 2 README describing schema, source review, deduplication, legal-use checks, and ingestion expectations.

Still required before Phase 2 can be marked complete:
- Open and review each candidate source.
- Confirm at least 15 independent, eligible Amazon SDE-I reports after cross-post/deduplication checks.
- Complete legal-use review for source terms.
- Run the syllabus downloader locally, verify text-selectability, and preserve the original PDF at `data/raw/syllabi/VIT_CSE_2024_2025.pdf`.
- Parse reviewed sources into processed data while preserving provenance.

## Phase 13 — Ground-truth benchmark

Implemented in repository:
- Expanded taxonomy v1.1 (56 topic nodes); original v1.0 snapshot preserved.
- 392 synthetic candidate prompts in `evaluation/candidate_mappings_for_review.csv`, explicitly marked unverified.
- Empty `evaluation/ground_truth.csv` with provenance and human-review fields.
- Evaluation script comparing keyword overlap, TF-IDF, and sentence embeddings, using development/validation/test splits and validation-only threshold tuning.
- Documentation of benchmark requirements and limitations.

Still required before Phase 13 can be marked complete:
- Collect at least 200 source-backed examples permitted for this use.
- Have a human reviewer verify each text-to-topic mapping and fill reviewer/date/status fields.
- Ensure the final test split is untouched during model/threshold selection.
- Run the evaluation on verified examples and save/review metrics and per-topic errors.

## Important interpretation

File counts are not completion evidence by themselves. The repository now contains scaffolding and a source discovery index, but both phases remain pending their explicit validation gates above. Do not present synthetic candidates as real interview questions or as manually verified ground truth.
