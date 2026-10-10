# Prepline

Prepline compares college curriculum coverage with company interview topics and highlights preparation gaps.

## Current implementation status

Phase 2 and Phase 13 are **in progress, not accepted as complete**. The repository contains candidate datasets and evaluation tooling, but acceptance requires source review, independent-report checks, and human-verified labels.

- [Phase 2 / Phase 13 status](PHASE2_PHASE13_STATUS.md)
- [Interview report index](data/raw/interviews/amazon_sde1_interview_experiences_phase2.csv)
- [VIT CSE course catalog extract](data/raw/syllabi/vit_cse_2024_2025_discipline_core_catalog.csv)
- [Taxonomy v1.1](data/taxonomy/taxonomy_v1.1.json)
- [Phase 13 candidate mappings (202 unique text/topic pairs)](evaluation/source_backed_mappings_for_review.csv)
- [Ground-truth benchmark template](evaluation/ground_truth.csv)
- [Benchmark evaluator](evaluation/evaluate_nlp.py)
- [Readiness checker](scripts/check_phase_readiness.py)
- [Data validator](scripts/validate_prepline_data.py)
- [Automated data tests](tests/test_repository_data.py)
- [GitHub Actions validation workflow](.github/workflows/validate-data.yml)
- [Human review workflow](evaluation/HUMAN_REVIEW_WORKFLOW.md)
- [Phase 13 review CLI](scripts/review_phase13_candidates.py) (approved labels go to `ground_truth.csv`; all decisions go to `review_decisions.csv`)
- [Phase 2 contributor guide](data/raw/interviews/CONTRIBUTION_GUIDE.md)
- [Licensed CodePrep candidate mappings](evaluation/codeprep_mappings_for_review.csv)

## Important data-quality rule

The source-linked mappings are **candidates**, not verified ground truth. Do not report model accuracy, precision, recall, or F1 as benchmark results until at least 200 source-backed labels have been verified by a real reviewer, source provenance and permissions have been checked, and the final test split has remained untouched during model selection.

## Check readiness

Run from the repository root:

```bash
python scripts/check_phase_readiness.py
```

The checker fails closed while the explicit acceptance gates are open.
