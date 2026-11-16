# DASS Software Demonstrator

The current Python program is an offline, synthetic device-health telemetry demonstration.

It records fictional battery level, enclosure temperature, connection state and sensor status. It exports the records as CSV so the data pipeline and software tests can be reviewed before hardware exists.

Run from the repository root:

```bash
python -m software.dass_telemetry_demo
python -m unittest discover -s tests -v
```

There is no hardware interface, actuator output, firearm interface, weapon-operation logic, trajectory calculation or aiming/impact computation in this demonstration.

When real electronics are developed, measured values must replace synthetic records only after their units, calibration, source and validity checks have been documented.
