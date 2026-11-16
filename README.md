# DASS — Dynamic Shooting Simulation System

**An Advanced High-Fidelity Electromechanical Training Platform with Integrated 3D Ballistics Engine**

*Prepared by: Ayça Bahar Güner — Department of Mechanical Engineering, Dokuz Eylül University*

-----

## Problem

Live-fire training is expensive, logistically heavy, and environmentally hazardous. Existing simulation alternatives (laser tag systems) fail on three counts: no kinetic recoil feedback, straight-line light trajectories that ignore real ballistics, and chassis geometry that doesn’t match actual weapon inertia. DASS eliminates these compromises without live ammunition.

## System Architecture

DASS integrates three electromechanical modules:

**1. Pneumatic Recoil Module**
A high-pressure (6–8 bar) pneumatic piston drives an engineered inertia mass along linear guide rails, replicating the authentic impulse curve of standard-issue weapons. Recoil energy: 6–10 J (adjustable per platform).

**2. IR Optical Target Tracking**
A focused 940nm IR beam (≤1cm spot at range) strikes a structural target plate. Impact coordinates are resolved via a four-quadrant piezoelectric TDoA matrix with millimeter-level precision (target: ±5mm at 50m).

**3. Real-Time 3D Ballistics Engine**
Rather than accepting the straight-line IR path, the software intercepts weapon orientation from a 9-axis IMU (Kalman-filtered) and solves full equations of motion including aerodynamic drag, gravity drop, crosswind drift, and Magnus effect. Numerical integration via Euler-Cromer (symplectic, energy-conserving).

## Ballistics Model

```
a⃗ = (F⃗_drag / m) + g⃗

F⃗_drag = -0.5 · ρ · ||v⃗_rel||² · Cd · A · (v⃗_rel / ||v⃗_rel||)
```

Environmental parameters (air density, wind, temperature) are dynamically adjustable. Drag coefficient is Mach-dependent with transonic breakpoint correction.

## Monte Carlo Validation

System accuracy is validated via stochastic simulation (n=300 shots) with realistic noise sources:

|Noise Source   |1-sigma|
|---------------|-------|
|IMU pitch/yaw  |0.05°  |
|IMU roll       |0.20°  |
|Muzzle velocity|3.0 m/s|
|Wind gust      |0.5 m/s|

Two CEP metrics are reported:

- **Mean-centered CEP** — grouping quality, independent of zero offset
- **Target-centered CEP** — operational accuracy including systematic bias

## Performance Targets

|Parameter          |Conventional Laser|DASS Target                    |
|-------------------|------------------|-------------------------------|
|Recoil feedback    |None              |6–10 J pneumatic               |
|End-to-end latency |>80 ms            |<18 ms                         |
|Hit precision @50m |±50 mm            |±5 mm                          |
|Environmental model|Static            |Dynamic drag, wind, temperature|
|Communication      |Bluetooth/Wi-Fi   |ESP-NOW (Layer-2, <20ms)       |

## Known Limitations

- `spin_axis` is held constant along the trajectory (gyroscopic precession not modeled). Effect is negligible at pistol ranges (<300m); sniper module will require dynamic spin integration.
- Euler-Cromer integration is sufficient for short-range pistol simulation. RK4 recommended for long-range platforms (v5 roadmap).
- Pneumatic reservoir capacity and recharge time under sustained fire not yet characterized.

## Running the Simulation

```bash
pip install numpy matplotlib
python dass_ballistics_v4.py
```

Outputs: trajectory CSV, Monte Carlo scatter CSV, summary plot.

## Peer Review Process

For independent, structured evaluation, see the [Peer Review Process](PEER_REVIEW.md) and submit a [Peer Review](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=peer-review.yml). Reviews should identify the exact commit examined and focus on software quality, reproducibility, documentation, and responsible-use safeguards.

## Feedback & Technical Review

Feedback is welcome from engineers, researchers, and users reviewing the DASS repository. To keep reports actionable, please use one of the structured GitHub issue forms:

- [Technical Review](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=technical-review.yml) — software architecture, numerical methods, model assumptions, validation, and documentation.
- [Bug Report](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=bug-report.yml) — reproducible software or documentation problems.
- [Research Feedback](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=research-feedback.yml) — methodology, reproducibility, validation design, and relevant literature.

Please include enough context to reproduce or assess your observation. Keep submissions focused on the repository's software and simulation scope, and do not post personal data, credentials, or sensitive operational information. Existing reports can be reviewed and discussed in the repository's [Issues](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues) tab.

---

## Changelog

|Version|Key Changes                                                                                                                                         |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------|
|v1     |Initial ballistics engine, basic drag model                                                                                                         |
|v2     |Acoustic TDoA target tracking prototype                                                                                                             |
|v3     |Paradigm shift: TDoA → IR optical tracking. DASScorrectionEngine (LoS vs PoI correction vector). Monte Carlo engine. Latency budget.                |
|v4     |Vectorized MC engine (removed per-shot instantiation). `poi_at_range` linear interpolation fix. Dual CEP reporting. spin_axis limitation documented.|
