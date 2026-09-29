import unittest

from scripts.analyze_score_sensitivity import (
    aggregate,
    grade_configuration,
    percentile_midrank,
    spearman,
)


class ScoreSensitivityHelpersTest(unittest.TestCase):
    def test_percentile_midrank_preserves_ties(self):
        scores = percentile_midrank({"a": 10, "b": 20, "c": 20, "d": 40})
        self.assertEqual(scores["a"], 12.5)
        self.assertEqual(scores["b"], scores["c"])
        self.assertEqual(scores["d"], 87.5)

    def test_inverse_percentile(self):
        scores = percentile_midrank({"a": 10, "b": 20}, higher_is_better=False)
        self.assertGreater(scores["a"], scores["b"])

    def test_spearman_detects_reversal(self):
        self.assertAlmostEqual(spearman({"a": 1, "b": 2, "c": 3}, {"a": 3, "b": 2, "c": 1}), -1)

    def test_aggregate_requires_requested_component_count(self):
        components = {"all": {"a": 10, "b": 20, "c": 30}, "two": {"a": 10, "b": 20}}
        weights = {"a": 0.4, "b": 0.3, "c": 0.3}
        self.assertEqual(set(aggregate(components, weights, 3)), {"all"})
        self.assertEqual(set(aggregate(components, weights, 2)), {"all", "two"})

    def test_grade_configuration(self):
        self.assertEqual(grade_configuration({**{f"ÅR{i}": "J" for i in range(1, 7)}}), "grades 1–6")
        self.assertEqual(grade_configuration({**{f"ÅR{i}": "J" for i in range(1, 10)}}), "grades 1–9")
        self.assertEqual(grade_configuration({**{f"ÅR{i}": "J" for i in range(7, 10)}}), "grades 7–9")


if __name__ == "__main__":
    unittest.main()
