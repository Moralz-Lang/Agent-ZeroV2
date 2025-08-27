#!/usr/bin/env python3
import argparse, json, subprocess, sys
from pathlib import Path
from scanner import load_patterns, scan_files

REPORTS = Path("reports")
REPORTS.mkdir(parents=True, exist_ok=True)

def do_update_cve():
    print("[*] Updating CVE DB...")
    subprocess.check_call([sys.executable, "update_cve_db.py"])

def do_scan(targets):
    pats = load_patterns(Path("rules/patterns.yml"))
    findings = scan_files(targets, pats)
    out_path = REPORTS / "latest.txt"
    out_path.write_text(json.dumps(findings, indent=2))
    print(f"[+] Scan complete. Findings -> {out_path}")
    return findings

def do_simulate(url="http://localhost:8080/index.php"):
    print(f"[*] Simulating exploit against {url}")
    subprocess.run(["bash", "-lc", "sed -i 's/\\r$//' exploit.sh; chmod +x exploit.sh"])
    res = subprocess.run(["./exploit.sh", url], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr.strip():
        print(res.stderr, file=sys.stderr)

def main():
    ap = argparse.ArgumentParser(description="Local Cybersecurity AI Agent")
    ap.add_argument("--update-cve", action="store_true", help="Refresh local NVD 2.0 feed")
    ap.add_argument("--scan", nargs="+", help="Scan files")
    ap.add_argument("--simulate", nargs="?", const="http://localhost:8080/index.php",
                    help="Run exploit simulation against URL")
    args = ap.parse_args()

    if args.update_cve:
        do_update_cve()
    if args.scan:
        do_scan(args.scan)
    if args.simulate:
        do_simulate(args.simulate)
    if not any([args.update_cve, args.scan, args.simulate]):
        ap.print_help()

if __name__ == "__main__":
    main()

