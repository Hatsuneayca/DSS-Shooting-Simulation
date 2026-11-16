# DASS — Modular Electromechanical Training & Device-Management Platform

**DASS is a research-stage concept for a modular, serviceable training platform built around dedicated inert, non-functional training props.** The project focuses on maintainable hardware packaging, device-health monitoring, local software, session records and product feasibility.

Prepared by: Ayça Bahar Güner — Department of Mechanical Engineering, Dokuz Eylül University

> **Scope and safety boundary:** DASS is intended only for dedicated inert training props. It is not designed to attach to, modify, or interface with a functional firearm. It does not use live ammunition and does not interact with firing, trigger, chamber, slide/bolt, safety, or other operating mechanisms. The active software scope excludes weapon-operation logic, ballistic or trajectory calculations, aiming assistance, point-of-impact correction, and recoil replication. Any future haptic feature is limited to generic user-interface notifications, not simulated weapon recoil.

---

## 1. Project objective

DASS investigates whether a compact, modular and serviceable electromechanical training accessory can support device monitoring and training-session administration without requiring a large fixed simulator installation.

The project's potential contribution will be assessed through measurable engineering questions:

- Can hardware be organized into serviceable modules?
- Can device condition and session state be monitored locally?
- Can the system generate reliable, privacy-conscious maintenance and session records?
- Can the enclosure and electronic architecture be manufactured and maintained with accessible components?
- What are the prototype, operating and maintenance costs?

These are research questions, not demonstrated results.

## 2. Proposed product architecture

### DASS Core — inert training-device module

A removable electronics enclosure intended only for a dedicated non-functional training prop. Research topics include enclosure design, serviceability, power management and generic device-health sensing. No compatibility is claimed for functional firearms.

### DASS Connect — local software

A desktop application concept for device status, session records, diagnostics and exportable reports. The first software milestone is an offline demonstration using synthetic device-health data.

### DASS Management — multi-device administration

A future management layer for training staff to review device availability, battery and connection status, service history and session records across a group of inert training devices. This layer is planned and has not been implemented.

## 3. What exists today

| Component | Current status |
|---|---|
| Initial system concept | Documented |
| Structured feedback and peer-review forms | Added to GitHub |
| Product requirements and architecture | Draft documentation added |
| Synthetic device-health telemetry demo | Implemented in Python |
| Automated tests for the synthetic demo | Added |
| CAD and enclosure prototype | Not yet completed |
| Electronics prototype | Not yet completed |
| Hardware integration | Not yet completed |
| Experimental validation | Not yet completed |
| Costed bill of materials | Template provided; costs not yet established |
| Multi-device management application | Future work |

No physical prototype, measured hardware performance, field evaluation, certification or institutional endorsement is claimed.

## 4. Repository structure

```text
.
├── .github/ISSUE_TEMPLATE/
├── docs/
│   ├── BUDGET_AND_BOM_TEMPLATE.md
│   ├── LEGACY_SCOPE_NOTE.md
│   ├── PRODUCT_POSITIONING.md
│   ├── PRODUCT_REQUIREMENTS.md
│   ├── PROJECT_BRIEF.md
│   ├── ROADMAP.md
│   ├── SYSTEM_ARCHITECTURE.md
│   └── VALIDATION_PLAN.md
├── software/
│   ├── README.md
│   └── dass_telemetry_demo.py
├── tests/
│   └── test_telemetry_demo.py
├── PEER_REVIEW.md
└── README.md
```

## 5. Run the software demonstration

Requirements: Python 3.9 or later. The current demonstration uses only the Python standard library.

From the repository root:

```bash
python -m software.dass_telemetry_demo
python -m unittest discover -s tests -v
```

Optional parameters:

```bash
python -m software.dass_telemetry_demo --duration 120 --interval 5 --seed 17 --output outputs/demo_session.csv
```

The script creates fictional battery, enclosure-temperature, connection and sensor-health records. The output is repeatable for a fixed seed. It does not connect to or control physical hardware.

## 6. Research and validation

The proposed work moves through requirements definition, concept selection, CAD and enclosure development, a low-risk electronics demonstrator, software integration, bench testing, and cost and maintainability analysis.

- [System Architecture](docs/SYSTEM_ARCHITECTURE.md)
- [Product Positioning and Differentiation](docs/PRODUCT_POSITIONING.md)
- [Legacy Scope Note](docs/LEGACY_SCOPE_NOTE.md)
- [Product Requirements](docs/PRODUCT_REQUIREMENTS.md)
- [Proof-of-Concept Brief](docs/PROJECT_BRIEF.md)
- [Validation Plan](docs/VALIDATION_PLAN.md)
- [Six-Month Roadmap](docs/ROADMAP.md)
- [Budget and BOM Template](docs/BUDGET_AND_BOM_TEMPLATE.md)
- [Independent Peer Review Process](PEER_REVIEW.md)

## 7. Feedback

- [Technical Review](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=technical-review.yml)
- [Bug Report](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=bug-report.yml)
- [Research Feedback](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=research-feedback.yml)
- [Peer Review](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=peer-review.yml)

Please do not post personal data, credentials, private datasets or sensitive operational information.

## 8. Current limitations

DASS is a student research project at the concept and software-demonstration stage. Synthetic telemetry is illustrative, not measured. Hardware selection, enclosure design, environmental limits, service intervals, production cost and performance claims require later engineering analysis and testing.

The repository does not claim compatibility with functional firearms, a validated physical recoil system, or a completed training product.
