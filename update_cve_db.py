# detect if SHA256 exists
import requests

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

