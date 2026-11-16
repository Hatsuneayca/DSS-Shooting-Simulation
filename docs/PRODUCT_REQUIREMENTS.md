# DASS Product Requirements — Draft

Status: preliminary requirements for discussion with the academic supervisor. These are proposed requirements, not verified product capabilities.

## 1. Intended users

- **Training staff:** review device availability and session records.
- **Technician:** inspect diagnostics and maintain replaceable modules.
- **Project researcher:** evaluate enclosure, power, serviceability, software reliability and cost.

## 2. Functional requirements

| ID | Requirement | Verification approach | Status |
|---|---|---|---|
| FR-01 | The demonstrator shall be intended only for a dedicated inert, non-functional training prop. | Design review | Proposed |
| FR-02 | The software shall display synthetic or validated device-health records. | Software test | Synthetic demo |
| FR-03 | The software shall export session records to CSV. | Automated test | Implemented for synthetic demo |
| FR-04 | The software shall report a device status field and diagnostic state. | Software test | Synthetic demo |
| FR-05 | The proposed enclosure shall permit access to designated serviceable modules. | CAD/design review | Not started |
| FR-06 | The proposed system shall support local operation without cloud connectivity. | Offline integration test | Planned |
| FR-07 | The management layer should support inventory and service-history views. | Demonstration review | Future work |

## 3. Non-functional requirements

| ID | Requirement | Proposed evidence |
|---|---|---|
| NFR-01 | No interface to functional-firearm operating mechanisms. | Architecture and design review |
| NFR-02 | No live ammunition or functional-firearm compatibility. | Scope review |
| NFR-03 | Hardware and software versions shall be traceable. | Revision log |
| NFR-04 | Synthetic demonstration data shall be identified as synthetic. | Documentation review |
| NFR-05 | Personal data shall be minimized. | Data-field review |
| NFR-06 | The software shall provide repeatable synthetic test data with a fixed seed. | Automated test |
| NFR-07 | Maintenance tasks and replaceable modules shall be documented. | Serviceability review |

## 4. Open decisions

The following should be agreed with the supervisor before detailed design:
- Target inert training-prop interface and physical envelope.
- Required operating time for the demonstrator.
- Local data connection method.
- Enclosure material and manufacturing process.
- Required service access and cleaning method.
- Data retention and user-access policy.
- Prototype budget and available laboratory facilities.

Do not turn estimates into requirements until they have been justified by user needs, component specifications or test evidence.
