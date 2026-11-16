"""Unit tests for the synthetic DASS telemetry demo."""

import csv
import tempfile
import unittest
from pathlib import Path

from software.dass_telemetry_demo import export_csv, simulate_session


class TelemetryDemoTests(unittest.TestCase):
    def test_output_is_deterministic_for_same_seed(self):
        first = simulate_session(duration_s=20, sample_period_s=5, seed=42)
        second = simulate_session(duration_s=20, sample_period_s=5, seed=42)
        self.assertEqual(first, second)

    def test_sample_count_includes_start_sample(self):
        samples = simulate_session(duration_s=20, sample_period_s=5)
        self.assertEqual(len(samples), 5)
        self.assertEqual(samples[0].event, "SESSION_START")

    def test_includes_exact_final_timestamp_for_non_divisible_duration(self):
        samples = simulate_session(duration_s=22, sample_period_s=5)
        self.assertEqual(samples[-1].elapsed_s, 22)

    def test_rejects_invalid_duration(self):
        with self.assertRaises(ValueError):
            simulate_session(duration_s=0)

    def test_exports_csv(self):
        samples = simulate_session(duration_s=10, sample_period_s=5)
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "nested" / "session.csv"
            written = export_csv(samples, destination)
            self.assertTrue(written.exists())
            with written.open(newline="", encoding="utf-8") as csv_file:
                rows = list(csv.DictReader(csv_file))
            self.assertEqual(len(rows), 3)
            self.assertIn("device_status", rows[0])


if __name__ == "__main__":
    unittest.main()
