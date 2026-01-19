# PubMed to CSV Export - Usage Guide

## Overview

The script now exports PubMed search results to a **CSV file** instead of downloading PDFs. The CSV includes all key metadata for easy analysis in Excel, R, Python, or other tools.

## CSV Columns

Each row contains:
- **PMID** - PubMed unique identifier
- **Title** - Article title
- **Authors** - First 3 authors (Last Name + Initials)
- **Journal** - Journal name
- **Year** - Publication year
- **DOI** - Digital Object Identifier
- **DOI_Link** - Direct link to DOI (https://doi.org/...)
- **PubMed_URL** - Direct link to PubMed page

## Usage

### Basic Search (Interactive Mode)

```bash
python3 pubmed_notebook_lm.py \
    --email your.email@example.com \
    --query "your search terms here"
```

This will:
1. Search PubMed
2. Show you the results
3. Let you select which ones to export
4. Create a CSV file

### Batch Mode (Export All Results)

```bash
python3 pubmed_notebook_lm.py \
    --email your.email@example.com \
    --query "Secretory carrier membrane associated protein" \
    --max-results 50 \
    --batch
```

The `--batch` flag exports all results without prompting for selection.

### Advanced: Date Filtering

```bash
python3 pubmed_notebook_lm.py \
    --email your.email@example.com \
    --query "CRISPR gene therapy" \
    --date-from 2023 \
    --date-to 2024 \
    --max-results 100
```

### Advanced: Custom Output Directory

```bash
python3 pubmed_notebook_lm.py \
    --email your.email@example.com \
    --query "machine learning" \
    --output-dir ./my_research_results
```

## Output Files

After running, you'll get:

1. **CSV file** - `pubmed_results_YYYYMMDD_HHMMSS.csv`
   - Contains all article metadata
   - Ready to open in Excel or import into R/Python

2. **Metadata JSON** - `search_metadata.json`
   - Search query used
   - Timestamp
   - Number of results
   - Full article data in JSON format

## Example Output

```
================================================================================
SUMMARY
================================================================================
Exported articles: 15
CSV file: pubmed_downloads/pubmed_results_20260116_213615.csv
Output directory: pubmed_downloads
Metadata file: pubmed_downloads/search_metadata.json

CSV contains: PMID, Title, Authors, Journal, Year, DOI, DOI_Link, PubMed_URL
```

## Opening the CSV

### In Excel / Google Sheets
1. Open Excel/Sheets
2. File → Open → Select the CSV file
3. Data will be automatically formatted into columns

### In Python (pandas)
```python
import pandas as pd

# Read the CSV
df = pd.read_csv('pubmed_downloads/pubmed_results_20260116_213615.csv')

# View first few rows
print(df.head())

# Filter by year
recent = df[df['Year'].astype(str) >= '2020']

# Count by journal
journal_counts = df['Journal'].value_counts()
```

### In R
```r
# Read the CSV
data <- read.csv('pubmed_downloads/pubmed_results_20260116_213615.csv')

# View structure
str(data)

# Filter by year
recent <- subset(data, Year >= 2020)

# Summary statistics
summary(data)
```

## Tips

1. **Use specific search terms** to get relevant results
2. **Limit max-results** for faster searches (default is 50)
3. **Use batch mode** for automated workflows
4. **Date filtering** helps narrow down to recent publications
5. **DOI links** provide direct access to full papers (if you have access)

## Troubleshooting

### No results found
- Check your search query spelling
- Try broader search terms
- Remove date filters

### Some years show "N/A"
- Some older articles may not have complete metadata
- This is normal for certain publication types

### SSL certificate errors
```bash
pip install certifi
```

### Module not found errors
```bash
pip install -r requirements.txt
```

## Next Steps

After exporting to CSV, you can:
- Import into citation managers (Zotero, Mendeley)
- Analyze trends over time
- Filter by journal or year
- Use DOI links to access full papers
- Create visualizations of publication patterns
- Export to other formats for further analysis

---

**Modified**: January 2026
**Script**: `pubmed_notebook_lm.py`
