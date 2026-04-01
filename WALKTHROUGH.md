# Lab Walkthrough — SOC Automation: SMB Brute Force Detection

## Overview

This walkthrough documents the end-to-end steps taken to complete the SOC Automation & Detection Engineering Lab, covering environment setup, attack simulation, Splunk detection, and Python-based case note automation.

---

## Phase 1: Environment Setup

### Virtual Machines
- **Host:** MacBook Pro M5 Pro (macOS)
- **Hypervisor:** VirtualBox 7.2.6
- **VMs:**
  - Kali Linux (attacker) — Host-only adapter + NAT
  - Windows 11 (target) — Host-only adapter + NAT

### Network Configuration
- Host-only adapter: allows VM-to-VM communication
- NAT adapter: allows internet access for package installation
- Verified connectivity between Kali and Windows 11 using `ping`
- Windows 11 VM assigned static IP `10.10.10.10` on the host-only interface

### Windows 11 Static IP Configuration
Ran `ipconfig` in PowerShell on the Windows 11 VM to confirm the static IP assignment on the host-only adapter.

![Windows 11 Static IP Configuration](screenshots/01.%20windows%20static%20ip%20.png)

### Splunk Universal Forwarder (Windows 11 VM)
- Installed Splunk Universal Forwarder on the Windows 11 VM
- Configured `inputs.conf` to monitor Windows Security Event Logs:
  ```
  [WinEventLog://Security]
  disabled = 0
  index = main
  ```
- Pointed forwarder output to Splunk Enterprise

---

## Phase 2: SMB Brute Force Attack Simulation

### Tools Used
- **smbclient** (Kali Linux) — SMB brute-force simulation

### Steps

**1. Bring up the host-only network interface on Kali:**
```bash
sudo ip link set eth1 up
```

**2. Confirm connectivity to the Windows 11 target:**
```bash
ping -c 4 10.10.10.10
```

**3. Run the SMB brute-force loop:**
```bash
for i in {1..15}; do smbclient -L //10.10.10.10 -U administrator%wrongpass > /dev/null 2>&1; done
```

#### Screenshot — Kali Ping Success & Brute Force Execution
Confirmed 0% packet loss to the Windows 11 target, then launched the SMB brute-force loop.

![Kali Ping Success and SMB Brute Force](screenshots/02.%20kali%20ping%20success.png)

#### Screenshot — SMB Brute Force Failures
The repeated failed attempts triggered the Windows 11 account lockout policy, confirming the brute-force simulation was successful and generating Event ID 4625 logs.

![Kali SMB Brute Force Failures](screenshots/03.%20kali%20smb%20bruteforce.png)

---

## Phase 3: Splunk Detection Engineering

### Log Ingestion
- Verified Event ID 4625 logs were arriving in Splunk via the Universal Forwarder
- Indexed under `index=main` with `sourcetype=WinEventLog:Security`

### Detection Query 1 — Event ID 4625 Aggregation (SPL)
```spl
index=main sourcetype="WinEventLog:Security" EventCode=4625
| stats count by Source_Network_Address, Account_Name
| sort - count
```
Result: **81 failed logon events** from source IP `10.10.10.20` targeting the `administrator` account.

![Splunk Event ID 4625 Aggregation](screenshots/04.%20splunk%204625%20aggregation.png)

### Detection Query 2 — Threshold-Based Brute Force Detection (SPL)
```spl
index=main sourcetype="WinEventLog:Security" EventCode=4625
| where NOT (Source_Network_Address="127.0.0.1" OR Source_Network_Address="::1")
| bucket _time span=5m
| stats count as failed_logins by Account_Name, Source_Network_Address, _time
| where failed_logins >= 10
| eval severity="High"
| table _time Account_Name Source_Network_Address failed_logins severity
```
Result: 8 time-bucketed alerts all rated **High severity**, confirming sustained brute-force activity from `10.10.10.20`.

![Splunk Threshold Detection](screenshots/05.%20splunk%20threshold%20detection.png)

### Detection Query 3 — EventCode Distribution (SPL)
```spl
index=main sourcetype="WinEventLog:Security"
| stats count by EventCode
```
Reviewed the full EventCode distribution across 376 events to validate log coverage and confirm 4625 was the dominant failure code.

![Splunk EventCode Distribution](screenshots/06.%20splunk%20eventcode%20distribution.png)

---

## Phase 4: Automated Case Note Generation

### Tools Used
- **Python 3**
- **Splunk REST API**

### Script Logic
1. Authenticate to Splunk REST API using session token
2. Run saved detection search via API call
3. Parse returned JSON results (account, source IP, failed logins, severity, timestamp)
4. Format structured case note in Markdown
5. Write case note to working directory with timestamped filename

### Screenshot — Python Script Execution
The Python script successfully queried the Splunk REST API, identified **2 alerts**, and formatted case notes with severity ratings and recommended actions.

![Python Script Execution](screenshots/07.%20python%20script%20execution.png)

### Screenshot — Generated Case Note Output
The auto-generated case note (`soc_case_20260329_150145.md`) captured both High severity alerts with full context: host, account, source IP, failed login count, logon type, and recommended triage actions.

![Generated Case Note](screenshots/08.%20generated%20case%20note.png)

### Sample Case Note Output
```
Alerts found: 2

## Alerts

### High — administrator from 10.10.10.20

- Time bucket: 2026-03-29T14:55:00.000-04:00
- Host: Windows11
- Account: administrator
- Source IP: 10.10.10.20
- Failed logins (5m): 16
- Logon types: 1
- Reasons: "Unknown user name or bad password."

**Recommended actions**
- Search for 4624 (success) for same user/IP after failures
- Validate if source IP is expected (admin host) or suspicious
- If suspicious: block IP + consider account lock/MFA
```

---

## Phase 5: Validation & Evidence Collection

- Captured screenshots of all lab phases (see `/screenshots/`)
- Confirmed end-to-end pipeline: Attack → Detection → Automated Case Note Output
- Pushed all configs and screenshots to GitHub

---

## Key Takeaways

- Hands-on experience with Windows event log forwarding and Splunk ingestion
- Built working SPL detection rules for brute-force behavior with threshold alerting
- Automated SOC triage documentation using Python + Splunk REST API
- Reinforced understanding of attacker techniques (T1110 - Brute Force) and defensive detection engineering
- Observed real account lockout behavior (NT_STATUS_ACCOUNT_LOCKED_OUT) as a detection signal

---

## References

- [Splunk REST API Documentation](https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTprolog)
- [MITRE ATT&CK T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/)
- [smbclient Documentation](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html)
