#!/usr/bin/env python3
"""Human-in-the-loop review for Prepline Phase 13 mapping candidates.

This tool never auto-approves a label. A reviewer must inspect each prompt,
source, and taxonomy topic and explicitly approve/reject/defer it.
Run from repository root:
    python scripts/review_phase13_candidates.py
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUTS = [
    ROOT / "evaluation/codeprep_mappings_for_review.csv",
    ROOT / "evaluation/source_backed_mappings_for_review.csv",
]
DEFAULT_OUTPUT = ROOT / "evaluation/ground_truth.csv"
FIELDS = [
    "raw_text", "expected_topic_id", "taxonomy_version", "source_id",
    "source_type", "source_url", "review_status", "reviewer", "review_date", "notes"
]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", default=[str(p) for p in DEFAULT_INPUTS])
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--taxonomy", default=str(ROOT / "data/taxonomy/taxonomy_v1.1.json"))
    parser.add_argument("--reviewer", default="")
    args = parser.parse_args()

    reviewer = args.reviewer.strip() or input("Reviewer name/identifier: ").strip()
    if not reviewer:
        parser.error("A reviewer identifier is required.")
    taxonomy = json.loads(Path(args.taxonomy).read_text(encoding="utf-8"))
    version = taxonomy.get("taxonomy_version", "unknown")
    topics = {t["topic_id"]: t for t in taxonomy.get("topics", [])}
    candidates = []
    for source in args.inputs:
        path = Path(source)
        if path.exists():
            candidates.extend(load_csv(path))
        else:
            print(f"Skipping missing input: {path}")

    output = Path(args.output)
    existing = load_csv(output) if output.exists() else []
    seen = {(r.get("raw_text", "").strip().casefold(), r.get("expected_topic_id", "").strip()) for r in existing}
    accepted = [r for r in existing if r.get("review_status", "").strip().lower() in {"verified", "approved"}]
    accepted_keys = {(r.get("raw_text", "").strip().casefold(), r.get("expected_topic_id", "").strip()) for r in accepted}
    pending = [r for r in candidates if (r.get("raw_text", "").strip().casefold(), r.get("expected_topic_id", "").strip()) not in seen]
    print(f"Taxonomy {version}: {len(topics)} topics; {len(pending)} new candidates; {len(accepted)} already accepted labels.")
    print("For every approval, inspect the original source and confirm both source eligibility and taxonomy fit.")
    for index, row in enumerate(pending, start=1):
        topic_id = row.get("expected_topic_id", "").strip()
        if topic_id not in topics:
            print(f"SKIP invalid taxonomy ID: {topic_id}")
            continue
        print("\n" + "=" * 78)
        print(f"[{index}/{len(pending)}] {row.get('source_id','')} | {topic_id} — {topics[topic_id].get('name','')}")
        print("Prompt:", row.get("raw_text", ""))
        print("Source:", row.get("source_url", ""))
        print("Notes:", row.get("notes", ""))
        print("Check the source page and applicable license/permission before approval.")
        choice = input("[a]pprove / [r]eject / [s]kip / [q]uit: ").strip().lower()
        if choice == "q":
            break
        if choice not in {"a", "r"}:
            continue
        review_date = date.today().isoformat()
        note = input("Review note (optional): ").strip()
        record = {key: str(row.get(key, "") or "") for key in FIELDS}
        record["taxonomy_version"] = version
        record["review_status"] = "verified" if choice == "a" else "rejected"
        record["reviewer"] = reviewer
        record["review_date"] = review_date
        record["notes"] = (record.get("notes", "") + (" | " if record.get("notes") else "") + f"Human review: {note}").strip()
        existing.append(record)
        key = (record["raw_text"].strip().casefold(), record["expected_topic_id"].strip())
        seen.add(key)
        if choice == "a":
            accepted_keys.add(key)
        write_csv(output, existing)
        print(f"Saved {record['review_status']} label to {output}")
    print(f"\nSaved {len(existing)} reviewed/candidate records; {len(accepted_keys)} currently accepted unique pairs.")
    print("This is not a complete benchmark until 200+ distinct labels are approved and source eligibility is confirmed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
