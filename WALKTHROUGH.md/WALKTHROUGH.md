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
  - Windows 10 (target) — Host-only adapter + NAT

### Network Configuration
- Host-only adapter: allows VM-to-VM communication
- NAT adapter: allows internet access for package installation
- Verified connectivity between Kali and Windows using `ping`

### Splunk Universal Forwarder (Windows VM)
- Installed Splunk Universal Forwarder on the Windows 10 VM
- Configured `inputs.conf` to monitor Windows Security Event Logs:
  ```
  [WinEventLog://Security]
  disabled = 0
  index = main
  ```
- Pointed forwarder output to Splunk Enterprise (running on the Windows VM or host)

---

## Phase 2: SMB Brute Force Attack Simulation

### Tools Used
- **Hydra** (Kali Linux) — SMB brute-force

### Steps
1. Confirmed SMB (port 445) was open on the Windows target using `nmap`
2. Created a wordlist for the brute-force attempt
3. Executed Hydra against the Windows target:
   ```bash
   hydra -l administrator -P /usr/share/wordlists/rockyou.txt smb://<target-ip>
   ```
4. Confirmed failed login attempts were generating Windows Security Event ID **4625** (Failed Logon)

---

## Phase 3: Splunk Detection Engineering

### Log Ingestion
- Verified Event ID 4625 logs were arriving in Splunk via the Universal Forwarder
- Indexed under `index=main` with `sourcetype=WinEventLog:Security`

### Detection Query (SPL)
```spl
index=main sourcetype="WinEventLog:Security" EventCode=4625
| stats count by src_ip, user, host
| where count > 5
| sort - count
```

### Alert Configuration
- Saved search as a Splunk Alert
- Configured to trigger when failed logon count exceeds threshold
- Alert action: log to file / trigger Python script

---

## Phase 4: Automated Case Note Generation

### Tools Used
- **Python 3**
- **Splunk REST API**

### Script Logic
1. Authenticate to Splunk REST API using session token
2. Run saved search via API call
3. Parse returned JSON results (src_ip, user, count, timestamp)
4. Format structured case note
5. Write case note to `/notes/` directory

### Sample Case Note Output
```
=== SOC CASE NOTE ===
Date: 2025-XX-XX
Alert: SMB Brute Force Detected
Source IP: 192.168.X.X
Target User: administrator
Failed Attempts: 47
Action Taken: Flagged for escalation
Status: Open
=====================
```

---

## Phase 5: Validation & Evidence Collection

- Captured screenshots of each phase (see `/screenshots/`)
- Confirmed end-to-end pipeline: Attack → Detection → Automated Output
- Pushed all configs, notes, and screenshots to GitHub

---

## Key Takeaways

- Hands-on experience with Windows event log forwarding and Splunk ingestion
- Built a working detection rule using SPL for brute-force behavior
- Automated SOC triage documentation using Python + REST API
- Reinforced understanding of attacker techniques (T1110 - Brute Force) and defensive detection engineering

---

## References

- [Splunk REST API Documentation](https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTprolog)
- [MITRE ATT&CK T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/)
- [Hydra Documentation](https://github.com/vanhauser-thc/thc-hydra)
