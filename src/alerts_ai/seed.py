"""Seed the database with a test user and sample alerts.

Run: uv run python -m alerts_ai.seed
Safe to re-run: skips the user if the email exists and alerts if any exist.
"""

import asyncio

from sqlalchemy import func, select

from alerts_ai.core.database import SessionLocal
from alerts_ai.core.security import hash_password
from alerts_ai.features.alerts.model import Alert, AlertStatus, AlertVerdict
from alerts_ai.features.users.model import User

TP = AlertVerdict.TRUE_POSITIVE
FP = AlertVerdict.FALSE_POSITIVE
NI = AlertVerdict.NEED_INVESTIGATION
PENDING = AlertStatus.PENDING
INVESTIGATING = AlertStatus.INVESTIGATING
DONE = AlertStatus.DONE

# (title, verdict, severity 1-5, attack_outcome, status)
ALERTS = [
    ("Mimikatz credential dumping detected on WS-FIN-023", TP, 5, "Blocked", DONE),
    ("LSASS memory access by rundll32.exe on SRV-DC-01", TP, 5, "Succeeded", INVESTIGATING),
    ("Suspicious PowerShell encoded command on WS-HR-007", NI, 4, "Unknown", PENDING),
    ("Impossible travel: login from Lagos and Berlin within 20 minutes for j.miller", TP, 4, "Succeeded", DONE),
    ("Brute force attempt against VPN gateway from 185.220.101.47", TP, 3, "Failed", DONE),
    ("Phishing email with malicious macro delivered to 14 mailboxes", TP, 4, "Blocked", DONE),
    ("Outbound connection to known Cobalt Strike C2 server 45.137.22.91", TP, 5, "Succeeded", INVESTIGATING),
    ("Ransomware behavior: mass file renames with .lockbit extension on FS-02", TP, 5, "Prevented", DONE),
    ("New local administrator account created on WS-ENG-114", NI, 3, "Unknown", PENDING),
    ("Scheduled task created for persistence on SRV-APP-04", TP, 4, "Succeeded", INVESTIGATING),
    ("Suspicious OAuth consent grant to unverified app 'Mail Sync Pro'", NI, 3, "Unknown", PENDING),
    ("DNS tunneling detected: high-entropy subdomains to xz7q.top", TP, 4, "Detected", INVESTIGATING),
    ("Kerberoasting: RC4 TGS requests for 37 service accounts", TP, 5, "Succeeded", INVESTIGATING),
    ("PsExec lateral movement from WS-IT-002 to SRV-SQL-03", FP, 3, "N/A", DONE),
    ("Nmap port scan from internal host 10.20.4.17", FP, 2, "N/A", DONE),
    ("Antivirus disabled via registry on WS-SALES-031", TP, 4, "Prevented", DONE),
    ("Excessive failed logins for admin account on Okta", TP, 3, "Failed", DONE),
    ("Data exfiltration: 4.2 GB uploaded to mega.nz from WS-RND-009", NI, 5, "Unknown", PENDING),
    ("Log4Shell exploitation attempt against api.internal:8080", TP, 5, "Blocked", DONE),
    ("SQL injection attempt on /login endpoint from 103.75.190.12", TP, 3, "Blocked", DONE),
    ("Windows event log cleared on SRV-DC-02", TP, 5, "Succeeded", INVESTIGATING),
    ("certutil.exe used to download payload on WS-FIN-011", TP, 4, "Prevented", DONE),
    ("MFA fatigue: 23 push requests denied by s.nguyen", TP, 4, "Failed", DONE),
    ("Suspicious inbox forwarding rule to external gmail address", NI, 3, "Unknown", PENDING),
    ("AWS root account console login without MFA", TP, 5, "Succeeded", INVESTIGATING),
    ("S3 bucket 'customer-exports' made public", TP, 4, "Succeeded", DONE),
    ("IAM access key used from TOR exit node 109.70.100.23", TP, 5, "Succeeded", INVESTIGATING),
    ("GuardDuty: EC2 instance i-0a3f querying crypto mining pool", TP, 4, "Succeeded", DONE),
    ("Azure AD sign-in from anonymous IP for svc-backup", NI, 3, "Unknown", PENDING),
    ("Office spawned cmd.exe on WS-LEGAL-005", NI, 4, "Unknown", PENDING),
    ("Known malicious hash detected: Emotet loader on WS-OPS-018", TP, 5, "Blocked", DONE),
    ("WMI remote process execution on SRV-WEB-06", FP, 3, "N/A", DONE),
    ("Password spray against 120 accounts from 91.240.118.0/24", TP, 4, "Failed", DONE),
    ("Unusual RDP session from contractor laptop to SRV-HR-01", NI, 3, "Unknown", INVESTIGATING),
    ("Shadow copy deletion via vssadmin on FS-01", TP, 5, "Prevented", DONE),
    ("Suspicious DLL side-loading by OneDriveUpdater.exe", NI, 4, "Unknown", PENDING),
    ("Web shell detected: cmd.aspx uploaded to IIS on SRV-EXCH-01", TP, 5, "Succeeded", INVESTIGATING),
    ("Large volume of 403 responses from single IP on WAF", FP, 1, "N/A", DONE),
    ("USB mass storage device connected to WS-FIN-002", FP, 2, "N/A", DONE),
    ("Okta session hijack: session reused from new ASN", NI, 4, "Unknown", PENDING),
    ("GitHub personal access token leaked in public repository", TP, 4, "Succeeded", DONE),
    ("Kubernetes pod running privileged container in prod namespace", NI, 3, "Unknown", PENDING),
    ("Golden ticket suspected: TGT lifetime exceeds policy", TP, 5, "Succeeded", INVESTIGATING),
    ("Typosquatted domain conif3rs.com registered", NI, 2, "Unknown", PENDING),
    ("Vulnerability scanner traffic from Qualys appliance", FP, 1, "N/A", DONE),
    ("Beaconing to 194.26.29.112 every 60 seconds from WS-MKT-021", TP, 4, "Detected", INVESTIGATING),
    ("Credential phishing page hosted on sharepoint-docs-login.net clicked by 3 users", TP, 4, "Succeeded", DONE),
    ("Suspicious use of AdFind.exe for domain enumeration", TP, 4, "Detected", INVESTIGATING),
    ("Firewall rule change allowing 0.0.0.0/0 on port 3389", TP, 4, "Succeeded", DONE),
    ("Endpoint agent offline for 72 hours on SRV-PAY-01", NI, 2, "Unknown", PENDING),
]
assert len(ALERTS) == 50


async def seed() -> None:
    async with SessionLocal() as session:
        if not await session.scalar(select(User).where(User.email == "abd@test.com")):
            session.add(User(name="Abd Test", email="abd@test.com", password_hash=hash_password("12345678")))

        if not await session.scalar(select(func.count()).select_from(Alert)):
            session.add_all(
                Alert(title=t, verdict=v, severity=s, attack_outcome=o, status=st)
                for t, v, s, o, st in ALERTS
            )

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
