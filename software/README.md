# DASS Software Demonstrator

The active Python demonstrator is a local, dependency-free simulation of generic electronic device health. It creates clearly labelled synthetic telemetry, session summaries and repeated scenario-analysis records.

## Run

From the repository root:

```bash
python -m software.dass_telemetry_demo
python -m unittest discover -s tests -v
```

Example with a shorter session:

```bash
python -m software.dass_telemetry_demo --duration 120 --interval 5 --seed 17 --runs 50 --output-dir outputs
```

## Software modules

- `DeviceConfig`: explicit, validated assumptions for a generic electronic device.
- `DeviceHealthSimulator`: creates deterministic synthetic battery, enclosure-temperature, connection and sensor-status records.
- `ScenarioMonteCarloEvaluator`: repeats the synthetic scenario using independent seeds and summarizes the resulting variation.
- CSV export functions: write telemetry, session summaries and scenario results for later review.

## Output files

- `session_telemetry.csv`: time-indexed synthetic device-health records.
- `session_summary.csv`: summary of one synthetic session.
- `scenario_trials.csv`: one row per repeated synthetic scenario.
- `scenario_summary.csv`: aggregate statistics across the repeated scenarios.

All probabilities, battery drain values and temperature changes are illustrative software assumptions. They are not measured failure rates, battery specifications, thermal predictions or field reliability claims. The code does not connect to hardware, control actuators, or calculate weapon-operation, aiming, trajectory, impact or recoil information.
