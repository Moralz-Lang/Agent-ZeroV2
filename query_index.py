#!/usr/bin/env python3
from pathlib import Path
import json, faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import sys

INDEX_DIR = Path("data/index")

def main():
    query = " ".join(sys.argv[1:]) or "Buffer overflow in Apache"
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    index = faiss.read_index(str(INDEX_DIR / "cve.index"))
    meta = json.loads((INDEX_DIR / "meta.json").read_text())
    qv = model.encode([query], convert_to_numpy=True).astype(np.float32)
    D, I = index.search(qv, k=5)
    for rank, idx in enumerate(I[0].tolist(), 1):
        print(f"{rank}. {meta[idx]['id']}  {meta[idx]['description'][:120]}...")

if __name__ == "__main__":
    main()

