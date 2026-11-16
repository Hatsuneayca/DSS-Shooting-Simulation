"""Synthetic device-health telemetry demo for the DASS project.

This module generates fictional session records for software development and
documentation. It does not connect to hardware, control actuators, model
weapon operation, or calculate aiming/trajectory/impact information.
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class TelemetrySample:
    elapsed_s: int
    battery_pct: float
    enclosure_temp_c: float
    connection_status: str
    sensor_status: str
    device_status: str
    event: str


def simulate_session(
    duration_s: int = 60,
    sample_period_s: int = 5,
    seed: int = 17,
) -> List[TelemetrySample]:
    """Generate deterministic, synthetic device-health records.

    Values are illustrative only. They are not measured hardware performance.
    """
    if isinstance(duration_s, bool) or not isinstance(duration_s, int):
        raise TypeError("duration_s must be an integer.")
    if isinstance(sample_period_s, bool) or not isinstance(sample_period_s, int):
        raise TypeError("sample_period_s must be an integer.")
    if duration_s <= 0 or duration_s > 3600:
        raise ValueError("duration_s must be between 1 and 3600 seconds.")
    if sample_period_s <= 0 or sample_period_s > duration_s:
        raise ValueError("sample_period_s must be positive and no greater than duration_s.")

    sample_count = duration_s // sample_period_s + 1
    if sample_count > 3601:
        raise ValueError("Requested session would generate too many records.")

    rng = random.Random(seed)
    battery = 100.0
    temperature = 23.0
    samples: List[TelemetrySample] = []

    for index in range(sample_count):
        elapsed = min(index * sample_period_s, duration_s)
        if index:
            battery = max(0.0, battery - rng.uniform(0.02, 0.08))
            temperature = min(
                45.0,
                max(18.0, temperature + rng.uniform(-0.15, 0.25)),
            )

        connection_status = "CONNECTED" if rng.random() >= 0.02 else "CHECK"
        sensor_status = "SIMULATED_OK" if rng.random() >= 0.01 else "CHECK"
        device_status = (
            "OK"
            if connection_status == "CONNECTED" and sensor_status == "SIMULATED_OK"
            else "ATTENTION"
        )
        event = "SESSION_START" if index == 0 else "TELEMETRY_SAMPLE"

        samples.append(
            TelemetrySample(
                elapsed_s=elapsed,
                battery_pct=round(battery, 2),
                enclosure_temp_c=round(temperature, 2),
                connection_status=connection_status,
                sensor_status=sensor_status,
                device_status=device_status,
                event=event,
            )
        )

    return samples


def export_csv(samples: Iterable[TelemetrySample], output_path: Path) -> Path:
    """Write synthetic telemetry samples to a CSV file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(TelemetrySample.__dataclass_fields__.keys())
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for sample in samples:
            writer.writerow(asdict(sample))

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a synthetic DASS device-health session log."
    )
    parser.add_argument("--duration", type=int, default=60, help="Session duration in seconds.")
    parser.add_argument("--interval", type=int, default=5, help="Sampling interval in seconds.")
    parser.add_argument("--seed", type=int, default=17, help="Random seed for repeatable demo data.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/demo_session.csv"),
        help="CSV output path.",
    )
    args = parser.parse_args()

    records = simulate_session(args.duration, args.interval, args.seed)
    output = export_csv(records, args.output)
    print(f"Generated {len(records)} synthetic records: {output}")
    print("Demo data only: no hardware is connected or controlled.")


if __name__ == "__main__":
    main()
