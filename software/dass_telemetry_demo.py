"""Synthetic device-health and serviceability simulation for DASS.

This is an offline software demonstrator. It generates fictional device-health
telemetry and scenario-based reliability summaries. It does not connect to
hardware, control actuators, model weapon operation, or calculate aiming,
trajectory, impact, or recoil information. All rates and thresholds are
illustrative assumptions, not measured hardware characteristics.
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class DeviceConfig:
    """Illustrative assumptions for one generic electronic training device."""

    device_id: str = "DASS-DEV-001"
    duration_s: int = 300
    sample_period_s: int = 5
    initial_battery_pct: float = 100.0
    baseline_temp_c: float = 23.0
    battery_drain_pct_per_min: float = 0.35
    temperature_rise_c_per_min: float = 0.35
    connection_dropout_probability: float = 0.01
    sensor_warning_probability: float = 0.005
    battery_warning_pct: float = 20.0
    temperature_warning_c: float = 45.0

    def validate(self) -> None:
        if not self.device_id or not self.device_id.strip():
            raise ValueError("device_id must not be empty.")
        if isinstance(self.duration_s, bool) or not isinstance(self.duration_s, int):
            raise TypeError("duration_s must be an integer.")
        if isinstance(self.sample_period_s, bool) or not isinstance(self.sample_period_s, int):
            raise TypeError("sample_period_s must be an integer.")
        if self.duration_s <= 0 or self.duration_s > 3600:
            raise ValueError("duration_s must be between 1 and 3600 seconds.")
        if self.sample_period_s <= 0 or self.sample_period_s > self.duration_s:
            raise ValueError("sample_period_s must be positive and no greater than duration_s.")
        if not 0.0 <= self.initial_battery_pct <= 100.0:
            raise ValueError("initial_battery_pct must be in [0, 100].")
        if not 0.0 <= self.connection_dropout_probability <= 1.0:
            raise ValueError("connection_dropout_probability must be in [0, 1].")
        if not 0.0 <= self.sensor_warning_probability <= 1.0:
            raise ValueError("sensor_warning_probability must be in [0, 1].")
        if self.battery_drain_pct_per_min < 0.0:
            raise ValueError("battery_drain_pct_per_min must be non-negative.")
        if self.temperature_rise_c_per_min < 0.0:
            raise ValueError("temperature_rise_c_per_min must be non-negative.")


@dataclass(frozen=True)
class TelemetrySample:
    device_id: str
    elapsed_s: int
    battery_pct: float
    enclosure_temp_c: float
    connection_status: str
    sensor_status: str
    device_status: str
    event: str
    data_origin: str = "SYNTHETIC"


@dataclass(frozen=True)
class SessionSummary:
    device_id: str
    sample_count: int
    connection_availability_pct: float
    sensor_ok_pct: float
    minimum_battery_pct: float
    maximum_enclosure_temp_c: float
    attention_sample_count: int
    session_status: str
    data_origin: str = "SYNTHETIC"


@dataclass(frozen=True)
class MonteCarloTrial:
    trial_id: int
    seed: int
    connection_availability_pct: float
    sensor_ok_pct: float
    minimum_battery_pct: float
    maximum_enclosure_temp_c: float
    attention_sample_count: int
    session_status: str
    data_origin: str = "SYNTHETIC_SCENARIO"


@dataclass(frozen=True)
class MonteCarloSummary:
    trial_count: int
    mean_connection_availability_pct: float
    mean_sensor_ok_pct: float
    mean_minimum_battery_pct: float
    mean_maximum_enclosure_temp_c: float
    trials_without_attention_pct: float
    data_origin: str = "SYNTHETIC_SCENARIO"


@dataclass(frozen=True)
class SessionResult:
    samples: Sequence[TelemetrySample]
    summary: SessionSummary


class DeviceHealthSimulator:
    """Generate reproducible synthetic health telemetry for a generic device."""

    def __init__(self, config: DeviceConfig, seed: int = 17) -> None:
        config.validate()
        self.config = config
        self.seed = seed
        self._rng = random.Random(seed)

    def run(self) -> SessionResult:
        cfg = self.config
        timestamps = list(range(0, cfg.duration_s, cfg.sample_period_s))
        if not timestamps or timestamps[-1] != cfg.duration_s:
            timestamps.append(cfg.duration_s)
        if len(timestamps) > 3601:
            raise ValueError("Session would generate too many telemetry records.")

        battery = cfg.initial_battery_pct
        temperature = cfg.baseline_temp_c
        previous_connection = "CONNECTED"
        previous_sensor = "SIMULATED_OK"
        samples: List[TelemetrySample] = []

        for index, elapsed_s in enumerate(timestamps):
            if index:
                elapsed_min = (timestamps[index] - timestamps[index - 1]) / 60.0
                battery_drop = cfg.battery_drain_pct_per_min * elapsed_min
                battery_drop *= self._rng.uniform(0.85, 1.15)
                battery = max(0.0, battery - battery_drop)

                thermal_change = cfg.temperature_rise_c_per_min * elapsed_min
                thermal_change += self._rng.uniform(-0.08, 0.08) * max(elapsed_min, 0.1)
                temperature = min(70.0, max(10.0, temperature + thermal_change))

            connection = (
                "CHECK"
                if self._rng.random() < cfg.connection_dropout_probability
                else "CONNECTED"
            )
            sensor = (
                "CHECK"
                if self._rng.random() < cfg.sensor_warning_probability
                else "SIMULATED_OK"
            )

            events: List[str] = []
            if index == 0:
                events.append("SESSION_START")
            if connection != previous_connection:
                events.append("CONNECTION_LOST" if connection == "CHECK" else "CONNECTION_RESTORED")
            if sensor != previous_sensor:
                events.append("SENSOR_WARNING" if sensor == "CHECK" else "SENSOR_RECOVERED")
            if battery < cfg.battery_warning_pct:
                events.append("LOW_BATTERY")
            if temperature >= cfg.temperature_warning_c:
                events.append("HIGH_TEMPERATURE")
            if not events:
                events.append("TELEMETRY_SAMPLE")

            device_status = (
                "ATTENTION"
                if connection != "CONNECTED"
                or sensor != "SIMULATED_OK"
                or battery < cfg.battery_warning_pct
                or temperature >= cfg.temperature_warning_c
                else "OK"
            )
            samples.append(
                TelemetrySample(
                    device_id=cfg.device_id,
                    elapsed_s=elapsed_s,
                    battery_pct=round(battery, 2),
                    enclosure_temp_c=round(temperature, 2),
                    connection_status=connection,
                    sensor_status=sensor,
                    device_status=device_status,
                    event="|".join(events),
                )
            )
            previous_connection = connection
            previous_sensor = sensor

        summary = self._summarize(samples)
        return SessionResult(samples=tuple(samples), summary=summary)

    @staticmethod
    def _summarize(samples: Sequence[TelemetrySample]) -> SessionSummary:
        if not samples:
            raise ValueError("Cannot summarize an empty session.")
        total = len(samples)
        connected = sum(s.connection_status == "CONNECTED" for s in samples)
        sensor_ok = sum(s.sensor_status == "SIMULATED_OK" for s in samples)
        attention = sum(s.device_status == "ATTENTION" for s in samples)
        return SessionSummary(
            device_id=samples[0].device_id,
            sample_count=total,
            connection_availability_pct=round(100.0 * connected / total, 2),
            sensor_ok_pct=round(100.0 * sensor_ok / total, 2),
            minimum_battery_pct=round(min(s.battery_pct for s in samples), 2),
            maximum_enclosure_temp_c=round(max(s.enclosure_temp_c for s in samples), 2),
            attention_sample_count=attention,
            session_status="ATTENTION" if attention else "OK",
        )


class ScenarioMonteCarloEvaluator:
    """Run repeated synthetic device-health scenarios with independent seeds.

    This is a software demonstration of uncertainty analysis. It is not a
    field-reliability estimate and its probabilities are not measured rates.
    """

    def __init__(self, base_config: DeviceConfig, runs: int = 100, seed: int = 1000) -> None:
        base_config.validate()
        if isinstance(runs, bool) or not isinstance(runs, int):
            raise TypeError("runs must be an integer.")
        if runs < 1 or runs > 500:
            raise ValueError("runs must be between 1 and 500.")
        self.base_config = base_config
        self.runs = runs
        self.seed = seed

    def run(self) -> tuple[List[MonteCarloTrial], MonteCarloSummary]:
        trials: List[MonteCarloTrial] = []
        for run_index in range(self.runs):
            run_seed = self.seed + run_index
            result = DeviceHealthSimulator(self.base_config, seed=run_seed).run()
            summary = result.summary
            trials.append(
                MonteCarloTrial(
                    trial_id=run_index + 1,
                    seed=run_seed,
                    connection_availability_pct=summary.connection_availability_pct,
                    sensor_ok_pct=summary.sensor_ok_pct,
                    minimum_battery_pct=summary.minimum_battery_pct,
                    maximum_enclosure_temp_c=summary.maximum_enclosure_temp_c,
                    attention_sample_count=summary.attention_sample_count,
                    session_status=summary.session_status,
                )
            )

        summary = MonteCarloSummary(
            trial_count=len(trials),
            mean_connection_availability_pct=round(
                mean(t.connection_availability_pct for t in trials), 2
            ),
            mean_sensor_ok_pct=round(mean(t.sensor_ok_pct for t in trials), 2),
            mean_minimum_battery_pct=round(mean(t.minimum_battery_pct for t in trials), 2),
            mean_maximum_enclosure_temp_c=round(
                mean(t.maximum_enclosure_temp_c for t in trials), 2
            ),
            trials_without_attention_pct=round(
                100.0 * sum(t.attention_sample_count == 0 for t in trials) / len(trials), 2
            ),
        )
        return trials, summary


def export_dataclass_csv(records: Iterable[object], output_path: Path) -> Path:
    """Export dataclass records to CSV without requiring third-party packages."""
    rows = [asdict(record) for record in records]
    if not rows:
        raise ValueError("No records supplied for CSV export.")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def export_session_result(result: SessionResult, output_dir: Path) -> tuple[Path, Path]:
    output_dir = Path(output_dir)
    telemetry_path = export_dataclass_csv(
        result.samples, output_dir / "session_telemetry.csv"
    )
    summary_path = export_dataclass_csv(
        [result.summary], output_dir / "session_summary.csv"
    )
    return telemetry_path, summary_path


def export_monte_carlo_result(
    trials: Sequence[MonteCarloTrial], summary: MonteCarloSummary, output_dir: Path
) -> tuple[Path, Path]:
    output_dir = Path(output_dir)
    trials_path = export_dataclass_csv(trials, output_dir / "scenario_trials.csv")
    summary_path = export_dataclass_csv(
        [summary], output_dir / "scenario_summary.csv"
    )
    return trials_path, summary_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the synthetic DASS device-health software demonstration."
    )
    parser.add_argument("--device-id", default="DASS-DEV-001")
    parser.add_argument("--duration", type=int, default=300, help="Session duration in seconds (max 3600).")
    parser.add_argument("--interval", type=int, default=5, help="Telemetry interval in seconds.")
    parser.add_argument("--seed", type=int, default=17, help="Seed for the example session.")
    parser.add_argument("--runs", type=int, default=100, help="Synthetic scenario runs (1-500).")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    config = DeviceConfig(
        device_id=args.device_id,
        duration_s=args.duration,
        sample_period_s=args.interval,
    )
    session = DeviceHealthSimulator(config, seed=args.seed).run()
    telemetry_path, summary_path = export_session_result(session, args.output_dir)

    trials, mc_summary = ScenarioMonteCarloEvaluator(
        config, runs=args.runs, seed=args.seed + 1000
    ).run()
    trials_path, mc_summary_path = export_monte_carlo_result(
        trials, mc_summary, args.output_dir
    )

    print("DASS synthetic device-health demonstration")
    print(f"Device: {config.device_id} | samples: {session.summary.sample_count}")
    print(f"Session state: {session.summary.session_status}")
    print(f"Connection availability: {session.summary.connection_availability_pct:.2f}%")
    print(f"Sensor status OK: {session.summary.sensor_ok_pct:.2f}%")
    print(f"Minimum synthetic battery: {session.summary.minimum_battery_pct:.2f}%")
    print(f"Maximum synthetic enclosure temperature: {session.summary.maximum_enclosure_temp_c:.2f} C")
    print(f"Scenario runs without attention: {mc_summary.trials_without_attention_pct:.2f}%")
    print("All records are synthetic; no physical hardware is connected or controlled.")
    for path in (telemetry_path, summary_path, trials_path, mc_summary_path):
        print(f"CSV: {path}")


if __name__ == "__main__":
    main()
