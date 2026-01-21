# 🔬 PubMed Search → Google Notebook LM Setup Guide

## ✨ What You Can Do

This toolkit lets you:
1. **Search PubMed** with keywords, date ranges, and boolean operators
2. **Interactively select** which articles to download
3. **Automatically download PDFs** from open-access sources (PubMed Central)
4. **Prepare documents** for Google Notebook LM
5. **Generate summaries, FAQs, study guides** using Notebook LM's AI

**Example**: Find 50 papers on "CRISPR gene therapy", download the 10 most relevant, and upload to Notebook LM for analysis—all in minutes.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `biopython` - Interface to NCBI/PubMed (free)
- `requests` - HTTP library for downloading PDFs

### Step 2: Run the Interactive Example

```bash
python example_usage.py
```

This will prompt you to:
- Choose a research topic (or enter custom query)
- Enter your email (required by NCBI)
- Optionally provide NCBI API key
- Choose whether to open Notebook LM automatically

### Step 3: Upload to Notebook LM

The script generates step-by-step instructions. Simply:
1. Go to https://notebooklm.google.com
2. Create a new notebook
3. Drag-and-drop the PDFs from `pubmed_downloads/`
4. Use Notebook LM's AI features (Ask, Create Study Guide, etc.)

---

## 📋 Common Use Cases

### Case 1: Quick Literature Review
```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "deep learning medical imaging" \
  --max-results 50 \
  --open-notebook-lm
```

### Case 2: Focus on Recent Publications
```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "immunotherapy cancer" \
  --date-from 2023 \
  --date-to 2024 \
  --max-results 30
```

### Case 3: Batch Download (No Prompting)
```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "CRISPR" \
  --batch \
  --max-results 20 \
  --output-dir ~/research/crispr_2024
```

### Case 4: With NCBI API Key (Faster)
```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --api-key YOUR_NCBI_API_KEY \
  --query "machine learning biology" \
  --max-results 100
```

---

## 🔑 Getting Your NCBI API Key (Optional but Recommended)

1. Visit: https://www.ncbi.nlm.nih.gov/account/
2. Sign in (or create free account)
3. Click "API Key Management"
4. Copy your API key
5. Use with: `--api-key YOUR_KEY`

**Why?** API key increases your request limit from ~3/second to ~10/second (3x faster)

---

## 🎯 Command Reference

### Required Arguments
- `--email your@email.com` - Your email (NCBI requires this)
- `--query "your search"` - What to search for

### Optional Arguments
- `--api-key KEY` - NCBI API key (for faster requests)
- `--max-results N` - How many articles to search for (default: 50)
- `--date-from YYYY` - Start year (e.g., 2023)
- `--date-to YYYY` - End year (e.g., 2024)
- `--output-dir PATH` - Where to save PDFs (default: `./pubmed_downloads`)
- `--batch` - Download all without prompting (auto mode)
- `--open-notebook-lm` - Open Notebook LM in browser when done

### Examples
```bash
# Basic search
python pubmed_notebook_lm.py --email user@example.com --query "cancer"

# Advanced search with filters
python pubmed_notebook_lm.py \
  --email user@example.com \
  --query "immunotherapy AND (melanoma OR leukemia)" \
  --date-from 2022 \
  --date-to 2024 \
  --max-results 100

# Batch mode with custom output
python pubmed_notebook_lm.py \
  --email user@example.com \
  --query "deep learning" \
  --batch \
  --max-results 25 \
  --output-dir ~/my_research
```

---

## 📁 Output Files

After running the script, you'll get:

```
pubmed_downloads/
│
├── PMID_ArticleTitle.pdf          ← Actual PDF files to upload
├── PMID_ArticleTitle.pdf
├── search_metadata.json            ← Search results in JSON format
│                                      (useful for analysis/tracking)
└── NOTEBOOK_LM_INSTRUCTIONS.txt    ← Step-by-step upload guide
```

### Example: search_metadata.json
```json
{
  "search_query": "deep learning medical imaging",
  "search_date": "2024-01-16T10:30:45",
  "total_results": 87,
  "downloaded_pdfs": 12,
  "articles": [
    {
      "pmid": "38123456",
      "title": "Deep Learning Applications...",
      "authors": "Smith J, Johnson M, Williams R",
      "year": "2024",
      "url": "https://pubmed.ncbi.nlm.nih.gov/38123456/"
    }
  ]
}
```

---

## 💡 Tips & Tricks

### Better PubMed Queries
Use boolean operators and field tags for precision:

```bash
# Find papers by a specific author
--query "Smith J[Author] AND cancer"

# Find review articles only
--query "cancer AND (review[PT] OR meta-analysis[PT])"

# Find clinical trials
--query "immunotherapy[Title] AND (clinical trial[PT] OR RCT)"

# Exclude certain topics
--query "machine learning NOT (cryptocurrency OR blockchain)"
```

### Organize Research Projects
```bash
# Create a project folder
mkdir ~/research_2024

# Search multiple topics
python pubmed_notebook_lm.py --email user@example.com \
  --query "topic1" --output-dir ~/research_2024/topic1

python pubmed_notebook_lm.py --email user@example.com \
  --query "topic2" --output-dir ~/research_2024/topic2

# Create separate Notebook LM notebooks for each topic
```

### Use Notebook LM's Features
Once PDFs are uploaded to Notebook LM, you can:
- **Ask Questions**: "What are the main findings?"
- **Create Study Guides**: Automatic Q&A generation
- **Generate FAQs**: Common questions answered
- **Create Podcast Scripts**: Summarized as audio script
- **Export**: Download as PDF, Google Doc, or markdown

### Automate Daily Searches
Add to your crontab (Linux/Mac):
```bash
# Search every day at 9 AM
0 9 * * * python ~/path/pubmed_notebook_lm.py \
  --email user@example.com \
  --query "your topic" \
  --batch \
  --output-dir ~/research_daily/$(date +\%Y-\%m-\%d)
```

---

## ⚠️ Important Limitations

### PDF Availability
- **Only ~25-40% of articles have open-access PDFs** available
- Script downloads from PubMed Central (PMC), which is free
- Paywalled articles require institutional access

**What to do about paywalled papers?**
- Contact the authors (many will send you their paper)
- Use your institution's library access
- Try ResearchGate or author's website
- Look for preprints on bioRxiv or arXiv

### File Size Limits
- Max 500 MB per PDF in Notebook LM
- Very long articles (500+ pages) might be truncated

### Google Notebook LM API
- Currently no public API for automated uploads
- Must upload PDFs manually via browser
- (Google may release API in future)

---

## 🐛 Troubleshooting

### Problem: "No results found"
**Solution**: 
- Check query spelling
- Try simpler/broader terms
- Check date filters aren't too restrictive

### Problem: "Email not provided by NCBI"
**Solution**: 
- Make sure you used `--email your@actual.email`
- Email address must be valid (but doesn't need to be verified)

### Problem: "No PDF found for this article"
**Solution**: 
- Article is not in PubMed Central (PMC)
- Search for full text manually at: pubmed.ncbi.nlm.nih.gov/PMID/
- Try finding preprint version (bioRxiv, arXiv)

### Problem: "Connection timeout"
**Solution**: 
- Reduce `--max-results` to download fewer articles
- Get NCBI API key (`--api-key`) to increase rate limit
- Check your internet connection

### Problem: "Permission denied" when saving files
**Solution**: 
- Check output directory exists and is writable
- Try: `mkdir -p ~/pubmed_downloads`
- Or specify different output: `--output-dir /tmp/pdfs`

---

## 📚 Learn More

### PubMed Advanced Search Syntax
- https://pubmed.ncbi.nlm.nih.gov/help/

### Google Notebook LM
- https://notebooklm.google.com
- Help: https://support.google.com/notebooklm

### Research on Medical Topics
- PubMed Central (free full text): https://www.ncbi.nlm.nih.gov/pmc/
- bioRxiv (preprints): https://www.biorxiv.org/
- arXiv (physics/CS preprints): https://arxiv.org/

---

## ✅ Pre-Flight Checklist

Before running for the first time:

- [ ] Python 3.7+ installed (`python --version`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Valid email address ready
- [ ] Internet connection working
- [ ] Output directory has write permissions
- [ ] Google account for Notebook LM (free)
- [ ] (Optional) NCBI API key obtained

---

## 🎓 Example Workflow: Writing a Literature Review

```bash
# 1. Search for papers
python pubmed_notebook_lm.py \
  --email student@university.edu \
  --query "CRISPR gene therapy clinical trials" \
  --date-from 2020 \
  --max-results 100

# 2. Select ~20 most relevant papers interactively

# 3. Upload to Notebook LM
# → Files saved in pubmed_downloads/

# 4. Go to https://notebooklm.google.com
# → Create notebook "CRISPR Literature Review"
# → Drag PDFs into workspace

# 5. Use Notebook LM features:
# → Ask: "What are the clinical outcomes?"
# → Ask: "What are the main challenges?"
# → Generate: Study guide
# → Generate: FAQ document

# 6. Export the study guide and use in your paper
```

---

## 📞 Support

If you encounter issues:
1. Check the **Troubleshooting** section above
2. Verify your email is correct
3. Try a simpler search query
4. Check internet connection
5. Try with `--api-key` if rate-limited

---

**Version**: 1.0  
**Last Updated**: January 2026  
**License**: MIT (use freely)
