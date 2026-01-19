#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║      PubMed → Google Notebook LM Toolkit — File Index & Quick Start        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

INDEX = """
┌────────────────────────────────────────────────────────────────────────────┐
│                      📁 TOOLKIT FILES (10 total)                           │
└────────────────────────────────────────────────────────────────────────────┘

CORE SCRIPTS
─────────────────────────────────────────────────────────────────────────────
1. pubmed_notebook_lm.py          [19 KB] Main CLI script
   → Full PubMed search & PDF download functionality
   → Use with: python3 pubmed_notebook_lm.py --email you@ex.com --query "..."
   → Supports all features: filtering, batch mode, etc.

2. example_usage.py               [3.4 KB] Interactive quick-start
   → Guided prompts for first-time users
   → Pre-configured search topics
   → Use with: python3 example_usage.py

3. advanced_examples.py           [12 KB] Integration code examples
   → Library usage (import into your code)
   → Batch processing multiple topics
   → Citation export (BibTeX, CSV)
   → Scheduled searches
   → Pandas analysis
   → HTML report generation
   → Copy & adapt these for your workflow

DEPENDENCIES
─────────────────────────────────────────────────────────────────────────────
4. requirements.txt               [31 B] Python package list
   → Contains: biopython, requests
   → Install with: pip install -r requirements.txt

DOCUMENTATION
─────────────────────────────────────────────────────────────────────────────
5. README.md                      [9.2 KB] Overview & features
   → Features, use cases, system requirements
   → FAQ and troubleshooting
   → License info
   → START HERE for overview

6. SETUP_GUIDE.md                 [9.2 KB] Installation & how-to guide
   → Step-by-step installation
   → Common use cases with examples
   → Tips & best practices
   → Troubleshooting detailed help
   → SETUP GUIDE for getting started

7. PUBMED_NOTEBOOK_LM_README.md   [11 KB] Complete API documentation
   → All command-line arguments
   → Input/output formats
   → Advanced features
   → API reference
   → TECHNICAL REFERENCE

8. DELIVERY_SUMMARY.md            [8.5 KB] What was delivered
   → Overview of what you got
   → How to get started (3 steps)
   → Features checklist
   → What files do what
   → DELIVERY NOTES & SUMMARY

REFERENCE
─────────────────────────────────────────────────────────────────────────────
9. QUICK_REFERENCE.py             [~2 KB] Printable quick reference
   → Common commands
   → Search query examples
   → Argument reference
   → Workflow diagram
   → Troubleshooting guide
   → Run: python3 QUICK_REFERENCE.py

10. INDEX.md (this file)           Quick navigation guide


┌────────────────────────────────────────────────────────────────────────────┐
│                    🚀 QUICK START (Choose One)                             │
└────────────────────────────────────────────────────────────────────────────┘

OPTION A: Interactive Mode (Recommended for First Time)
──────────────────────────────────────────────────────
$ pip install -r requirements.txt
$ python3 example_usage.py
  → Follow prompts
  → Select from preset topics or custom query
  → Auto-downloads PDFs

OPTION B: Direct Command Line
──────────────────────────────
$ python3 pubmed_notebook_lm.py \\
    --email your.email@example.com \\
    --query "CRISPR gene therapy"
  → Interactively select articles
  → Downloads PDFs
  → Shows instructions

OPTION C: Batch Mode (No Prompting)
────────────────────────────────────
$ python3 pubmed_notebook_lm.py \\
    --email your.email@example.com \\
    --query "immunotherapy cancer" \\
    --batch \\
    --max-results 50
  → Downloads everything automatically
  → Good for automation/scripts


┌────────────────────────────────────────────────────────────────────────────┐
│                      📚 WHICH FILE TO READ?                                │
└────────────────────────────────────────────────────────────────────────────┘

IF YOU WANT TO...                          READ...
─────────────────────────────────────────────────────────────────────────────
Understand what this toolkit does          → README.md
Get started in 5 minutes                   → SETUP_GUIDE.md (first section)
Learn all command-line options             → PUBMED_NOTEBOOK_LM_README.md
See code integration examples              → advanced_examples.py
Quick command reference                    → python3 QUICK_REFERENCE.py
Understand what you received               → DELIVERY_SUMMARY.md
See typical workflows                      → SETUP_GUIDE.md (use cases)
Learn troubleshooting                      → SETUP_GUIDE.md (troubleshooting)
Find all useful links                      → README.md or QUICK_REFERENCE.py
Use as Python library                      → advanced_examples.py
See API reference                          → PUBMED_NOTEBOOK_LM_README.md


┌────────────────────────────────────────────────────────────────────────────┐
│                    💡 COMMON WORKFLOWS                                      │
└────────────────────────────────────────────────────────────────────────────┘

WORKFLOW 1: First-Time User
───────────────────────────
1. Read: README.md (5 min)
2. Read: SETUP_GUIDE.md - Quick Start section (5 min)
3. Run: python3 example_usage.py (5 min)
4. Follow on-screen instructions
5. Use outputs in Google Notebook LM

WORKFLOW 2: Academic Researcher
────────────────────────────────
1. Read: SETUP_GUIDE.md - Use Cases section
2. Run: Custom search with multiple topics
3. Export metadata.json
4. Analyze with advanced_examples.py (Pandas section)
5. Upload best papers to Notebook LM

WORKFLOW 3: Automation / Scheduled Searches
────────────────────────────────────────────
1. Read: advanced_examples.py - Scheduled section
2. Set up APScheduler or cron job
3. Run daily/weekly automatically
4. Organize by date/topic
5. Batch upload to Notebook LM

WORKFLOW 4: Integration with Existing Code
───────────────────────────────────────────
1. Read: advanced_examples.py - Library usage example
2. Import: from pubmed_notebook_lm import PubMedSearcher
3. Use in your Python project
4. Customize as needed


┌────────────────────────────────────────────────────────────────────────────┐
│                    🔧 INSTALLATION                                         │
└────────────────────────────────────────────────────────────────────────────┘

STEP 1: Install Python 3.7+
────────────────────────────
$ python3 --version          # Check your version

STEP 2: Install Dependencies
──────────────────────────────
$ pip install -r requirements.txt

   This installs:
   - biopython (NCBI/PubMed interface)
   - requests (HTTP client for PDFs)

STEP 3: Verify Installation
─────────────────────────────
$ python3 -c "import Bio; import requests; print('✓ Ready!')"

OPTIONAL STEP 4: Get NCBI API Key
──────────────────────────────────
For 3x faster requests (optional):
  → Visit: https://www.ncbi.nlm.nih.gov/account/
  → Sign up / sign in
  → Copy API key
  → Use with: --api-key YOUR_KEY


┌────────────────────────────────────────────────────────────────────────────┐
│                    ⚡ MOST COMMON COMMANDS                                  │
└────────────────────────────────────────────────────────────────────────────┘

# Simple search
python3 pubmed_notebook_lm.py --email you@ex.com --query "cancer"

# With date filter
python3 pubmed_notebook_lm.py --email you@ex.com --query "cancer" \\
  --date-from 2023 --date-to 2024

# With API key (faster)
python3 pubmed_notebook_lm.py --email you@ex.com --api-key YOUR_KEY \\
  --query "your topic"

# Download 10 most recent papers
python3 pubmed_notebook_lm.py --email you@ex.com \\
  --query "your topic" --max-results 10 --batch

# Get quick reference
python3 QUICK_REFERENCE.py

# See help
python3 pubmed_notebook_lm.py --help


┌────────────────────────────────────────────────────────────────────────────┐
│                    📂 OUTPUT STRUCTURE                                      │
└────────────────────────────────────────────────────────────────────────────┘

After running, you'll find:

pubmed_downloads/
├── PMID_ArticleTitle.pdf       ← Downloaded PDF files
├── PMID_ArticleTitle.pdf
├── search_metadata.json        ← Article metadata (JSON)
└── NOTEBOOK_LM_INSTRUCTIONS.txt ← Step-by-step upload guide

Ready to upload to Google Notebook LM!


┌────────────────────────────────────────────────────────────────────────────┐
│                    ✅ VERIFICATION CHECKLIST                                │
└────────────────────────────────────────────────────────────────────────────┘

Before running first search:
[ ] Python 3.7+ installed        → python3 --version
[ ] Dependencies installed       → pip install -r requirements.txt
[ ] Valid email ready            → your.email@example.com
[ ] Internet connection working  → ping google.com
[ ] Google account ready         → gmail.com or other Google account
[ ] (Optional) API key obtained  → https://www.ncbi.nlm.nih.gov/account/


┌────────────────────────────────────────────────────────────────────────────┐
│                    🎯 NEXT STEPS                                            │
└────────────────────────────────────────────────────────────────────────────┘

RIGHT NOW (Next 5 minutes):
  1. Install: pip install -r requirements.txt
  2. Run: python3 example_usage.py
  3. Follow prompts

SOON (Next 30 minutes):
  1. Download your first papers
  2. Upload to Google Notebook LM
  3. Explore Notebook LM features (Ask, Study Guide, FAQ)

THIS WEEK (Optional):
  1. Get NCBI API key
  2. Explore advanced_examples.py
  3. Set up scheduled searches
  4. Integrate into your workflow


┌────────────────────────────────────────────────────────────────────────────┐
│                    📞 NEED HELP?                                            │
└────────────────────────────────────────────────────────────────────────────┘

1. Check documentation:
   - README.md (overview)
   - SETUP_GUIDE.md (how-to)
   - PUBMED_NOTEBOOK_LM_README.md (detailed)
   - DELIVERY_SUMMARY.md (what you got)

2. Quick reference:
   - python3 QUICK_REFERENCE.py

3. Code examples:
   - advanced_examples.py

4. Common issues:
   - SETUP_GUIDE.md → Troubleshooting section


╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  You're all set! Start with:  python3 example_usage.py                   ║
║                                                                            ║
║  Questions? Check the documentation files listed above.                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(INDEX)
