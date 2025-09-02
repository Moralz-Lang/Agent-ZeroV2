#!/usr/bin/env python3
import requests
import gzip
import shutil
import hashlib
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "nvd"

# URLs
NVD_JSON_URL = "https://nvd.nist.gov/feeds/json/cve/2.0/nvdcve-2.0-recent.json.gz"
SHA256_URL = NVD_JSON_URL + ".sha256"

# Paths
GZ_PATH = DATA_DIR / "recent.json.gz"
JSON_PATH = DATA_DIR / "recent.json"

def download(url, path):
    """Download file from URL to local path"""
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

def verify_sha256(file_path, sha_line):
    """Verify SHA256 checksum of file against provided hash"""
    expected = sha_line.strip().split()[0]  # some .sha256 files contain "hash filename"
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest() == expected

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("[+] Downloading CVE feed (NVD 2.0)...")
    download(NVD_JSON_URL, GZ_PATH)

    # SHA256 optional
    try:
        sha_resp = requests.head(SHA256_URL)
        if sha_resp.status_code == 200:
            print("[+] Downloading SHA256...")
            sha_path = DATA_DIR / "recent.json.gz.sha256"
            download(SHA256_URL, sha_path)
            with open(sha_path) as f:
                sha_line = f.read()
            print("[*] Verifying checksum...")
            if not verify_sha256(GZ_PATH, sha_line):
                raise SystemExit("[-] SHA256 mismatch. Aborting.")
        else:
            print("[!] SHA256 not found, skipping verification.")
    except Exception as e:
        print(f"[!] SHA256 check skipped: {e}")

    print("[+] Extracting JSON...")
    with gzip.open(GZ_PATH, "rb") as fin, open(JSON_PATH, "wb") as fout:
        shutil.copyfileobj(fin, fout)

    print(f"[+] Ready: {JSON_PATH.resolve()}")

if __name__ == "__main__":
    main()





