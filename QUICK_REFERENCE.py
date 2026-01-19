#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         QUICK REFERENCE: PubMed → Google Notebook LM Toolkit                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

QUICK_START = """
┌─ INSTALLATION ────────────────────────────────────────────────────────────┐
│                                                                             │
│  pip install -r requirements.txt                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

BASIC_COMMANDS = """
┌─ BASIC COMMANDS ──────────────────────────────────────────────────────────┐
│                                                                             │
│  # Interactive mode (recommended)                                          │
│  python example_usage.py                                                   │
│                                                                             │
│  # Simple search                                                           │
│  python pubmed_notebook_lm.py \\                                           │
│    --email you@example.com \\                                              │
│    --query "CRISPR"                                                        │
│                                                                             │
│  # Advanced search with date filter                                        │
│  python pubmed_notebook_lm.py \\                                           │
│    --email you@example.com \\                                              │
│    --query "immunotherapy cancer" \\                                       │
│    --date-from 2023 \\                                                     │
│    --date-to 2024 \\                                                       │
│    --max-results 50                                                        │
│                                                                             │
│  # Batch mode (no prompting)                                               │
│  python pubmed_notebook_lm.py \\                                           │
│    --email you@example.com \\                                              │
│    --query "deep learning" \\                                              │
│    --batch \\                                                              │
│    --open-notebook-lm                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

COMMON_SEARCHES = """
┌─ COMMON RESEARCH QUERIES ─────────────────────────────────────────────────┐
│                                                                             │
│  Cancer Research:                                                          │
│    --query "immunotherapy cancer treatment"                                │
│                                                                             │
│  Gene Therapy:                                                             │
│    --query "CRISPR gene therapy clinical trials"                           │
│                                                                             │
│  AI in Medicine:                                                           │
│    --query "deep learning medical imaging diagnosis"                       │
│                                                                             │
│  COVID-19:                                                                 │
│    --query "COVID-19 vaccine efficacy variants"                            │
│                                                                             │
│  Neuroscience:                                                             │
│    --query "neuroinflammation Alzheimer disease treatment"                 │
│                                                                             │
│  By Author:                                                                │
│    --query "Smith J[Author] AND machine learning"                          │
│                                                                             │
│  Review Articles Only:                                                     │
│    --query "topic AND (review[PT] OR meta-analysis[PT])"                   │
│                                                                             │
│  Clinical Trials:                                                          │
│    --query "drug AND (clinical trial[PT] OR RCT)"                          │
│                                                                             │
│  Recent & Broad:                                                           │
│    --query "your topic" --date-from 2024 --max-results 100                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

ARGUMENTS_REFERENCE = """
┌─ ARGUMENT REFERENCE ──────────────────────────────────────────────────────┐
│                                                                             │
│  REQUIRED:                                                                 │
│    --email ADDR                Email (required by NCBI)                    │
│    --query TEXT                Search terms                                │
│                                                                             │
│  OPTIONAL:                                                                 │
│    --api-key KEY               NCBI API key (faster, get at NCBI)          │
│    --max-results N             Results to fetch (default: 50)              │
│    --date-from YYYY            Start year/date                             │
│    --date-to YYYY              End year/date                               │
│    --output-dir PATH           Where to save PDFs (default: ./pd_downloads)│
│    --batch                     Non-interactive mode                        │
│    --open-notebook-lm          Open Notebook LM when done                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

WORKFLOW = """
┌─ TYPICAL WORKFLOW ────────────────────────────────────────────────────────┐
│                                                                             │
│  1. SEARCH                                                                 │
│     python pubmed_notebook_lm.py --email you@ex.com --query "your topic"  │
│                                                                             │
│  2. SELECT (interactive mode)                                              │
│     Enter: 1 2 3 5                                                         │
│     (or: 1-5 for range, or: all for all results)                           │
│                                                                             │
│  3. DOWNLOAD                                                               │
│     Script downloads PDFs to pubmed_downloads/                             │
│                                                                             │
│  4. UPLOAD                                                                 │
│     Go to https://notebooklm.google.com                                    │
│     Drag-drop PDFs from pubmed_downloads/                                  │
│                                                                             │
│  5. ANALYZE                                                                │
│     Click "Ask NotebookLM"                                                 │
│     Ask questions or generate study guides                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

OUTPUT_FILES = """
┌─ OUTPUT FILES ────────────────────────────────────────────────────────────┐
│                                                                             │
│  pubmed_downloads/                                                         │
│  ├── PMID_ArticleTitle.pdf              ← Downloaded PDF files             │
│  ├── PMID_ArticleTitle.pdf                                                 │
│  ├── search_metadata.json               ← Article metadata (JSON)         │
│  └── NOTEBOOK_LM_INSTRUCTIONS.txt       ← Upload guide                    │
│                                                                             │
│  Files ready to upload to Google Notebook LM!                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

TROUBLESHOOTING = """
┌─ TROUBLESHOOTING ─────────────────────────────────────────────────────────┐
│                                                                             │
│  Issue: "No results found"                                                 │
│  → Check query spelling, try simpler terms, remove date filters            │
│                                                                             │
│  Issue: "No PDF found"                                                     │
│  → Article not in PubMed Central; try ResearchGate or author's site        │
│                                                                             │
│  Issue: "Email not provided"                                               │
│  → Use --email with valid email address (doesn't need to be verified)      │
│                                                                             │
│  Issue: "Connection timeout"                                               │
│  → Get NCBI API key (speeds up requests), or reduce --max-results          │
│                                                                             │
│  Issue: "Permission denied"                                                │
│  → Check output directory exists and is writable                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

TIPS = """
┌─ TIPS & TRICKS ───────────────────────────────────────────────────────────┐
│                                                                             │
│  ✓ Get NCBI API Key for 3x faster requests:                               │
│    https://www.ncbi.nlm.nih.gov/account/                                   │
│                                                                             │
│  ✓ Use boolean operators in queries:                                       │
│    --query "cancer AND (immunotherapy OR vaccine)"                         │
│                                                                             │
│  ✓ Organize by topic:                                                      │
│    --output-dir ~/research/cancer_2024                                     │
│                                                                             │
│  ✓ Use in Python scripts:                                                  │
│    from pubmed_notebook_lm import PubMedSearcher                           │
│    searcher = PubMedSearcher(email="you@ex.com")                           │
│    articles = searcher.search("query")                                     │
│                                                                             │
│  ✓ Export to BibTeX, CSV, etc (see advanced_examples.py)                   │
│                                                                             │
│  ✓ Combine with other sources:                                             │
│    Download from PubMed, add preprints (bioRxiv, arXiv) manually           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

LINKS = """
┌─ USEFUL LINKS ────────────────────────────────────────────────────────────┐
│                                                                             │
│  PubMed:           https://pubmed.ncbi.nlm.nih.gov/                        │
│  NCBI API Key:     https://www.ncbi.nlm.nih.gov/account/                   │
│  PubMed Central:   https://www.ncbi.nlm.nih.gov/pmc/                       │
│  Notebook LM:      https://notebooklm.google.com                           │
│  bioRxiv:          https://www.biorxiv.org/ (preprints)                    │
│  arXiv:            https://arxiv.org/ (physics/CS preprints)               │
│  PubMed Search:    https://pubmed.ncbi.nlm.nih.gov/help/                   │
│                                                                             │
│  Documentation:                                                            │
│    - README.md                                                             │
│    - SETUP_GUIDE.md                                                        │
│    - PUBMED_NOTEBOOK_LM_README.md                                          │
│    - advanced_examples.py                                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

def main():
    """Print quick reference"""
    print(QUICK_START)
    print(BASIC_COMMANDS)
    print(COMMON_SEARCHES)
    print(ARGUMENTS_REFERENCE)
    print(WORKFLOW)
    print(OUTPUT_FILES)
    print(TROUBLESHOOTING)
    print(TIPS)
    print(LINKS)
    print("\n✨ Ready to start? Run: python example_usage.py\n")

if __name__ == "__main__":
    main()
