#!/usr/bin/env python3
import re, yaml, json
from pathlib import Path

def load_patterns(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f)
    return [(re.compile(p["regex"]), p) for p in y.get("patterns", [])]

def scan_files(files, patterns):
    findings = []
    for fp in files:
        p = Path(fp)
        if not p.exists():
            findings.append({"file": fp, "match": None, "rule": None, "note": "missing"})
            continue
        text = p.read_text(errors="ignore")
        for rx, rule in patterns:
            if rx.search(text):
                findings.append({
                    "file": fp,
                    "match": rx.pattern,
                    "rule": rule["id"],
                    "desc": rule["description"]
                })
    return findings

if __name__ == "__main__":
    pats = load_patterns(Path("rules/patterns.yml"))
    files = [
        "rules/static/sample-configs/apache.conf",
        "rules/static/sample-configs/mysql.cnf",
    ]
    out = scan_files(files, pats)
    print(json.dumps({"count": len(out), "findings": out}, indent=2))

