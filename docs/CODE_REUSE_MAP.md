# Reusable Code Assets from the Earlier DASS Iteration

## Purpose

The earlier DASS source was a substantial software experiment. When the active project scope was refocused, its original file was removed from the current branch but preserved in Git history.

The original source can be viewed at this historical revision:

[Legacy DASS source — historical commit](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/blob/352a430fcff12c07a191805128de4d8b5793e8c9/Dass%20Balistics)

This note records which general software-engineering ideas remain useful and how they have been redirected into the current project.

## Reusable engineering patterns

| Earlier software pattern | Current DASS use |
|---|---|
| Separate classes for separate responsibilities | `DeviceConfig`, `DeviceHealthSimulator`, and result dataclasses |
| Repeatable random-number generation | Explicit seeds for synthetic sessions |
| Repeated-run Monte Carlo structure | `ScenarioMonteCarloEvaluator` for device-health scenario variation |
| CSV data export | Telemetry, session-summary, scenario-trial and aggregate-summary files |
| Numerical summary and reporting | Connection availability, sensor status, minimum synthetic battery, maximum synthetic enclosure temperature and attention count |
| Inline documentation of limitations | Synthetic-data labels and explicit statement that scenario parameters are not measured |

## What was intentionally not carried into the active software

Domain-specific projectile, aiming, point-of-impact and recoil calculations are not part of the current DASS product scope. They are not active software components and are not needed for the current research questions on serviceability, device-health management, session records and product feasibility.

## Why retain the historical source?

Keeping the original revision in Git history preserves the development record and makes the evolution of the project transparent. The current branch should remain focused on the product and research scope that will be reviewed by the academic supervisor.

## Current status

The active software is a synthetic device-health demonstrator. Its scenario model is useful for developing data structures, reproducibility, reporting and test organization. Its outputs must not be presented as real hardware measurements or field-reliability estimates.
