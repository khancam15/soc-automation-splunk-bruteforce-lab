#!/usr/bin/env python3
"""
soc_automation.py
-----------------
SOC Automation Script — SMB Brute Force Detection
Author:      khancam15 (Khaneil Campbell)
Lab:         SOC Automation & Detection Engineering Lab

Description:
    Authenticates to the Splunk REST API, runs the brute force
    detection search, parses the results, and auto-generates a
    structured Markdown case note for SOC analyst review.

Usage:
    python3 soc_automation.py

Requirements:
    pip install requests urllib3
"""

import os
import requests
import urllib3
from datetime import datetime

# ── Suppress SSL warnings for local Splunk instance ───────────────────────────
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── Configuration ─────────────────────────────────────────────────────────────
SPLUNK_HOST  = "https://localhost:8089"
SPLUNK_USER  = os.getenv("SPLUNK_USER", "admin")
SPLUNK_PASS  = os.getenv("SPLUNK_PASS", "your_password_here")
OUTPUT_DIR   = "notes"

# ── Detection Query ───────────────────────────────────────────────────────────
SPL_QUERY = """
search index=main sourcetype="WinEventLog:Security" EventCode=4625
| where NOT (Source_Network_Address="127.0.0.1" OR Source_Network_Address="::1")
| bucket _time span=5m
| stats count as failed_logins
        values(Logon_Type)     as logon_types
        values(Failure_Reason) as reasons
        values(host)           as host
  by Account_Name, Source_Network_Address, _time
| where failed_logins >= 10
| eval severity=if(failed_logins >= 20, "High", "Medium")
| sort - failed_logins
| table _time Account_Name Source_Network_Address host failed_logins logon_types reasons severity
""".strip()


# ── Step 1: Authenticate ──────────────────────────────────────────────────────
def get_session_key():
    """Authenticate to Splunk and return a session key."""
    url  = f"{SPLUNK_HOST}/services/auth/login"
    data = {
        "username":    SPLUNK_USER,
        "password":    SPLUNK_PASS,
        "output_mode": "json"
    }
    print("[*] Authenticating to Splunk REST API...")
    response = requests.post(url, data=data, verify=False, timeout=30)
    response.raise_for_status()
    key = response.json()["sessionKey"]
    print("[+] Authentication successful.")
    return key


# ── Step 2: Run Search ────────────────────────────────────────────────────────
def run_search(session_key):
    """Submit the SPL query and return the search job ID."""
    headers = {"Authorization": f"Splunk {session_key}"}
    url     = f"{SPLUNK_HOST}/services/search/jobs"
    data    = {
        "search":      SPL_QUERY,
        "output_mode": "json",
        "exec_mode":   "blocking"
    }
    print("[*] Running brute force detection search...")
    response = requests.post(url, headers=headers, data=data, verify=False, timeout=120)
    response.raise_for_status()
    sid = response.json()["sid"]
    print(f"[+] Search job completed. SID: {sid}")
    return sid


# ── Step 3: Fetch Results ─────────────────────────────────────────────────────
def get_results(session_key, sid):
    """Retrieve results from the completed search job."""
    headers = {"Authorization": f"Splunk {session_key}"}
    url     = f"{SPLUNK_HOST}/services/search/jobs/{sid}/results"
    params  = {"output_mode": "json", "count": 0}
    print("[*] Fetching alert results...")
    response = requests.get(url, headers=headers, params=params, verify=False, timeout=30)
    response.raise_for_status()
    results = response.json()["results"]
    print(f"[+] {len(results)} alert(s) found.")
    return results


# ── Step 4: Generate Case Note ────────────────────────────────────────────────
def generate_case_note(alerts):
    """Format and write a structured Markdown case note."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = os.path.join(OUTPUT_DIR, f"soc_case_{timestamp}.md")
    count     = len(alerts)

    lines = []
    lines.append(f"- Alerts found: **{count}**\n")
    lines.append("## Alerts\n")

    for alert in alerts:
        account  = alert.get("Account_Name",           "-")
        src_ip   = alert.get("Source_Network_Address",  "-")
        host     = alert.get("host",                    "-")
        logins   = alert.get("failed_logins",           "-")
        severity = alert.get("severity",                "-")
        time_val = alert.get("_time",                   "-")
        logon    = alert.get("logon_types",             "-")
        reasons  = alert.get("reasons",                 "-")

        lines.append(f"### {severity} - {account} from {src_ip}\n")
        lines.append(f"- Time bucket: **{time_val}**")
        lines.append(f"- Host: **{host}**")
        lines.append(f"- Account: **{account}**")
        lines.append(f"- Source IP: **{src_ip}**")
        lines.append(f"- Failed logins (5m): **{logins}**")
        lines.append(f"- Logon types: `{logon}`")
        lines.append(f"- Reasons: \"{reasons}\"\n")
        lines.append("**Recommended actions**")
        lines.append("- Search for 4624 (success) for same user/IP after failures")
        lines.append("- Validate if source IP is expected (admin host) or suspicious")
        lines.append("- If suspicious: block IP + consider account lock/MFA\n")

    with open(filename, "w") as f:
        f.write("\n".join(lines))

    print(f"[+] Case note written to: {filename}")
    print(f"\n- Alerts found: **{count}**")
    for alert in alerts:
        sev     = alert.get("severity", "-")
        account = alert.get("Account_Name", "-")
        src_ip  = alert.get("Source_Network_Address", "-")
        logins  = alert.get("failed_logins", "-")
        print(f"  -> {sev} - {account} from {src_ip} ({logins} failed logins)")

    return filename


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  SOC Automation Script - SMB Brute Force Detection")
    print("  khancam15 | Columbia University CUIT")
    print("=" * 55 + "\n")

    try:
        session_key = get_session_key()
        sid         = run_search(session_key)
        alerts      = get_results(session_key, sid)

        if not alerts:
            print("[!] No alerts found matching threshold. Nothing to report.")
        else:
            output = generate_case_note(alerts)
            print(f"\n[*] Done. Review your case note: {output}")

    except requests.exceptions.ConnectionError:
        print("[!] Could not connect to Splunk. Is Splunk running on localhost:8089?")
    except requests.exceptions.HTTPError as e:
        print(f"[!] HTTP error: {e}")
    except KeyError as e:
        print(f"[!] Unexpected response format. Missing key: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
