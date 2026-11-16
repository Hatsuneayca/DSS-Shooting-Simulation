# Independent Peer Review

## Purpose

DASS welcomes structured, independent feedback that improves the repository's software quality, maintainability, reproducibility, documentation, and responsible-use safeguards.

The peer-review process is intended to make technical criticism traceable and constructive. It does not constitute academic peer review of a published paper, product certification, safety certification, or endorsement of real-world use.

## Review scope

Reviews may address:

- Software architecture, readability, maintainability, and error handling.
- Test organization, dependency management, and reproducibility.
- General numerical-software robustness using synthetic or software-only test cases.
- Clarity of assumptions, limitations, and the distinction between simulated results and measured results.
- Documentation quality, safe-use statements, and responsible-use safeguards.

Reviews must not provide instructions or recommendations intended to improve real-world weapon accuracy, targeting, range, lethality, construction, modification, or operation. Do not submit live-fire procedures, real-world targeting data, operational weapon parameters, private datasets, credentials, or personal information. Keep examples synthetic and software-only.

## How to submit a review

1. Open the [Peer Review issue form](https://github.com/Hatsuneayca/DSS-Shooting-Simulation/issues/new?template=peer-review.yml).
2. Record the exact commit SHA or release reviewed. A review without a revision reference may be difficult to reproduce.
3. Select the primary review scope and provide an overall assessment.
4. Separate major findings from minor findings. For each finding, cite a file path or line number when possible and explain its impact.
5. Include only safe, synthetic reproduction details. State what you could not verify rather than inferring results.
6. Submit the issue publicly. Do not use GitHub Issues to disclose vulnerabilities that contain sensitive information; contact the maintainer privately through a verified contact channel instead.

## Review handling

The maintainer will:

1. Check that the review identifies the reviewed revision and stays within the stated scope.
2. Ask for clarification when a finding is not reproducible or lacks enough context.
3. Respond to each substantive finding with its disposition:
   - **Accepted** — the finding is valid and a change or follow-up has been planned.
   - **Partially accepted** — the concern is valid, but the proposed interpretation or remedy needs adjustment.
   - **Not accepted** — the concern was considered but will not be acted on; the rationale should be recorded.
   - **Unable to verify** — available evidence is insufficient to reach a conclusion.
4. Link any resulting documentation or software-only change to the review issue.
5. Close the issue when all findings have a recorded disposition or when no further action is planned.

A review outcome such as “Suitable for further review” is an assessment by the reviewer, not a claim that the system has been independently validated or certified.

## Reproducibility and evidence

A useful review identifies:

- The reviewed commit or release.
- Relevant file paths and line numbers.
- Software versions and dependencies, when applicable.
- The synthetic test or software-only steps used.
- Expected versus observed behavior.
- Any assumptions or unavailable information.

Simulation outputs must be described as simulation results unless independently supported by real measurements. Do not present targets, estimates, or unverified performance claims as validated real-world performance.

## Reviewer conduct

Be specific, respectful, and evidence-led. Disagreement is acceptable; unsupported personal remarks are not. Public issue reports are visible to others and should contain only information that is appropriate to publish.

## Important limitation

DASS is presented as a software and simulation project. A GitHub review, successful test run, or merged change does not establish that any physical device is safe, compliant, accurate, or suitable for real-world operation. Do not use repository feedback as a substitute for qualified safety assessment or applicable regulatory review.
