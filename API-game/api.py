"""
AbuseIPDB API client.
Free tier: 1000 checks/day. Get your key at https://www.abuseipdb.com/register
"""

import os
import requests
from dataclasses import dataclass

ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"
MALICIOUS_THRESHOLD = 25  # Confidence score above this = malicious


@dataclass
class IPVerdict:
    ip: str
    confidence_score: int
    total_reports: int
    country: str
    isp: str
    domain: str
    is_malicious: bool
    last_reported: str | None
    via_api: bool = True  # False = demo mode


def check_ip(ip: str) -> IPVerdict | None:
    """
    Query AbuseIPDB for an IP address. Returns None on failure.
    Reads ABUSEIPDB_API_KEY from environment.
    """
    api_key = os.environ.get("ABUSEIPDB_API_KEY", "")
    if not api_key:
        return None

    try:
        response = requests.get(
            ABUSEIPDB_URL,
            headers={
                "Key": api_key,
                "Accept": "application/json",
            },
            params={
                "ipAddress": ip,
                "maxAgeInDays": "90",
                "verbose": "",
            },
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()["data"]

        score = data.get("abuseConfidenceScore", 0)
        return IPVerdict(
            ip=ip,
            confidence_score=score,
            total_reports=data.get("totalReports", 0),
            country=data.get("countryCode", "??"),
            isp=data.get("isp", "Unknown ISP"),
            domain=data.get("domain", ""),
            last_reported=data.get("lastReportedAt"),
            is_malicious=score >= MALICIOUS_THRESHOLD,
            via_api=True,
        )
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Demo mode targets — used when no API key is set.
# Each entry: (ip, is_malicious, confidence_score, country, isp, reports)
# ---------------------------------------------------------------------------
DEMO_TARGETS = [
    # ---- Clearly malicious ----
    ("185.220.101.45",  True,  100, "DE", "Frantech Solutions",          3842, "Tor exit node — a known conveyor belt for bad actors."),
    ("194.165.16.11",   True,   98, "LT", "UAB Cherry Servers",          1204, "Persistent mass-scanner. It knows what it's doing."),
    ("80.82.77.139",    True,   87, "DE", "Shodan.io",                    887, "Shodan's own scanner. Malicious? Depends who you ask."),
    ("45.141.84.120",   True,   96, "RU", "Petersburg Internet Network",  2110, "Brute-force origin. Basically a login-attempt factory."),
    ("92.255.85.172",   True,   95, "RU", "TimeWeb Ltd.",                 1893, "Command-and-control infrastructure. Ominous by design."),
    ("62.210.16.12",    True,   82, "FR", "Online SAS",                    643, "Port scanner. It's been very thorough about it."),
    ("116.31.116.36",   True,   79, "CN", "Chinanet",                      501, "Credential stuffing source. Enthusiastic."),
    ("198.199.70.50",   True,   73, "US", "DigitalOcean",                  389, "Spam origin. Cloud servers: democratizing everything."),

    # ---- Benign / legitimate ----
    ("8.8.8.8",         False,   0, "US", "Google LLC",           0, "Google's public DNS. About as evil as a golden retriever."),
    ("1.1.1.1",         False,   0, "AU", "Cloudflare Inc.",       0, "Cloudflare DNS. Fast, private, thoroughly uninteresting."),
    ("9.9.9.9",         False,   0, "US", "Quad9",                 0, "Quad9 DNS. Blocking malware, one lookup at a time."),
    ("208.67.222.222",  False,   0, "US", "Cisco OpenDNS",         0, "OpenDNS. Cisco wants you to know it's very enterprise."),
    ("13.107.42.14",    False,   1, "US", "Microsoft Corporation", 2, "Microsoft's CDN. The 1 report was probably a false alarm."),
    ("151.101.1.69",    False,   0, "US", "Fastly Inc.",           0, "Fastly CDN node. Delivering your memes since 2011."),
    ("17.172.224.47",   False,   0, "US", "Apple Inc.",            0, "Apple's infrastructure. Shiny, expensive, benign."),
    ("104.16.123.96",   False,   0, "US", "Cloudflare Inc.",       0, "Another Cloudflare IP. They have a lot of them."),

    # ---- Spicy / ambiguous ----
    ("45.33.32.156",    False,  12, "US", "Linode",                24, "scanme.nmap.org — intentionally public scan target. Technically fine."),
    ("66.249.64.1",     False,   2, "US", "Google LLC",             3, "Googlebot. It's read your entire website. Multiple times."),
    ("5.188.86.172",    True,   91, "NL", "Serverius",            1500, "DDoS-for-hire infrastructure. The audacity of a fixed address."),
    ("72.14.192.1",     False,   0, "US", "Google LLC",             0, "Google backbone. Your packets probably passed through here."),
]


def get_demo_verdict(entry: tuple) -> IPVerdict:
    """Build an IPVerdict from a demo target tuple."""
    ip, is_malicious, score, country, isp, reports, _ = entry
    return IPVerdict(
        ip=ip,
        confidence_score=score,
        total_reports=reports,
        country=country,
        isp=isp,
        domain="",
        last_reported=None,
        is_malicious=is_malicious,
        via_api=False,
    )
