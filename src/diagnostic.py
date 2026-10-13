"""Small, auditable growth-systems diagnostic using only Python's standard library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_FRAMEWORK = ROOT / "framework.json"


class ValidationError(ValueError):
    """Raised when an assessment cannot be scored safely."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"Expected a JSON object in {path}")
    return value


def validate(assessment: dict[str, Any], framework: dict[str, Any]) -> None:
    required_top = {"assessment_name", "assessment_date", "synthetic", "context", "dimensions"}
    missing_top = sorted(required_top - assessment.keys())
    if missing_top:
        raise ValidationError(f"Missing top-level fields: {', '.join(missing_top)}")
    if not isinstance(assessment["synthetic"], bool):
        raise ValidationError("synthetic must be true or false")

    expected = set(framework["dimensions"])
    supplied = set(assessment["dimensions"])
    missing = sorted(expected - supplied)
    extra = sorted(supplied - expected)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing dimensions: {', '.join(missing)}")
        if extra:
            details.append(f"unknown dimensions: {', '.join(extra)}")
        raise ValidationError("; ".join(details))

    for key, value in assessment["dimensions"].items():
        if not isinstance(value, dict):
            raise ValidationError(f"{key} must be an object")
        for field in ("score", "evidence_quality", "observations", "evidence", "risks", "actions"):
            if field not in value:
                raise ValidationError(f"{key} is missing {field}")
        if not isinstance(value["score"], int) or not 0 <= value["score"] <= 4:
            raise ValidationError(f"{key}.score must be an integer from 0 to 4")
        if not isinstance(value["evidence_quality"], int) or not 0 <= value["evidence_quality"] <= 3:
            raise ValidationError(f"{key}.evidence_quality must be an integer from 0 to 3")
        for field in ("observations", "evidence", "risks", "actions"):
            if not isinstance(value[field], list) or not all(isinstance(item, str) for item in value[field]):
                raise ValidationError(f"{key}.{field} must be a list of strings")

    weights = [item["weight"] for item in framework["dimensions"].values()]
    if any(not isinstance(weight, (int, float)) or weight <= 0 for weight in weights):
        raise ValidationError("Every framework weight must be a positive number")


def maturity_band(score: float) -> str:
    if score < 25:
        return "absent-to-reactive"
    if score < 50:
        return "reactive-to-defined"
    if score < 75:
        return "defined-to-managed"
    return "managed-to-adaptive"


def evidence_label(score: float) -> str:
    if score < 35:
        return "low"
    if score < 70:
        return "moderate"
    return "strong"


def system_warnings(assessment: dict[str, Any]) -> list[dict[str, str]]:
    dims = assessment["dimensions"]
    warnings: list[dict[str, str]] = []
    if dims["measurement_data_quality"]["score"] <= 1 and any(
        item["score"] >= 3 for key, item in dims.items() if key != "measurement_data_quality"
    ):
        warnings.append({
            "rule": "strong_claims_weak_measurement",
            "interpretation": "Higher maturity claims elsewhere may be difficult to verify because measurement maturity is low."
        })
    if dims["conversion"]["score"] >= 2 and dims["lifecycle_follow_up"]["score"] <= 1:
        warnings.append({
            "rule": "conversion_without_follow_up",
            "interpretation": "Initial demand may be created without a reliable follow-up system, creating avoidable leakage."
        })
    if dims["organizational_process_alignment"]["score"] <= 1:
        warnings.append({
            "rule": "execution_alignment_risk",
            "interpretation": "Tool or channel improvements may not persist until ownership and operating rhythms are clearer."
        })
    return warnings


def diagnose(assessment: dict[str, Any], framework: dict[str, Any]) -> dict[str, Any]:
    validate(assessment, framework)
    dimensions = []
    weighted_maturity = 0.0
    weighted_evidence = 0.0
    total_weight = sum(item["weight"] for item in framework["dimensions"].values())

    for key, definition in framework["dimensions"].items():
        entry = assessment["dimensions"][key]
        weight_share = definition["weight"] / total_weight
        maturity = entry["score"] / 4 * 100
        evidence = entry["evidence_quality"] / 3 * 100
        # Priority is a transparent blend of capability gap and evidence uncertainty.
        priority = round((100 - maturity) * 0.7 + (100 - evidence) * 0.3, 1)
        weighted_maturity += maturity * weight_share
        weighted_evidence += evidence * weight_share
        dimensions.append({
            "key": key,
            "label": definition["label"],
            "score": entry["score"],
            "maturity_percent": round(maturity, 1),
            "evidence_quality": entry["evidence_quality"],
            "evidence_label": evidence_label(evidence),
            "priority_score": priority,
            "observations": entry["observations"],
            "evidence": entry["evidence"],
            "risks": entry["risks"],
            "actions": entry["actions"]
        })

    priorities = [
        {
            "dimension": item["key"],
            "label": item["label"],
            "priority_score": item["priority_score"],
            "why": "Rank reflects 70% maturity gap and 30% evidence uncertainty; it is a triage aid, not proof of business impact.",
            "candidate_actions": item["actions"]
        }
        for item in sorted(dimensions, key=lambda item: (-item["priority_score"], item["key"]))[:3]
    ]

    overall = round(weighted_maturity, 1)
    evidence_coverage = round(weighted_evidence, 1)
    return {
        "diagnostic_version": framework["version"],
        "assessment": {
            "name": assessment["assessment_name"],
            "date": assessment["assessment_date"],
            "synthetic": assessment["synthetic"],
            "context": assessment["context"]
        },
        "summary": {
            "overall_maturity_score": overall,
            "maturity_band": maturity_band(overall),
            "evidence_coverage": evidence_coverage,
            "evidence_confidence": evidence_label(evidence_coverage),
            "interpretation": "Maturity and evidence are reported separately. Neither score is a benchmark or causal finding."
        },
        "dimensions": dimensions,
        "priorities": priorities,
        "system_warnings": system_warnings(assessment),
        "limitations": [
            "Scores reflect assessor judgment against descriptive anchors.",
            "Default weights are equal and have not been empirically calibrated.",
            "Priority ranking estimates gaps and uncertainty, not financial impact or causality.",
            "The diagnostic is a structured hypothesis generator; validate findings with stakeholders and source systems."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Assessment JSON file")
    parser.add_argument("--framework", type=Path, default=DEFAULT_FRAMEWORK)
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    try:
        result = diagnose(load_json(args.input), load_json(args.framework))
    except ValidationError as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()

