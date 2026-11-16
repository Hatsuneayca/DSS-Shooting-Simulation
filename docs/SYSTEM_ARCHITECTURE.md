# DASS System Architecture

## 1. Purpose

DASS is a research-stage modular training-device and device-management concept. The proposed hardware is intended only for dedicated inert, non-functional training props. The architecture deliberately excludes functional-firearm integration and weapon-operation functions.

## 2. Logical architecture

```text
DEDICATED INERT TRAINING PROP
            |
            v
DASS CORE (proposed hardware)
  - serviceable electronics enclosure
  - power and battery monitoring
  - generic device-health sensing
  - optional generic UI notification
            |
            v
LOCAL DATA INTERFACE
            |
            v
DASS CONNECT (desktop software)
  - device status
  - session records
  - diagnostic log
  - CSV export
            |
            v
DASS MANAGEMENT (future)
  - multi-device inventory
  - service history
  - availability overview
  - training administration reports
```

This is a logical concept diagram, not a completed electrical or mechanical design.

## 3. Subsystem responsibilities

### DASS Core

Research topics include enclosure packaging, accessibility of service points, power management, generic electronics health, connector robustness and replaceable modules. Any physical notification feature is limited to a generic user-interface cue; it is not intended to reproduce recoil or an operating cycle.

### DASS Connect

The first software milestone is a local, offline application. It will display device availability, battery and connection state, diagnostic messages and session metadata. The current Python demonstration generates synthetic device-health records only.

### DASS Management

A future layer may consolidate records from multiple inert training devices. User identity should be minimized; access control, retention policy and export permissions must be defined before any real deployment.

## 4. Explicit exclusions

The project does not design or provide:
- Attachments for functional firearms.
- Interfaces to firing, trigger, chamber, slide/bolt, safety or other operating mechanisms.
- Live-ammunition functionality.
- Aiming, sight-alignment, targeting or point-of-impact assistance.
- Ballistic or projectile-trajectory calculations.
- Recoil or weapon-cycle replication.
- Instructions for weapon construction, modification or operation.

## 5. Design principles

1. **Inert-only interface:** physical prototypes are evaluated only on dedicated non-functional training props.
2. **Modularity:** serviceable subassemblies should be replaceable without discarding the complete unit.
3. **Local-first operation:** the core demonstration should work without a cloud account or internet connection.
4. **Traceability:** requirements, revisions, tests and design decisions should be recorded.
5. **Honest evidence:** synthetic data, analytical estimates and measured results must be clearly distinguished.
6. **Privacy by design:** store only the minimum information needed for device and session administration.
