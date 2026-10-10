# Prepline Phase 2 + Phase 13 Status

Updated: 2026-10-10 (source review pass)

## Latest work in this pass

- Added `evaluation/SOURCE_REVIEW_LOG.md` with 12 publicly discoverable interview-experience candidates, topic-level summaries, candidate taxonomy mapping suggestions, and explicit source/legal/deduplication caveats.
- Added `evaluation/source_backed_mappings_for_review.csv` with 109 source-linked topic-mapping candidates from publicly indexed interview reports. Every row remains `needs_human_review` and is excluded from benchmark metrics.
- Added `scripts/check_phase_readiness.py`, which checks explicit completion fields and refuses to mark either phase ready while minimum acceptance gates are open.

## Phase 2 — Dataset construction

Implemented in repository:
- Source-linked Amazon SDE-I interview experience discovery CSV with round/question-topic summaries and review fields.
- Official VIT CSE 2024-25 syllabus manifest with the official PDF URL and course-code scope.
- Extracted the Discipline Core course catalog from the user's available VIT syllabus PDF into `data/raw/syllabi/vit_cse_2024_2025_discipline_core_catalog.csv` (21 rows, printed page 2); added `data/raw/syllabi/README.md` with provenance and limitations.
- Downloader script that fetches the PDF from VIT's official host, validates the PDF signature, and prints SHA-256.
- Phase 2 README describing schema, source review, deduplication, legal-use checks, and ingestion expectations.

Still required before Phase 2 can be marked complete:
- Open and review each candidate source; the new source-review log is discovery evidence, not legal clearance or proof of independence.
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


## Final execution attempt (2026-10-10)

A further public-source research pass confirmed examples of topic summaries from publicly indexed Amazon SDE-1 experience pages, including graph traversal, trees, heaps, binary search, dynamic programming, strings, and linked lists. These remain candidates and must be verified against their source pages before acceptance. Examples reviewed during this pass include:
- https://leetcode.com/discuss/post/7344078/amazon-sde-1-interview-experience-dsa-ro-mxfs/
- https://leetcode.com/discuss/post/6915570/amazon-sde-1-interview-experience-2025-o-r3jt/
- https://leetcode.com/discuss/post/1191068/Amazon-SDE-1-Interview-Experience/
- https://leetcode.com/discuss/post/6414650/Amazon-SDE-1-Interview-Experience-or-February-2025-or-Offer-Received/
- https://www.geeksforgeeks.org/interview-experiences/amazon-interview-experience-for-sde-1-25/
- https://www.geeksforgeeks.org/interview-experiences/amazon-interview-experience-sde-1-2/

The official VIT PDF download was attempted from the current execution environment but could not be retrieved because outbound DNS/network access was unavailable. The user's library copy was available, so a 21-row Discipline Core catalog was extracted and committed. The original PDF binary is still not stored in the repository, and full syllabus text/topic extraction remains pending.

### Additional implementation pass (2026-10-10)

- Extracted the user's available VIT CSE 2024-25 syllabus PDF into a structured Discipline Core catalog at `data/raw/syllabi/vit_cse_2024_2025_discipline_core_catalog.csv` (21 rows, printed page 2). The original PDF binary is not committed, and this is not a full topic-level syllabus extraction.
- Expanded the source-linked mapping candidate list from 84 to 109 rows using additional publicly indexed interview reports. All remain `needs_human_review`; the count does not satisfy the manual-verification gate.
- Updated the evaluator to reject unreviewed labels by default and include per-topic diagnostics.

### Final status

**Not complete / not accepted yet.** No ground-truth rows have been promoted to verified, because a model-generated label cannot honestly be represented as a human reviewer’s approval. The 109 candidate mapping rows are for review only. Phase 2 sources also remain pending legal-use and independent-report checks. The readiness checker is intended to fail closed until these conditions are met.

To finish the remaining external/manual gates, a human reviewer with access to the original pages must:
1. Review current terms/permission and independence for at least 15 eligible interview reports and set review fields only when supported.
2. Download the official PDF locally using `python scripts/download_vit_syllabus.py`, validate text extraction, and commit the PDF only if permitted by its terms; otherwise keep the official source URL and record the access decision.
3. Verify at least 200 source-backed mappings one by one, mark them reviewed with a real reviewer identity/date, and ensure taxonomy labels are supported by each source.
4. Run `python scripts/check_phase_readiness.py`, fix any remaining gates, then run `python evaluation/evaluate_nlp.py --data evaluation/ground_truth.csv --taxonomy data/taxonomy/taxonomy_v1.1.json`. Review split integrity and save the resulting metrics only if all preconditions pass.
