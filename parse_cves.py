#!/usr/bin/env python3
import json
from pathlib import Path

JSON_PATH = Path("data/nvd/recent.json")

def parse_cves():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    cve_items = data.get("CVE_Items", [])
    parsed = []

    for item in cve_items:
        cve_id = item.get("cve", {}).get("id", "N/A")

        # Get English description
        descs = item.get("cve", {}).get("descriptions", [])
        description = next((d["value"] for d in descs if d["lang"] == "en"), "N/A")

        # Get CVSS 3.1 Score
        metrics = item.get("metrics", {}).get("cvssMetricV31", [])
        if metrics:
            score = metrics[0]["cvssData"]["baseScore"]
            severity = metrics[0]["cvssData"]["baseSeverity"]
        else:
            score, severity = None, None

        parsed.append({
            "CVE_ID": cve_id,
            "Description": description,
            "CVSS_Score": score,
            "Severity": severity,
            "Published": item.get("published", "N/A")
        })

    return parsed

if __name__ == "__main__":
    results = parse_cves()
    for r in results[:10]:  # print first 10
        print(f"{r['CVE_ID']} | {r['Severity']} | {r['CVSS_Score']} | {r['Description'][:80]}...")
