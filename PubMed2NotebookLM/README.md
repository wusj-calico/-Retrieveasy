# 🔬 PubMed → Google Notebook LM Toolkit

**Automate PubMed searches and feed results directly into Google Notebook LM for AI-powered analysis.**

[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)]()

---

## 🎯 What This Does

| Step | What Happens | Time |
|------|---|---|
| 1️⃣ **Search** | Query PubMed for papers (50-1000 results) | 5-10 sec |
| 2️⃣ **Select** | Interactively choose which articles to download | 1-2 min |
| 3️⃣ **Download** | Automatically grab PDFs from open-access sources | 2-5 min |
| 4️⃣ **Upload** | Add PDFs to Google Notebook LM | 1-3 min |
| 5️⃣ **Analyze** | Use Notebook LM's AI to summarize, create guides, etc. | Instant |

**Total time: ~10-20 minutes** to go from research question to analysis-ready documents.

---

## ✨ Key Features

- ✅ **Full PubMed Integration** - Search via official NCBI API (free)
- ✅ **PDF Auto-Download** - Grabs open-access PDFs from PubMed Central
- ✅ **Interactive Selection** - Choose which papers matter to you
- ✅ **Batch Mode** - Non-interactive for automation/scripting
- ✅ **Google Notebook LM Ready** - Organized output for easy upload
- ✅ **Metadata Tracking** - JSON export for analysis & citation
- ✅ **Cross-Platform** - Works on Windows, Mac, Linux
- ✅ **Extensible** - Use as library or CLI tool

---

## 📦 What's Included

```
├── pubmed_notebook_lm.py          ← Main script (CLI tool)
├── example_usage.py               ← Interactive quick-start
├── advanced_examples.py           ← Integration code examples
├── requirements.txt               ← Python dependencies
├── SETUP_GUIDE.md                 ← Installation & how-to
├── PUBMED_NOTEBOOK_LM_README.md   ← Detailed documentation
└── README.md                      ← This file
```

---

## 🚀 Quick Start

### 1. Install

```bash
# Clone or download this repository
cd pubmed-notebook-lm

# Install dependencies (2 packages, ~30 MB)
pip install -r requirements.txt
```

### 2. Run

```bash
# Option A: Interactive mode (recommended for first time)
python example_usage.py

# Option B: Direct command line
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "CRISPR gene therapy" \
  --max-results 50
```

### 3. Upload to Notebook LM

Files are saved in `pubmed_downloads/`. The script generates instructions:

1. Go to https://notebooklm.google.com
2. Create a new notebook
3. Drag-drop PDFs from the folder
4. Ask questions or generate study guides!

---

## 💡 Example Searches

### Academic Research
```bash
python pubmed_notebook_lm.py \
  --email researcher@university.edu \
  --query "immunotherapy cancer treatment" \
  --date-from 2023 \
  --max-results 100
```

### Staying Updated in Your Field
```bash
python pubmed_notebook_lm.py \
  --email doctor@hospital.org \
  --query "precision medicine AND cardiology" \
  --date-from 2024 \
  --batch \
  --open-notebook-lm
```

### Literature Review
```bash
python pubmed_notebook_lm.py \
  --email student@school.edu \
  --query "deep learning medical imaging" \
  --date-from 2022 \
  --date-to 2024 \
  --max-results 200
```

### Preprint Combination
```bash
python pubmed_notebook_lm.py \
  --email scientist@lab.edu \
  --query "CRISPR AND (clinical trial OR treatment)" \
  --max-results 50
# Then manually add papers from bioRxiv/arXiv to Notebook LM
```

---

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation, configuration, tips
- **[PUBMED_NOTEBOOK_LM_README.md](PUBMED_NOTEBOOK_LM_README.md)** - Complete API docs
- **[advanced_examples.py](advanced_examples.py)** - Code integration examples

---

## 🎓 Use Cases

### 📚 **Student Writing Literature Review**
```
1. Search PubMed for 50 papers on topic
2. Select 15-20 most relevant
3. Upload to Notebook LM
4. Use "Create Study Guide" feature
5. Export as PDF or Google Doc
6. Incorporate findings into paper
```

### 🔬 **Researcher Tracking New Developments**
```
1. Schedule daily search for your topic (APScheduler)
2. Auto-download new papers
3. Upload to Notebook LM weekly
4. Use AI to summarize latest findings
5. Stay on top of your field
```

### 🏥 **Clinician Preparing for Patient Case**
```
1. Search for papers on patient's condition
2. Select evidence-based treatment options
3. Upload to Notebook LM
4. Generate FAQ with treatment details
5. Discuss options with patient
```

### 🤖 **Data Scientist Learning New Algorithm**
```
1. Search for papers on algorithm
2. Download implementation papers
3. Upload implementation papers + theory papers
4. Ask Notebook LM: "How does this work?"
5. Ask: "What are real-world applications?"
```

---

## ⚙️ System Requirements

- **Python**: 3.7+
- **OS**: Windows, macOS, Linux
- **Internet**: Required (PubMed API)
- **Storage**: ~100 MB per 20 PDFs
- **RAM**: 200 MB minimum
- **Google Account**: Free (for Notebook LM)

### Dependencies
- `biopython` - NCBI/PubMed interface
- `requests` - HTTP client for downloads
- (Optional) `pandas` - for advanced analysis

---

## 🔐 Privacy & Security

- ✅ **No login required** - Uses free NCBI API
- ✅ **No data stored** - All local processing
- ✅ **Open source** - Fully transparent code
- ✅ **Your email only** - Required by NCBI only
- ✅ **PDF downloads** - From official PubMed Central
- ✅ **Google integration** - Via your Google account only

---

## 📊 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Search PubMed | 5-10 sec | ~3 requests/sec (faster with API key) |
| Download 10 PDFs | 1-2 min | Depends on file size & internet |
| Upload to Notebook LM | ~1 min | Manual drag-drop (or API in future) |
| Process by Notebook LM | ~2-3 min | Per document, first time |

---

## 🛠️ Advanced Features

### Use as a Python Library
```python
from pubmed_notebook_lm import PubMedSearcher

searcher = PubMedSearcher(email="you@example.com")
articles = searcher.search("machine learning", max_results=50)

for article in articles[:5]:
    pdf_url = searcher.get_full_text_url(article['pmid'])
    if pdf_url:
        searcher.download_pdf(pdf_url, f"pdfs/{article['pmid']}.pdf")
```

### Batch Processing
```python
# See advanced_examples.py for:
# - Searching multiple topics
# - Smart filtering by criteria
# - Citation export (BibTeX, CSV)
# - Scheduled searches
# - HTML report generation
# - Pandas analysis
```

### NCBI API Key (Faster Requests)
Get free at: https://www.ncbi.nlm.nih.gov/account/

```bash
python pubmed_notebook_lm.py \
  --email user@example.com \
  --api-key YOUR_API_KEY \
  --query "your topic"
```

---

## ❓ FAQ

**Q: Can I download paywalled papers?**  
A: No. Only open-access papers from PubMed Central. For others, contact authors or use your institution's access.

**Q: Does Notebook LM have an API?**  
A: Not yet (as of Jan 2026). Manual upload required, but Google may release API soon.

**Q: How many papers can Notebook LM handle?**  
A: Typically 200+ documents, but performance may degrade. Start with 10-50.

**Q: Can I schedule automatic searches?**  
A: Yes! Use `APScheduler` or cron jobs. See advanced_examples.py.

**Q: Is this affiliated with Google or NCBI?**  
A: No. This is an independent tool using their free public APIs.

**Q: Works offline?**  
A: No. Requires internet to query PubMed and download PDFs.

**Q: Can I use with institutional access (paywalled) PDFs?**  
A: Partially. You'd need to manually add them to Notebook LM separately.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No PDF found" | Article not in PMC; try ResearchGate/author's site |
| "Email not provided" | Use valid email with `--email your@real.email` |
| "Connection timeout" | Try `--api-key`, reduce `--max-results`, check internet |
| "Permission denied" | Check output folder exists and is writable |
| No results | Check query spelling, broaden terms, remove filters |

See **SETUP_GUIDE.md** for more troubleshooting.

---

## 🚀 Roadmap

- [x] PubMed search & download
- [x] Interactive selection
- [x] Notebook LM integration
- [x] CLI tool
- [ ] Notebook LM API support (when Google releases it)
- [ ] Automatic scheduled searches
- [ ] Web UI dashboard
- [ ] Support for other databases (arXiv, bioRxiv)
- [ ] PDF text extraction & analysis
- [ ] Citation format generation
- [ ] Zotero/Mendeley integration

---

## 📝 License

MIT License - Use freely, including commercially.

---

## 🤝 Contributing

Found a bug? Have an idea? Contributions welcome!

1. Test your change
2. Update documentation if needed
3. Submit issue/PR

---

## 📞 Support

- **Docs**: See SETUP_GUIDE.md and advanced_examples.py
- **Issues**: Check troubleshooting section
- **Questions**: Review commented examples in the code

---

## 🎉 Getting Started NOW

**3 commands to get started:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run interactive mode
python example_usage.py

# 3. Upload PDFs to Notebook LM (browser)
# Files are ready in pubmed_downloads/
```

**That's it!** 🚀

---

**Made with ❤️ for researchers, students, and curious minds.**

*Last Updated: January 2026*
