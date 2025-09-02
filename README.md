# Agent-ZeroV2
# ⚡ Local AI Vulnerability Scanning Agent

---

## 📖 Table of Contents

1. 🛠️ Overview  
2. 📁 Directory Structure  
3. 🐍 Installation & Virtual Environment  
4. 📦 Python Dependencies  
5. 🚀 Running the Agent Manually  
6. 🔄 Updating CVE Database  
7. 📝 Generating & Updating Patterns  
8. 🔍 Scanning Targets  
9. 🧠 Semantic Classification (FAISS + Transformers)  
10. ⏰ Cron Job Automation  
11. 📜 Viewing Logs  
12. 🐳 Docker Integration  
13. 🌟 Key Features  
14. 🛠️ Fixes & Updates in This Version  
15. 🎯 Best Use Cases  
16. 💻 GitHub Integration & Contribution  
17. ⚠️ Security & Safety Notes  
18. 🔮 Future Recommendations  
19. 📚 References  

---

## 🛠️ 1. Overview

This **Local AI Vulnerability Scanning Agent** automatically:

- 📥 Downloads & updates CVE feeds from NVD  
- 🔍 Parses CVE JSON for vulnerabilities like **XSS, SQLi, RCE**  
- 📝 Generates and updates `rules/patterns.yml` automatically  
- 🧠 Uses **FAISS** + **sentence-transformers** for semantic classification  
- 🛡️ Simulates payloads safely (`simulation_only: true`)  
- 🐳 Provides Docker integration for isolated testing  

---

## 📁 2. Directory Structure

```

local-ai-agent/
├─ ai\_agent.py                # Main orchestration script
├─ scanner.py                 # Core scanning script
├─ run\_exploit.py             # Optional exploit simulation
├─ generate\_patterns.py       # Generate/update YAML patterns from CVEs
├─ update\_cve\_db.py           # Download & extract CVE JSON
├─ build\_index.py             # Build FAISS embedding index
├─ query\_index.py             # Query FAISS index for semantic CVE matching
├─ exploit.sh                 # Bash exploit helper
├─ requirements.txt           # Python dependencies
├─ README.md                  # Documentation
├─ Dockerfile                 # Base Dockerfile
├─ Dockerfile.runner          # Runner container for AI agent
├─ Dockerfile.vuln-apache     # Vulnerable Apache container
├─ docker-compose.yml         # Compose multiple containers
├─ data/                      # CVE JSON & extracted files
│   └─ nvd/recent.json
├─ logs/                      # Cron & execution logs
├─ reports/                   # Scan result reports
├─ rules/
│   └─ patterns.yml           # Vulnerability pattern rules
└─ venv/                      # Python virtual environment

````

---

## 🐍 3. Installation & Virtual Environment

```bash
# Clone repository
git clone https://github.com/<your-username>/local-ai-agent.git
cd local-ai-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip & install dependencies
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
````

---

## 📦 4. Python Dependencies

* `faiss-cpu==1.12.0` → vector indexing for semantic search 🧠
* `sentence-transformers==5.1.0` → embeddings for CVE descriptions 📝
* `requests==2.32.3` → HTTP downloads 🌐
* `PyYAML==6.0.2` → read/write patterns YAML 📄
* `numpy==1.26.4` → numeric operations 🔢
* `regex==2024.7.24` → regex pattern matching 🔎
* `docker==7.1.0` → container integration 🐳
* `paramiko==3.4.0` → SSH for optional remote interactions 🔑
* `bandit==1.7.9` → static security testing ⚔️

---

## 🚀 5. Running the Agent Manually

```bash
# Update CVE database
python update_cve_db.py

# Generate/update patterns
python generate_patterns.py

# Build FAISS semantic index
python build_index.py

# Run scanner
python scanner.py

# Or orchestrate full agent
python ai_agent.py --update-cve --scan rules/static/sample-configs/apache.conf rules/static/sample-configs/mysql.cnf --simulate "http://localhost:8080/"
```

---

## 🔄 6. Updating CVE Database

* Downloads NVD JSON feed (`data/nvd/recent.json`)
* Optional SHA256 verification (skips if missing)
* Extracts JSON from `.gz`
* Avoids overwriting errors ✅

---

## 📝 7. Generating & Updating Patterns

* Parses CVE JSON for **XSS, SQLi, RCE**
* Maps to `rules/patterns.yml`
* Fields: `simulation_only`, `method`, `parameter`
* Supports version & software filtering
* Semantic classification for accurate mapping

---

## 🔍 8. Pattern YAML Example

```yaml
- name: cve-2025-1111
  description: "Login form fails to sanitize input, allows XSS attacks"
  payloads:
    - "<script>alert(1)</script>"
  method: GET
  parameter: q
  simulation_only: true
```

---

## 🧠 9. Semantic Classification

* **FAISS:** Efficient similarity search on CVE embeddings 🔗
* **sentence-transformers:** Converts CVE descriptions into embeddings 🧠
* Matches new CVEs with existing known vulnerabilities
* Automates classification, reduces manual updates

---

## ⏰ 10. Cron Job Automation

```cron
# Update CVE DB daily at 03:00
0 3 * * * /home/vboxuser/local-ai-agent/venv/bin/python /home/vboxuser/local-ai-agent/update_cve_db.py >> /home/vboxuser/local-ai-agent/logs/cve_update.log 2>&1

# Generate patterns at 05:00
0 5 * * * /home/vboxuser/local-ai-agent/venv/bin/python /home/vboxuser/local-ai-agent/generate_patterns.py >> /home/vboxuser/local-ai-agent/logs/pattern_update.log 2>&1

# Build index at 06:00
0 6 * * * /home/vboxuser/local-ai-agent/venv/bin/python /home/vboxuser/local-ai-agent/build_index.py >> /home/vboxuser/local-ai-agent/logs/index_build.log 2>&1
```

* Ensure logs directory exists:

```bash
mkdir -p logs
```

---

## 📜 11. Viewing Logs

```bash
# Full log
cat logs/cve_update.log

# Last 50 lines
tail -n 50 logs/pattern_update.log

# Follow real-time updates
tail -f logs/index_build.log
```

---

## 🐳 12. Docker Integration

```bash
# Run test vulnerable container
docker run -d --name lab-web -p 8080:80 vuln-apache
docker ps --filter "name=lab-web"

# Remove conflicting containers
docker rm -f lab-web

# Scan locally
python ai_agent.py --simulate "http://localhost:8080/"
```

---

## 🌟 13. Key Features

* 📥 Automated CVE download & parsing
* 📝 Pattern generation from CVEs
* 🧠 Semantic classification with FAISS + Transformers
* 🔧 Version & software filtering
* 🛡️ Simulation-only safe execution
* 🐳 Docker-based target environments
* ⏰ Cron automation & logging
* 📊 Reports generation

---

## 🛠️ 14. Fixes & Updates

* SHA256 optional verification ✅
* Flattened `patterns.yml` structure handling
* Added `simulation_only` field
* Semantic classification added (FAISS + Transformers)
* Cron automation & logging fixes
* Manual execution clarified

---

## 🎯 15. Best Use Cases

* Web app testing (XSS, SQLi, RCE) 🌐
* Automated CVE tracking 🗂️
* Safe vulnerability simulation 🛡️
* Research & training environments 🎓
* PHP, JavaScript, Node.js, React, MySQL testing

---

## 💻 16. GitHub Integration

```bash
git init
git add .
git commit -m "Updated agent with semantic CVE classification & cron automation"
git branch -M main
git remote add origin https://github.com/<your-username>/local-ai-agent.git
git push -u origin main
```

* Users can clone, create venv, install requirements, and run scripts immediately ✅

---

## ⚠️ 17. Security & Safety Notes

* `simulation_only: true` prevents destructive execution
* Test in Docker / isolated environments
* Never run on production without permission
* Payloads are examples; adjust safely

---

## 🔮 18. Future Recommendations

* Continuous CVE updates via API/webhooks
* Multi-language CVE parsing 🌏
* Auto-version mapping for PHP/Node.js/Python
* Reporting dashboard 📊
* Integration with OWASP ZAP or Nikto

---

## 📚 19. References

* [NVD CVE JSON](https://nvd.nist.gov/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Sentence Transformers](https://www.sbert.net/)
* [Python Requests](https://docs.python-requests.org/)
* [PyYAML](https://pyyaml.org/)



