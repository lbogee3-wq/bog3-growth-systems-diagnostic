"""Deliberately naïve first pass, retained as an auditable learning artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def run_v1(assessment: dict[str, Any]) -> dict[str, Any]:
    """Average supplied scores and list the three lowest dimensions.

    This version intentionally does not validate completeness, distinguish evidence
    quality, or detect relationships between dimensions.
    """
    scores = {
        key: value["score"] for key, value in assessment["dimensions"].items()
    }
    overall = round(sum(scores.values()) / len(scores) / 4 * 100, 1)
    lowest = sorted(scores, key=scores.get)[:3]
    return {
        "assessment_name": assessment["assessment_name"],
        "synthetic": assessment.get("synthetic", False),
        "overall_score": overall,
        "lowest_dimensions": lowest,
        "warning": "V1 is an unvalidated arithmetic baseline, not a complete diagnostic."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    assessment = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(run_v1(assessment), indent=2))


if __name__ == "__main__":
    main()

