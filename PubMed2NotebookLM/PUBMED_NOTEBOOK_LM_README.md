# PubMed to Notebook LM Integration Guide

## Overview

This Python script enables you to:
1. **Search PubMed** with keywords and date filters
2. **Filter & select** results interactively
3. **Download PDFs** of open-access articles from PubMed Central (PMC)
4. **Prepare documents** for Google Notebook LM
5. **Generate upload instructions** for Notebook LM

## Features

- ✅ PubMed API integration (via Biopython/Entrez)
- ✅ Interactive article selection
- ✅ Automatic PDF downloading from open-access sources
- ✅ Batch mode for automation
- ✅ Metadata tracking (JSON export)
- ✅ Error handling & retry logic
- ✅ Step-by-step Notebook LM upload instructions

## Installation

### 1. Install Python Dependencies

```bash
pip install biopython requests
```

### 2. (Optional) Get NCBI API Key

For faster requests, get a free API key:
1. Go to: https://www.ncbi.nlm.nih.gov/account/
2. Sign in or create a free account
3. Copy your API key
4. Use it with `--api-key` parameter

## Usage

### Basic Usage - Interactive Mode

```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "cancer immunotherapy"
```

This will:
1. Search PubMed for "cancer immunotherapy"
2. Display first 50 results
3. Prompt you to select which articles to download
4. Download available PDFs to `./pubmed_downloads/`
5. Generate Notebook LM upload instructions

### Advanced Usage Examples

#### Search with date filter and API key

```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --api-key YOUR_NCBI_API_KEY \
  --query "CRISPR gene therapy" \
  --max-results 100 \
  --date-from 2023 \
  --date-to 2024
```

#### Batch mode - automatically download all results

```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "machine learning COVID-19" \
  --max-results 20 \
  --batch
```

#### Custom output directory and open Notebook LM

```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "immunotherapy melanoma" \
  --output-dir ~/my_research_pdfs \
  --open-notebook-lm
```

## Command-Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--email` | ✓ | Your email (required by NCBI for polite access) |
| `--query` | ✓ | PubMed search query |
| `--api-key` | | NCBI API key (optional; makes requests faster) |
| `--max-results` | | Max results to fetch (default: 50) |
| `--date-from` | | Filter by date: YYYY or YYYY/MM/DD |
| `--date-to` | | Filter by date: YYYY or YYYY/MM/DD |
| `--output-dir` | | Where to save PDFs (default: `./pubmed_downloads`) |
| `--batch` | | Non-interactive; download all results without prompting |
| `--open-notebook-lm` | | Open Notebook LM in browser after downloading |

## Workflow

### Step 1: Search & Select Articles

```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "deep learning medical imaging 2024"
```

**Output:**
```
Found 87 articles. Review and select which to download:

[1] Deep Learning Applications in Medical Image Analysis: A Review
    Authors: Smith J, Johnson M, Williams R
    Year: 2024 | PMID: 38123456
    Medical image analysis has been rapidly evolving with deep learning...

[2] Neural Networks for Pathology Image Classification
    Authors: Brown A, Davis B, Miller C
    Year: 2024 | PMID: 38123457
    ...

Enter article numbers to download (e.g., '1 3 5' or '1-5'), or 'all':
```

**Select articles:** `1 2 3 5` (or `1-5` for range, or `all`)

### Step 2: PDFs Download

```
Attempting to download 4 PDFs...
[*] Downloading PMID: 38123456...
    ✓ Downloaded: pubmed_downloads/38123456_Deep_Learning_Applications.pdf
[*] Downloading PMID: 38123457...
    ✓ Downloaded: pubmed_downloads/38123457_Neural_Networks_for.pdf
...
```

### Step 3: Upload to Notebook LM

The script generates detailed instructions:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                    NOTEBOOK LM - UPLOAD INSTRUCTIONS                       ║
╚════════════════════════════════════════════════════════════════════════════╝

2 PDF(s) ready for upload. Follow these steps:

STEP 1: Open Notebook LM
   → Go to: https://notebooklm.google.com
   → Sign in with your Google account

STEP 2: Create a New Notebook (if needed)
   → Click "+ Create new notebook"
   → Enter a title (e.g., "PubMed Research - 2024-01-16")
   → Click "Create"

STEP 3: Upload Documents
   → Click "Upload" or drag-and-drop PDFs into the workspace
   → Select files from: pubmed_downloads/
   
   Files to upload:
   1. 38123456_Deep_Learning_Applications.pdf (5.2 MB)
   2. 38123457_Neural_Networks_for.pdf (3.8 MB)

STEP 4: Generate Insights (Optional)
   → Once documents are processed, use "Ask NotebookLM" to:
      • Summarize findings
      • Create study guides
      • Generate FAQs
      • Create podcast scripts

STEP 5: Export & Share
   → Use the share button to collaborate with others
   → Export study guides, FAQs, or podcasts as needed
```

## Important Notes

### PDF Availability
- **Open-Access Only**: The script downloads PDFs only from PubMed Central (PMC), which contains freely available articles
- **Limited Coverage**: Many articles require institutional access or purchase
- **Success Rate**: Typically 20-40% of articles are available as open-access PDFs
- **Workaround**: You can manually add PDFs to Notebook LM if you have institutional access

### Google Notebook LM API
- **Current Status**: Google Notebook LM does not yet have a public API
- **Manual Upload Required**: PDFs must be uploaded manually to Notebook LM
- **Future**: Google may release an API for programmatic uploads

### Google Notebook LM Limits
- Maximum file size: 500 MB per PDF
- Supported formats: PDF, Google Docs, Google Slides
- Maximum documents per notebook: Varies (typically 200+)
- Processing time: Usually a few minutes per document

## Output Files

After running the script, you'll find:

```
pubmed_downloads/
├── PMID_Title.pdf           # Downloaded PDF files
├── PMID_Title.pdf
├── search_metadata.json     # Search results & metadata
└── NOTEBOOK_LM_INSTRUCTIONS.txt  # Detailed upload guide
```

### Metadata File Example
```json
{
  "search_query": "deep learning medical imaging",
  "search_date": "2024-01-16T10:30:45.123456",
  "total_results": 87,
  "downloaded_pdfs": 2,
  "articles": [
    {
      "pmid": "38123456",
      "title": "Deep Learning Applications in Medical Image Analysis",
      "abstract": "Recent advances in deep learning...",
      "authors": "Smith J, Johnson M, Williams R",
      "year": "2024",
      "url": "https://pubmed.ncbi.nlm.nih.gov/38123456/"
    },
    ...
  ]
}
```

## Tips & Best Practices

### 1. Refine Your Search Query
Use PubMed search syntax for better results:
```bash
# Boolean operators
--query "CRISPR AND (cancer OR leukemia)"

# Date ranges
--query "immunotherapy" --date-from 2023 --date-to 2024

# Specific fields
--query "Smith J[Author] AND machine learning"
```

### 2. Batch Download for Analysis
```bash
# Download 10 most recent articles
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "your research topic" \
  --max-results 10 \
  --batch \
  --output-dir ~/research_project_2024
```

### 3. Organize Multiple Searches
Create a separate notebook for each topic:
```bash
# First notebook
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "topic 1" \
  --output-dir ./research/topic1

# Second notebook
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "topic 2" \
  --output-dir ./research/topic2
```

### 4. Use NCBI API Key
Set up an API key for significantly faster requests:
```bash
python pubmed_notebook_lm.py \
  --email your.email@example.com \
  --api-key YOUR_KEY \
  --query "your query" \
  --max-results 100
```

## Troubleshooting

### Issue: "No PDF found for article"
- **Cause**: Article is not available in PubMed Central (PMC)
- **Solution**: 
  - Check if the full text is available via: https://pubmed.ncbi.nlm.nih.gov/PMID/
  - Look for "Free full text" or "PMC" link
  - Try searching for preprints (arXiv, bioRxiv)

### Issue: "Connection timeout / Too many requests"
- **Cause**: Rate limiting or network issues
- **Solution**: 
  - Reduce `--max-results`
  - Add delays between requests
  - Use `--api-key` (increases rate limit)

### Issue: Notebook LM says "PDF is encrypted"
- **Cause**: PDF has restrictions
- **Solution**: Try manually downloading and removing encryption, or find alternative source

### Issue: "Email not provided by NCBI"
- **Cause**: Entrez requires a valid email
- **Solution**: Ensure `--email` is a real email address

## Advanced: Scripting & Automation

### Python Script Integration

```python
from pubmed_notebook_lm import PubMedSearcher, NotebookLMManager

# Search
searcher = PubMedSearcher(email="your.email@example.com")
articles = searcher.search("machine learning", max_results=50)

# Filter articles by year
recent_articles = [a for a in articles if int(a['year']) >= 2023]

# Attempt to download
for article in recent_articles[:5]:
    pdf_url = searcher.get_full_text_url(article['pmid'])
    if pdf_url:
        searcher.download_pdf(pdf_url, f"pdf/{article['pmid']}.pdf")

# Generate Notebook LM instructions
mgr = NotebookLMManager()
mgr.open_notebook_lm()
```

### Schedule Periodic Searches

```bash
# Add to crontab for daily search (runs every day at 9 AM)
0 9 * * * python /path/to/pubmed_notebook_lm.py \
  --email your.email@example.com \
  --query "your topic" \
  --batch \
  --output-dir ~/research_daily
```

## FAQ

**Q: Can I download paywalled articles?**  
A: No, this script only downloads open-access PDFs from PubMed Central. For paywalled articles, you'll need institutional access or to contact authors.

**Q: Can I upload more than just PDFs to Notebook LM?**  
A: Yes! Notebook LM also accepts Google Docs and Google Slides directly.

**Q: Does the script work on Windows/Mac/Linux?**  
A: Yes! Python is cross-platform. The script works on all three.

**Q: Can I use this without a Google account?**  
A: You need a Google account to use Google Notebook LM, but the script itself doesn't require one.

**Q: How do I cite the articles I find?**  
A: Export the `search_metadata.json` file and use the PMIDs/PubMed URLs for proper citation.

## License & Attribution

This script uses:
- **Biopython**: Free/open-source
- **NCBI Entrez**: Public service (free with email)
- **PubMed Central**: Free open-access full-text articles
- **Google Notebook LM**: Requires Google account (free tier available)

## Support & Future Improvements

### Potential Enhancements
- [ ] Automatic PDF text extraction & summarization
- [ ] Integration with Zotero/Mendeley for citation management
- [ ] Google Sheets export for article metadata
- [ ] Notebook LM API integration (when available)
- [ ] Support for other preprint servers (arXiv, bioRxiv)
- [ ] Docker containerization

### Report Issues
If you encounter problems, check:
1. NCBI email is valid and not blocked
2. Internet connection is stable
3. Output directory has write permissions
4. PDFs are not encrypted

---

**Last Updated**: January 2026  
**Version**: 1.0
