import unittest

from scripts.audit_school_data import column_index, normalize_code, systematic_sample


class AuditHelpersTest(unittest.TestCase):
    def test_column_index(self):
        self.assertEqual(column_index("A1"), 0)
        self.assertEqual(column_index("Z9"), 25)
        self.assertEqual(column_index("AA10"), 26)

    def test_normalize_school_unit_code(self):
        self.assertEqual(normalize_code("01234567"), "01234567")
        self.assertEqual(normalize_code("12345678.0"), "12345678")
        self.assertIsNone(normalize_code("123"))

    def test_systematic_sample_is_deterministic_and_bounded(self):
        self.assertEqual(systematic_sample(["a", "b", "c", "d"], 2), ["a", "c"])
        self.assertEqual(systematic_sample(["a", "b"], 8), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
