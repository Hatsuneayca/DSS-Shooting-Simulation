# DASS System Architecture

## 1. Purpose

DASS is a research-stage modular training-device and device-management concept. The proposed physical demonstrator is intended only for dedicated inert, non-functional training props. The architecture deliberately excludes functional-firearm integration and weapon-operation functions.

## 2. Logical architecture

```text
DEDICATED INERT TRAINING PROP
            |
            v
DASS CORE (proposed hardware)
  - serviceable electronics enclosure
  - power and battery monitoring
  - generic device-health sensing
  - device identification
            |
            v
LOCAL DATA INTERFACE
            |
            v
DASS CONNECT (desktop software)
  - synthetic / later validated telemetry
  - device status and diagnostics
  - session records and CSV export
  - scenario-analysis summaries
            |
            v
DASS MANAGEMENT (future)
  - multi-device inventory
  - service history
  - availability overview
  - training administration reports
```

This is a logical concept diagram, not a completed electrical or mechanical design.

## 3. Current software architecture

The active Python demonstrator contains four layers:

1. **Configuration:** `DeviceConfig` validates duration, sample interval, initial battery assumption and illustrative diagnostic probabilities.
2. **Session simulation:** `DeviceHealthSimulator` generates synthetic battery, enclosure-temperature, connection and sensor-status records using a fixed random seed.
3. **Scenario evaluation:** `ScenarioMonteCarloEvaluator` repeats the synthetic device-health scenario with independent seeds and summarizes variation across runs.
4. **Data export:** CSV functions write time-series telemetry, a single-session summary, individual scenario trials and aggregate scenario statistics.

All generated records are explicitly marked synthetic. The configured probabilities and rates are software assumptions, not measured device failure rates or engineering specifications.

## 4. Subsystem responsibilities

### DASS Core

Research topics include enclosure packaging, accessibility of service points, power management, generic electronics health, connector robustness and replaceable modules. No functional-firearm interface or mechanism actuation is part of the design.

### DASS Connect

The first software milestone is a local, offline application. It will display device availability, battery and connection state, diagnostic messages and session metadata. The current Python demonstration is a command-line data generator with CSV outputs; it is not yet a graphical desktop application and does not connect to physical hardware.

### DASS Management

A future layer may consolidate records from multiple inert training devices. User identity should be minimized; access control, retention policy and export permissions must be defined before any real deployment.

## 5. Explicit exclusions

The project does not design or provide:
- Attachments for functional firearms.
- Interfaces to firing, trigger, chamber, slide/bolt, safety or other operating mechanisms.
- Live-ammunition functionality.
- Aiming, sight-alignment, targeting or point-of-impact assistance.
- Ballistic or projectile-trajectory calculations.
- Recoil or weapon-cycle replication.
- Instructions for weapon construction, modification or operation.

## 6. Design principles

1. **Inert-only interface:** physical prototypes are evaluated only on dedicated non-functional training props.
2. **Modularity:** serviceable subassemblies should be replaceable without discarding the complete unit.
3. **Local-first operation:** the core demonstration should work without a cloud account or internet connection.
4. **Traceability:** requirements, revisions, tests and design decisions should be recorded.
5. **Honest evidence:** synthetic data, analytical estimates and measured results must be clearly distinguished.
6. **Privacy by design:** store only the minimum information needed for device and session administration.

## 7. Next software milestones

- Replace the command-line summary with a local dashboard after the information requirements are approved.
- Define a documented, read-only telemetry data interface for a future bench electronics demonstrator.
- Add data validation and diagnostics for missing, stale or out-of-range device-health records.
- Add device inventory and service-history records only after the core single-device workflow is validated.
