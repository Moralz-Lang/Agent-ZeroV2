
#!/usr/bin/env python3
"""
generate_patterns.py
Automatically generate .yml patterns from CVE JSON.
Includes keyword matching, default payloads, and semantic classification using FAISS + sentence-transformers.
"""

import json
import yaml
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Files
CVE_JSON = Path("data/nvd/recent.json")
PATTERN_YML = Path("rules/patterns.yml")

# Keyword detection with default payloads
KEYWORDS = {
    "xss": {
        "keywords": ["cross-site scripting", "xss"],
        "payloads": ["<script>alert(1)</script>"]
    },
    "sql_injection": {
        "keywords": ["sql injection", "sqli", "database error"],
        "payloads": ["' OR '1'='1", "'; DROP TABLE users; --"]
    },
    "rce": {
        "keywords": ["remote code execution", "rce", "arbitrary code"],
        "payloads": ["<?php system('id'); ?>"]
    }
}


def load_cves():
    """Load CVEs from the downloaded JSON (NVD 2.0 format)."""
    with open(CVE_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("vulnerabilities", [])


def detect_type(description):
    """Return vulnerability type based on keywords."""
    desc_lower = description.lower()
    for vuln_type, info in KEYWORDS.items():
        for kw in info["keywords"]:
            if kw in desc_lower:
                return vuln_type
    return None


def generate_patterns():
    """Generate patterns from CVE JSON using keyword matching."""
    cves = load_cves()
    patterns = []

    for item in cves:
        cve_id = item["cve"]["id"]
        # English description
        desc = next((d["value"] for d in item["cve"]["descriptions"] if d["lang"] == "en"), "")
        vuln_type = detect_type(desc)

        if vuln_type:
            pattern = {
                "name": cve_id,
                "description": desc[:120] + "...",
                "payloads": KEYWORDS[vuln_type]["payloads"],
                "method": "GET" if vuln_type in ["xss", "sql_injection"] else "POST",
                "parameter": "input",
                "simulation_only": True  # safety flag
            }
            patterns.append(pattern)

    return patterns


def add_semantic_patterns(patterns, model_name='all-MiniLM-L6-v2'):
    """
    Use sentence-transformers + FAISS to classify new CVEs semantically.
    Returns FAISS index and model for future similarity search.
    """
    if not patterns:
        return None, None

    model = SentenceTransformer(model_name)
    descriptions = [p['description'] for p in patterns]
    embeddings = model.encode(descriptions, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, model

def save_patterns(patterns):
    PATTERN_YML.parent.mkdir(parents=True, exist_ok=True)

    if PATTERN_YML.exists():
        existing_yaml = yaml.safe_load(PATTERN_YML.read_text()) or {}
        existing_patterns = existing_yaml.get("patterns", [])
        # Only keep dicts with 'name' key
        existing_patterns = [p for p in existing_patterns if isinstance(p, dict) and 'name' in p]
        existing_ids = {p['name'] for p in existing_patterns}
        patterns = [p for p in patterns if p['name'] not in existing_ids]
        all_patterns = existing_patterns + patterns
    else:
        all_patterns = patterns

    with open(PATTERN_YML, "w", encoding="utf-8") as f:
        yaml.dump({"patterns": all_patterns}, f, sort_keys=False)




def main():
    print("[+] Generating patterns from CVE JSON...")
    new_patterns = generate_patterns()
    index, model = add_semantic_patterns(new_patterns)  # optional semantic similarity index
    save_patterns(new_patterns)
    print(f"[+] Saved {len(new_patterns)} new patterns to {PATTERN_YML}")

    # Example of semantic search (optional)
    if index is not None:
        query = model.encode(["Remote SQL injection in Node.js"], convert_to_numpy=True)
        D, I = index.search(query, k=5)
        print("[*] Top semantic matches for sample query:")
        for idx in I[0]:
            print(new_patterns[idx])


if __name__ == "__main__":
    main()
