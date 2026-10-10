"""Check Phase 2 and Phase 13 completion gates without treating candidates as verified.

Run from repository root:
    python scripts/check_phase_readiness.py

This script deliberately reports NOT READY if source/legal/human-review gates are open.
It does not perform legal review or substitute for a human annotator.
"""
from pathlib import Path
import csv
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
INTERVIEWS = ROOT / "data/raw/interviews/amazon_sde1_interview_experiences_phase2.csv"
GROUND_TRUTH = ROOT / "evaluation/ground_truth.csv"
CANDIDATES = ROOT / "evaluation/source_backed_mappings_for_review.csv"
TAXONOMY = ROOT / "data/taxonomy/taxonomy_v1.1.json"
SYLLABUS = ROOT / "data/raw/syllabi/VIT_CSE_2024_2025.pdf"

def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def main():
    failures = []
    interview_rows = read_csv(INTERVIEWS) if INTERVIEWS.exists() else []
    eligible = [
        row for row in interview_rows
        if row.get("deduplication_status", "").strip().lower() in {"unique", "confirmed unique", "verified unique"}
        and row.get("source_review_status", "").strip().lower() in {"reviewed", "approved", "verified"}
        and row.get("legal_review_status", "").strip().lower() in {"approved", "permitted", "cleared"}
    ]
    unique_ids = {row.get("report_id", "").strip() for row in eligible if row.get("report_id", "").strip()}
    print(f"Phase 2: {len(unique_ids)} reports currently satisfy all explicit acceptance fields (minimum 15).")
    if len(unique_ids) < 15:
        failures.append("Phase 2: fewer than 15 reports have confirmed unique, source-reviewed, legally cleared status.")
    if not SYLLABUS.exists():
        failures.append("Phase 2: official syllabus PDF is not present at data/raw/syllabi/VIT_CSE_2024_2025.pdf.")
    elif SYLLABUS.stat().st_size < 100_000:
        failures.append("Phase 2: syllabus PDF exists but is unexpectedly small; validate the download.")

    if not TAXONOMY.exists():
        failures.append("Phase 13: taxonomy v1.1 file is missing.")
        valid_topic_ids = set()
    else:
        taxonomy = json.loads(TAXONOMY.read_text(encoding="utf-8"))
        valid_topic_ids = {topic["topic_id"] for topic in taxonomy.get("topics", [])}

    candidates = read_csv(CANDIDATES) if CANDIDATES.exists() else []
    candidate_pairs = {
        (row.get("raw_text", "").strip().casefold(), row.get("expected_topic_id", "").strip())
        for row in candidates
        if row.get("raw_text", "").strip() and row.get("expected_topic_id", "").strip() in valid_topic_ids
    }
    print(f"Phase 13 candidate pool: {len(candidates)} rows; {len(candidate_pairs)} unique valid text/topic pairs (candidates do not satisfy the verified-label gate).")

    labels = read_csv(GROUND_TRUTH) if GROUND_TRUTH.exists() else []
    accepted = []
    for row in labels:
        if (
            row.get("review_status", "").strip().lower() in {"verified", "approved"}
            and row.get("reviewer", "").strip()
            and row.get("review_date", "").strip()
            and row.get("source_url", "").strip()
            and row.get("raw_text", "").strip()
            and row.get("expected_topic_id", "").strip() in valid_topic_ids
            and row.get("taxonomy_version", "").strip() == "v1.1"
        ):
            accepted.append(row)
    print(f"Phase 13: {len(accepted)} rows currently satisfy the explicit accepted-label fields (minimum 200).")
    if len(accepted) < 200:
        failures.append("Phase 13: fewer than 200 source-backed mappings have explicit verified/approved review fields.")
    if len(accepted) >= 200:
        keys = {(r["raw_text"].strip().casefold(), r["expected_topic_id"].strip()) for r in accepted}
        if len(keys) < 200:
            failures.append("Phase 13: fewer than 200 unique text/topic pairs remain after deduplication.")

    if failures:
        print("\nNOT READY:")
        for failure in failures:
            print(f"- {failure}")
        print("\nDo not report final benchmark metrics until every gate is satisfied.")
        return 1
    print("\nReadiness fields pass. Independently confirm reviewer work and run the evaluation on the frozen dataset.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
