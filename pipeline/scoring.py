"""Coverage scoring helpers for Prepline; scores describe mappings, not student readiness."""
from __future__ import annotations

from collections import Counter
from typing import Iterable


def topic_coverage(syllabus_topic_ids: Iterable[str], interview_topic_ids: Iterable[str]) -> dict:
    """Compute simple unique-topic coverage and interview-topic gaps."""
    syllabus = set(syllabus_topic_ids)
    interview = list(interview_topic_ids)
    counts = Counter(interview)
    unique_interview = set(counts)
    covered = unique_interview & syllabus
    gaps = unique_interview - syllabus
    denominator = len(unique_interview)
    return {
        "coverage_ratio": len(covered) / denominator if denominator else 0.0,
        "coverage_percent": round(100 * len(covered) / denominator, 2) if denominator else 0.0,
        "unique_interview_topics": denominator,
        "covered_topics": sorted(covered),
        "gap_topics": sorted(gaps),
        "interview_frequency": dict(sorted(counts.items())),
        "interpretation": "Topic overlap only; not a measure of course depth, interview probability, or student proficiency.",
    }


def weighted_coverage(syllabus_weights: dict[str, float], interview_topic_ids: Iterable[str]) -> dict:
    """Weight each unique interview topic by a non-negative importance weight."""
    if any(float(weight) < 0 for weight in syllabus_weights.values()):
        raise ValueError("Syllabus weights must be non-negative")
    interview = set(interview_topic_ids)
    if not interview:
        return {"coverage_ratio": 0.0, "coverage_percent": 0.0, "covered_topics": [], "gap_topics": []}
    weights = {topic: float(syllabus_weights.get(topic, 0.0)) for topic in interview}
    total = sum(weights.values())
    covered = sorted(topic for topic in interview if weights[topic] > 0)
    # Zero weight means absent from the mapped syllabus; positive weight means present.
    if total == 0:
        return {"coverage_ratio": 0.0, "coverage_percent": 0.0, "covered_topics": [], "gap_topics": sorted(interview)}
    covered_weight = sum(weights[topic] for topic in covered)
    return {"coverage_ratio": covered_weight / total,
            "coverage_percent": round(100 * covered_weight / total, 2),
            "covered_topics": covered, "gap_topics": sorted(interview - set(covered))}
