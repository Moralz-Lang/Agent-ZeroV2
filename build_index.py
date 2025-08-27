#!/usr/bin/env python3
from pathlib import Path
import json, faiss, numpy as np
from sentence_transformers import SentenceTransformer

JSON_PATH = Path("data/nvd/recent.json")
INDEX_DIR = Path("data/index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

def load_cves_v2():
    # NVD 2.0 structure: {"vulnerabilities":[{"cve":{"id":"CVE-...","descriptions":[{"value": "..."}], ...}}]}
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    cves = []
    for v in data.get("vulnerabilities", []):
        cve = v.get("cve", {})
        cid = cve.get("id", "NA")
        descs = cve.get("descriptions", [])
        desc = descs[0]["value"] if descs else ""
        cves.append({"id": cid, "description": desc})
    return cves

def main():
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    cves = load_cves_v2()
    texts = [c["description"] for c in cves]
    if not texts:
        raise SystemExit("No CVE descriptions found in recent.json")
    embs = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    embs = embs.astype(np.float32)
    d = embs.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embs)
    faiss.write_index(index, str(INDEX_DIR / "cve.index"))
    (INDEX_DIR / "meta.json").write_text(json.dumps(cves))
    print("[+] FAISS index built at data/index/cve.index")

if __name__ == "__main__":
    main()

