import copy
import json
import unittest
from pathlib import Path

from src.diagnostic import ValidationError, diagnose


ROOT = Path(__file__).resolve().parents[1]


class DiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = json.loads((ROOT / "src/framework.json").read_text())
        cls.sample = json.loads((ROOT / "data/sample_bog3_synthetic.json").read_text())

    def test_sample_produces_separate_maturity_and_evidence_scores(self):
        result = diagnose(self.sample, self.framework)
        self.assertEqual(result["summary"]["overall_maturity_score"], 39.3)
        self.assertEqual(result["summary"]["evidence_coverage"], 52.4)
        self.assertTrue(result["assessment"]["synthetic"])

    def test_priority_order_is_deterministic(self):
        result = diagnose(self.sample, self.framework)
        self.assertEqual(
            [item["dimension"] for item in result["priorities"]],
            ["lifecycle_follow_up", "crm_martech", "organizational_process_alignment"]
        )

    def test_missing_dimension_is_rejected(self):
        invalid = copy.deepcopy(self.sample)
        del invalid["dimensions"]["conversion"]
        with self.assertRaisesRegex(ValidationError, "missing dimensions: conversion"):
            diagnose(invalid, self.framework)

    def test_out_of_range_score_is_rejected(self):
        invalid = copy.deepcopy(self.sample)
        invalid["dimensions"]["conversion"]["score"] = 5
        with self.assertRaisesRegex(ValidationError, "score must be an integer from 0 to 4"):
            diagnose(invalid, self.framework)

    def test_cross_system_warning_is_explicit(self):
        altered = copy.deepcopy(self.sample)
        altered["dimensions"]["measurement_data_quality"]["score"] = 1
        altered["dimensions"]["acquisition_discovery"]["score"] = 3
        result = diagnose(altered, self.framework)
        self.assertIn("strong_claims_weak_measurement", [item["rule"] for item in result["system_warnings"]])


if __name__ == "__main__":
    unittest.main()

