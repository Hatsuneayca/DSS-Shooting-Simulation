"""Unit tests for the synthetic DASS device-health demonstrator."""

import csv
import tempfile
import unittest
from pathlib import Path

from software.dass_telemetry_demo import (
    DeviceConfig,
    DeviceHealthSimulator,
    ScenarioMonteCarloEvaluator,
    export_session_result,
)


class DeviceHealthSimulatorTests(unittest.TestCase):
    def test_session_is_deterministic_for_same_seed(self):
        config = DeviceConfig(duration_s=20, sample_period_s=5)
        first = DeviceHealthSimulator(config, seed=42).run()
        second = DeviceHealthSimulator(config, seed=42).run()
        self.assertEqual(first, second)

    def test_exact_final_timestamp_is_included(self):
        result = DeviceHealthSimulator(
            DeviceConfig(duration_s=22, sample_period_s=5), seed=1
        ).run()
        self.assertEqual(result.samples[-1].elapsed_s, 22)

    def test_all_samples_are_marked_synthetic(self):
        result = DeviceHealthSimulator(DeviceConfig(duration_s=10), seed=1).run()
        self.assertTrue(all(sample.data_origin == "SYNTHETIC" for sample in result.samples))

    def test_zero_dropout_and_sensor_warning_produce_clean_status(self):
        config = DeviceConfig(
            duration_s=30,
            sample_period_s=5,
            connection_dropout_probability=0.0,
            sensor_warning_probability=0.0,
        )
        result = DeviceHealthSimulator(config, seed=8).run()
        self.assertEqual(result.summary.session_status, "OK")
        self.assertEqual(result.summary.connection_availability_pct, 100.0)
        self.assertEqual(result.summary.sensor_ok_pct, 100.0)

    def test_certain_dropout_is_reported(self):
        config = DeviceConfig(
            duration_s=10,
            sample_period_s=5,
            connection_dropout_probability=1.0,
        )
        result = DeviceHealthSimulator(config, seed=8).run()
        self.assertEqual(result.summary.connection_availability_pct, 0.0)
        self.assertEqual(result.summary.session_status, "ATTENTION")

    def test_invalid_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            DeviceHealthSimulator(DeviceConfig(duration_s=0))

    def test_monte_carlo_is_repeatable(self):
        config = DeviceConfig(duration_s=30, sample_period_s=5)
        first = ScenarioMonteCarloEvaluator(config, runs=5, seed=100).run()
        second = ScenarioMonteCarloEvaluator(config, runs=5, seed=100).run()
        self.assertEqual(first, second)

    def test_csv_exports_session_and_summary(self):
        result = DeviceHealthSimulator(
            DeviceConfig(duration_s=10, sample_period_s=5)
        ).run()
        with tempfile.TemporaryDirectory() as temp_dir:
            telemetry_path, summary_path = export_session_result(result, Path(temp_dir))
            with telemetry_path.open(newline="", encoding="utf-8") as handle:
                telemetry_rows = list(csv.DictReader(handle))
            with summary_path.open(newline="", encoding="utf-8") as handle:
                summary_rows = list(csv.DictReader(handle))
            self.assertEqual(len(telemetry_rows), 3)
            self.assertEqual(len(summary_rows), 1)
            self.assertEqual(telemetry_rows[0]["data_origin"], "SYNTHETIC")


if __name__ == "__main__":
    unittest.main()
