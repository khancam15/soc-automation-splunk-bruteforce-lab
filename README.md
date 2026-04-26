# soc-automation-splunk-bruteforce-lab

Simulated SMB brute-force attack -> Splunk detection engineering -> automated case note generation via Splunk REST API + Python.

## SOC Automation and Detection Engineering Lab

### SMB Brute Force Simulation -> Splunk Detection -> Automated Case Triage

## Overview

This lab simulates SMB brute-force activity in a controlled virtual environment, detects it in Splunk, and automates case-note generation through the Splunk REST API.

The project demonstrates an end-to-end SOC workflow:
- Threat simulation
- Detection engineering
- Alert triage documentation

## Tools and Technologies

| Tool | Purpose |
|---|---|
| Kali Linux | Attack simulation source |
| Windows 11 VM | Attack target |
| Splunk Enterprise | Ingestion, search, and alerting |
| Splunk Universal Forwarder | Windows log forwarding |
| Python 3 | REST API automation |
| VirtualBox | Virtual networking and isolation |
| smbclient | SMB authentication attempt simulation |

## Lab Architecture

```text
[Kali Linux VM] ---(Host-only Network)---> [Windows 11 VM]
                                                                  |
                                                [Splunk Universal Forwarder]
                                                                  |
                                                [Splunk Enterprise (indexer)]
                                                                  |
                                                     [Python REST API Client]
                                                                  |
                                                     [Automated Case Notes]
```

## Lab Objectives

- Simulate SMB brute-force attempts from Kali to Windows 11
- Forward Windows Security logs (EventCode 4625) to Splunk
- Build SPL detections for brute-force behavior
- Pull detection results programmatically from Splunk REST API
- Generate structured SOC case notes automatically

## Developer Cybersecurity Guardrails

Use this repository only in an isolated and authorized lab.

- Never run attack simulation commands against production or public systems
- Keep all VMs on a lab-only host-only network segment
- Use test accounts only; do not reuse real user credentials
- Rotate any lab credentials after demos or screenshots
- Use least privilege for Splunk API users and tokens
- Store secrets in environment variables, not source files
- Redact IPs, hostnames, usernames, and tokens before publishing screenshots

## GitHub Best Practices for This Lab

- Enable branch protection on main:
  - Require pull requests
  - Require at least 1 approval
  - Require status checks before merge
- Use small, focused pull requests with clear titles
- Use conventional commit messages where possible
- Require secret scanning and Dependabot alerts in repository settings
- Sign commits and tag releases for portfolio milestones
- Keep documentation and evidence in sync for every detection change

## Suggested Secure Development Workflow

1. Create a feature branch for each lab change.
2. Update detection, docs, and evidence together.
3. Run quick quality checks before commit:
    - SPL query sanity check in Splunk
    - Markdown link and formatting check
    - Manual review for secret leakage
4. Open a pull request with:
    - What changed
    - Why it changed
    - Validation evidence (screenshots or output)
5. Merge after review and passing checks.

## Repository Structure

```text
soc-automation-splunk-bruteforce-lab/
|-- queries/          # SPL detection queries used in Splunk
|-- screenshots/      # Lab evidence and validation screenshots
|-- .gitignore
|-- README.md
|-- SECURITY.md       # Lab and GitHub security practices
|-- WALKTHROUGH.md    # Step-by-step walkthrough
```

## Screenshots

See the screenshots directory for evidence of each lab phase, including attack execution, detections, and automated output.

## Walkthrough

See WALKTHROUGH.md for the full step-by-step guide.

## Core Project Files

- queries/ (SPL detection queries)
- screenshots/ (lab evidence)
- .gitignore
- README.md
- SECURITY.md (security policy and reporting guidance)
- WALKTHROUGH.md

## Author

Khaneil Campbell | khancam15

Cybersecurity | SOC Analyst | Blue Team


