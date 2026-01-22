#!/usr/bin/env python3
"""
PubMed Search & CSV Export Script

This script allows you to:
1. Search PubMed using keywords
2. Filter and select results
3. Export results to CSV with PMID, Title, Authors, Journal, Year, DOI, and links

Requirements:
    pip install biopython requests
"""

import os
import json
import csv
import argparse
import logging
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
import webbrowser
import re
import time

# Third-party imports
from Bio import Entrez
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# PUBMED SEARCH MODULE
# ============================================================================

class PubMedSearcher:
    """Interface for searching PubMed and retrieving metadata."""
    
    def __init__(self, email: str, api_key: Optional[str] = None):
        """
        Initialize PubMed searcher.
        
        Args:
            email: Required by NCBI Entrez for polite access
            api_key: Optional NCBI API key for faster requests
                    Get one at https://www.ncbi.nlm.nih.gov/account/
        """
        self.email = email
        Entrez.email = email
        if api_key:
            Entrez.api_key = api_key
        
        # Setup robust HTTP session for PDF downloads
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update({
            'User-Agent': 'PubMedSearch/1.0 (gzip)'
        })
    
    def search(self, query: str, max_results: int = 50, 
               date_from: Optional[str] = None,
               date_to: Optional[str] = None) -> List[Dict]:
        """
        Search PubMed for articles.
        
        Args:
            query: Search query (e.g., "cancer treatment 2023")
            max_results: Maximum number of results to fetch
            date_from: YYYY/MM/DD or YYYY (optional filter)
            date_to: YYYY/MM/DD or YYYY (optional filter)
        
        Returns:
            List of article dictionaries with PMID, title, abstract, authors, year
        """
        try:
            # Build date filter
            date_filter = ""
            if date_from or date_to:
                if date_from and date_to:
                    date_filter = f" AND ({date_from}:{date_to}[PDAT])"
                elif date_from:
                    date_filter = f" AND ({date_from}[PDAT] : 3000[PDAT])"
                elif date_to:
                    date_filter = f" AND (0001[PDAT] : {date_to}[PDAT])"
            
            full_query = query + date_filter
            
            logger.info(f"Searching PubMed with query: {full_query}")
            
            # Step 1: Get PMIDs
            search_handle = Entrez.esearch(
                db="pubmed",
                term=full_query,
                retmax=max_results,
                sort="relevance"
            )
            search_results = Entrez.read(search_handle)
            search_handle.close()
            
            pmids = search_results.get("IdList", [])
            total_count = int(search_results.get("Count", 0))
            
            logger.info(f"Found {total_count} results; fetching {len(pmids)} records")
            
            if not pmids:
                logger.warning("No results found")
                return []
            
            # Step 2: Fetch full records
            fetch_handle = Entrez.efetch(
                db="pubmed",
                id=",".join(pmids),
                rettype="xml"
            )
            records = Entrez.read(fetch_handle)
            fetch_handle.close()
            
            # Step 3: Parse records
            articles = []
            for record in records["PubmedArticle"]:
                try:
                    medline = record["MedlineCitation"]
                    article = medline["Article"]
                    
                    pmid = medline["PMID"]
                    title = article.get("ArticleTitle", "N/A")
                    
                    # Extract abstract
                    abstract = ""
                    if "Abstract" in article:
                        abstract_text = article["Abstract"].get("AbstractText", [])
                        if isinstance(abstract_text, list):
                            abstract = " ".join(str(t) for t in abstract_text)
                        else:
                            abstract = str(abstract_text)
                    
                    # Extract authors
                    authors = []
                    if "AuthorList" in article:
                        for author in article["AuthorList"]:
                            last_name = author.get("LastName", "")
                            initials = author.get("Initials", "")
                            if last_name:
                                authors.append(f"{last_name} {initials}".strip())
                    
                    # Extract publication year
                    year = "N/A"
                    if "ArticleDate" in article and article["ArticleDate"]:
                        year = article["ArticleDate"][0].get("Year", "N/A")
                    elif "PubDate" in article:
                        pub_date = article["PubDate"]
                        if "Year" in pub_date:
                            year = pub_date["Year"]
                        elif "MedlineDate" in pub_date:
                            # Extract year from MedlineDate (e.g., "2023 Jan-Feb")
                            medline_date = pub_date["MedlineDate"]
                            import re
                            year_match = re.search(r'\d{4}', str(medline_date))
                            if year_match:
                                year = year_match.group()
                    
                    # Extract journal name
                    journal = "N/A"
                    if "Journal" in article:
                        journal_info = article["Journal"]
                        if "Title" in journal_info:
                            journal = journal_info["Title"]
                        elif "ISOAbbreviation" in journal_info:
                            journal = journal_info["ISOAbbreviation"]
                    
                    # Extract DOI
                    doi = "N/A"
                    doi_link = "N/A"
                    if "ELocationID" in article:
                        for elocation in article["ELocationID"]:
                            if elocation.attributes.get("EIdType") == "doi":
                                doi = str(elocation)
                                doi_link = f"https://doi.org/{doi}"
                                break
                    
                    # If DOI not in article, check PubmedData
                    pmc_id = "N/A"
                    if "PubmedData" in record:
                        article_ids = record["PubmedData"].get("ArticleIdList", [])
                        for article_id in article_ids:
                            id_type = article_id.attributes.get("IdType")
                            if id_type == "doi" and doi == "N/A":
                                doi = str(article_id)
                                doi_link = f"https://doi.org/{doi}"
                            elif id_type == "pmc":
                                pmc_id = str(article_id)
                    
                    # Fetch citation count from PubMed Central
                    citation_count = self.get_citation_count(str(pmid))
                    
                    # Generate PMC PDF link
                    pdf_link = self.get_pmc_pdf_link(str(pmid), pmc_id)
                    
                    articles.append({
                        "pmid": str(pmid),
                        "pmc_id": pmc_id if pmc_id != "N/A" else "N/A",
                        "title": title,
                        "abstract": abstract[:500] + "..." if len(abstract) > 500 else abstract,
                        "authors": ", ".join(authors[:3]),  # First 3 authors
                        "year": year,
                        "journal": journal,
                        "doi": doi,
                        "doi_link": doi_link,
                        "pdf_link": pdf_link,
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        "citation_count": citation_count if citation_count is not None else "N/A"
                    })
                
                except Exception as e:
                    logger.warning(f"Error parsing record: {e}")
                    continue
            
            return articles
        
        except Exception as e:
            logger.error(f"PubMed search failed: {e}")
            raise

    def get_pmc_pdf_link(self, pmid: str, pmc_id: str) -> str:
        """
        Generate PubMed Central Open Access PDF download link.
        
        PMC provides Open Access PDFs through multiple formats:
        1. Direct PDF: https://www.ncbi.nlm.nih.gov/pmc/articles/{PMC_ID}/pdf/
        2. Alternative format: https://www.ncbi.nlm.nih.gov/pmc/articles/{PMC_ID}/?report=reader
        
        Note: Only Open Access articles are available via these links.
        
        Args:
            pmid: PubMed ID of the article
            pmc_id: PubMed Central ID (e.g., "PMC7057201")
        
        Returns:
            Direct PMC PDF download URL, or link to PMC article page if PDF unavailable
        """
        if not pmc_id or pmc_id == "N/A":
            return "N/A"
        
        # Try the direct PDF link format first
        # This works for Open Access articles
        pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/"
        
        return pdf_url
    
    def get_citation_count(self, pmid: str) -> Optional[int]:
        """
        Fetch citation count from NCBI PubMed Central using elink.
        
        This uses the official NCBI E-utilities API which is free and reliable.
        
        Args:
            pmid: PubMed ID of the article
        
        Returns:
            Citation count as integer, or None if not found
        """
        try:
            # Add a small delay to be respectful to NCBI
            time.sleep(0.4)  # NCBI allows 3 requests/sec without API key, 10/sec with key
            
            # Use elink to find articles that cite this PMID
            handle = Entrez.elink(
                dbfrom="pubmed",
                db="pubmed",
                id=pmid,
                linkname="pubmed_pubmed_citedin"  # Articles that cite this one
            )
            
            result = Entrez.read(handle)
            handle.close()
            
            # Extract citation count
            if result and len(result) > 0:
                link_set_db = result[0].get('LinkSetDb', [])
                if link_set_db and len(link_set_db) > 0:
                    cited_pmids = link_set_db[0].get('Link', [])
                    citation_count = len(cited_pmids)
                    logger.info(f"Found {citation_count} citations for PMID {pmid}")
                    return citation_count
            
            logger.debug(f"No citations found for PMID {pmid}")
            return 0
                
        except Exception as e:
            logger.warning(f"Error fetching citation count for PMID {pmid}: {e}")
            return None

    def get_full_text_url(self, pmid: str, article: Optional[Dict] = None) -> Dict[str, Optional[str]]:
            return None

    def get_full_text_url(self, pmid: str, article: Optional[Dict] = None) -> Dict[str, Optional[str]]:
        """
        Attempt to find full-text PDF URL from multiple sources.
        
        Tries in order:
        1. PubMed Central (free, open-access)
        2. bioRxiv/medRxiv (preprints, free)
        3. arXiv (preprints, free)
        4. ResearchGate (may have author-uploaded copies)
        5. PubMed Central alternate formats
        
        Args:
            pmid: PubMed ID
            article: Optional article dict with title/authors for alternative searches
        
        Returns:
            Dict with keys: 'url', 'source', 'access_type'
            Example: {'url': 'https://...', 'source': 'PMC', 'access_type': 'open-access'}
        """
        result = {
            'url': None,
            'source': None,
            'access_type': None
        }
        
        try:
            # 1. Check PubMed Central (most reliable)
            pmc_url = self._try_pmc(pmid)
            if pmc_url:
                result['url'] = pmc_url
                result['source'] = 'PubMed Central'
                result['access_type'] = 'open-access'
                return result
            
            # 2. Try preprint servers (bioRxiv, medRxiv)
            if article:
                preprint_url = self._try_preprints(pmid, article.get('title', ''))
                if preprint_url:
                    result['url'] = preprint_url
                    result['source'] = 'bioRxiv/medRxiv'
                    result['access_type'] = 'open-access'
                    return result
            
            # 3. Try arXiv for computational/AI papers
            if article:
                arxiv_url = self._try_arxiv(article.get('title', ''))
                if arxiv_url:
                    result['url'] = arxiv_url
                    result['source'] = 'arXiv'
                    result['access_type'] = 'open-access'
                    return result
            
            # 4. Try ResearchGate API
            if article:
                rg_url = self._try_researchgate(article.get('title', ''), article.get('authors', ''))
                if rg_url:
                    result['url'] = rg_url
                    result['source'] = 'ResearchGate'
                    result['access_type'] = 'possibly-paywalled'
                    return result
            
            return result
        
        except Exception as e:
            logger.debug(f"Error searching for PDFs for {pmid}: {e}")
            return result

    def _try_pmc(self, pmid: str) -> Optional[str]:
        """Try PubMed Central for open-access PDF"""
        try:
            search_handle = Entrez.esearch(
                db="pmc",
                term=pmid,
                retmax=1
            )
            search_results = Entrez.read(search_handle)
            search_handle.close()
            
            pmc_ids = search_results.get("IdList", [])
            if pmc_ids:
                pmc_id = pmc_ids[0]
                pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
                
                # Verify URL is accessible
                try:
                    response = self.session.head(pdf_url, timeout=5)
                    if response.status_code == 200:
                        logger.debug(f"Found PDF on PubMed Central for {pmid}")
                        return pdf_url
                except:
                    pass
            
            return None
        except Exception as e:
            logger.debug(f"PMC search failed for {pmid}: {e}")
            return None

    def _try_preprints(self, pmid: str, title: str) -> Optional[str]:
        """Try bioRxiv and medRxiv for preprints"""
        try:
            # Search bioRxiv API
            search_title = title.split(':')[0][:100]  # First 100 chars, before colon
            
            for server in ['biorxiv', 'medrxiv']:
                try:
                    url = f"https://api.biorxiv.org/details/{server}/{search_title}"
                    response = self.session.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if 'collection' in data and len(data['collection']) > 0:
                            preprint = data['collection'][0]
                            pdf_url = preprint.get('pdf', '')
                            if pdf_url and not pdf_url.startswith('http'):
                                pdf_url = f"https://biorxiv.org{pdf_url}"
                            
                            if pdf_url:
                                logger.debug(f"Found preprint for {pmid} on {server}")
                                return pdf_url
                except:
                    pass
            
            return None
        except Exception as e:
            logger.debug(f"Preprint search failed for {pmid}: {e}")
            return None

    def _try_arxiv(self, title: str) -> Optional[str]:
        """Try arXiv for computational/AI papers"""
        try:
            import urllib.parse
            
            search_title = title.split(':')[0][:100]
            query = urllib.parse.quote(search_title)
            
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=1"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                # Parse XML response
                if '<entry>' in response.text:
                    # Extract PDF URL from arXiv entry
                    import re
                    pdf_match = re.search(r'pdf>(.*?)<', response.text)
                    if pdf_match:
                        arxiv_id = pdf_match.group(1).split('/')[-1]
                        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                        logger.debug(f"Found preprint on arXiv: {arxiv_id}")
                        return pdf_url
            
            return None
        except Exception as e:
            logger.debug(f"arXiv search failed: {e}")
            return None

    def _try_researchgate(self, title: str, authors: str) -> Optional[str]:
        """Try to find paper on ResearchGate"""
        try:
            import urllib.parse
            
            search_title = title.split(':')[0][:100]
            # ResearchGate doesn't have public API, but we can suggest the search URL
            # Return the ResearchGate search URL so user can check
            rg_search = f"https://www.researchgate.net/search?q={urllib.parse.quote(search_title)}"
            
            # Try to check if page exists (optional)
            try:
                response = self.session.head(rg_search, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    logger.debug(f"ResearchGate search URL available for {title[:50]}")
                    return rg_search
            except:
                pass
            
            return None
        except Exception as e:
            logger.debug(f"ResearchGate search failed: {e}")
            return None

    def download_pdf(self, url: str, output_path: str) -> bool:
        """
        Download PDF from URL.
        
        Args:
            url: PDF URL
            output_path: Where to save the PDF
        
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            return False


# ============================================================================
# NOTEBOOK LM MODULE
# ============================================================================

class NotebookLMManager:
    """Interface for creating/managing Google Notebook LM workspaces."""
    
    def __init__(self):
        """Initialize Notebook LM manager."""
        self.notebook_lm_url = "https://notebooklm.google.com"
    
    def open_notebook_lm(self):
        """Open Notebook LM in default browser."""
        logger.info("Opening Notebook LM in browser...")
        webbrowser.open(self.notebook_lm_url)
    
    def create_upload_instructions(self, pdf_files: List[str]) -> str:
        """
        Generate manual upload instructions for PDFs.
        
        Note: Google Notebook LM API is not publicly available yet.
        This provides step-by-step instructions for manual upload.
        
        Args:
            pdf_files: List of PDF file paths
        
        Returns:
            Formatted instruction string
        """
        instructions = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    NOTEBOOK LM - UPLOAD INSTRUCTIONS                       ║
╚════════════════════════════════════════════════════════════════════════════╝

{len(pdf_files)} PDF(s) ready for upload. Follow these steps:

STEP 1: Open Notebook LM
   → Go to: {self.notebook_lm_url}
   → Sign in with your Google account

STEP 2: Create a New Notebook (if needed)
   → Click "+ Create new notebook"
   → Enter a title (e.g., "PubMed Research - {datetime.now().strftime('%Y-%m-%d')}")
   → Click "Create"

STEP 3: Upload Documents
   → Click "Upload" or drag-and-drop PDFs into the workspace
   → Select all {len(pdf_files)} PDF files from: {pdf_files[0] if pdf_files else "N/A"}
   
   Files to upload:
"""
        for i, pdf_file in enumerate(pdf_files, 1):
            file_size = os.path.getsize(pdf_file) / (1024 * 1024)  # Size in MB
            instructions += f"   {i}. {Path(pdf_file).name} ({file_size:.1f} MB)\n"
        
        instructions += f"""
STEP 4: Generate Insights (Optional)
   → Once documents are processed, use "Ask NotebookLM" to:
      • Summarize findings
      • Create study guides
      • Generate FAQs
      • Create podcast scripts

STEP 5: Export & Share
   → Use the share button to collaborate with others
   → Export study guides, FAQs, or podcasts as needed

═══════════════════════════════════════════════════════════════════════════════

TROUBLESHOOTING:
• File too large? Notebook LM supports PDFs up to 500 MB each
• Upload fails? Try uploading files one at a time
• PDFs encrypted? Notebook LM requires unencrypted PDFs
• API access? Google Notebook LM API is not yet publicly available;
  automated upload coming in future versions

═══════════════════════════════════════════════════════════════════════════════
"""
        return instructions


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def interactive_selection(articles: List[Dict]) -> List[str]:
    """
    Present search results and allow user to select articles.
    
    Args:
        articles: List of article dictionaries
    
    Returns:
        List of selected PMIDs
    """
    print("\n" + "="*80)
    print(f"Found {len(articles)} articles. Review and select which to download:\n")
    
    for i, article in enumerate(articles, 1):
        print(f"[{i}] {article['title'][:70]}...")
        print(f"    Authors: {article['authors']}")
        print(f"    Year: {article['year']} | PMID: {article['pmid']}")
        print(f"    {article['abstract'][:100]}...")
        print()
    
    print("Enter article numbers to download (e.g., '1 3 5' or '1-5'), or 'all': ", end="")
    selection = input().strip().lower()
    
    selected_indices = []
    if selection == 'all':
        selected_indices = list(range(len(articles)))
    else:
        # Parse ranges and individual numbers
        parts = selection.replace('-', ' ').split()
        for part in parts:
            if part.isdigit():
                idx = int(part) - 1
                if 0 <= idx < len(articles):
                    selected_indices.append(idx)
    
    selected_pmids = [articles[i]['pmid'] for i in selected_indices]
    print(f"\n✓ Selected {len(selected_pmids)} articles\n")
    return selected_pmids


def main():
    """Main script execution."""
    parser = argparse.ArgumentParser(
        description="Search PubMed and export results to CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive search with default email
  python pubmed_notebook_lm.py --email user@example.com --query "CRISPR gene therapy"
  
  # Search with date filter and API key
  python pubmed_notebook_lm.py --email user@example.com --api-key YOUR_KEY \\
      --query "machine learning COVID-19" --max-results 100 \\
      --date-from 2023 --date-to 2024
  
  # Batch mode (non-interactive) - export first 10 results
  python pubmed_notebook_lm.py --email user@example.com \\
      --query "immunotherapy melanoma" --max-results 10 --batch
        """
    )
    
    parser.add_argument('--email', required=True,
                        help='Your email (required by NCBI for polite access)')
    parser.add_argument('--api-key', default=None,
                        help='NCBI API key (optional; get at https://www.ncbi.nlm.nih.gov/account/)')
    parser.add_argument('--query', required=True,
                        help='PubMed search query')
    parser.add_argument('--max-results', type=int, default=50,
                        help='Maximum results to fetch (default: 50)')
    parser.add_argument('--date-from', default=None,
                        help='Filter by publication date (YYYY or YYYY/MM/DD)')
    parser.add_argument('--date-to', default=None,
                        help='Filter by publication date (YYYY or YYYY/MM/DD)')
    parser.add_argument('--output-dir', default='./pubmed_downloads',
                        help='Output directory for CSV file (default: ./pubmed_downloads)')
    parser.add_argument('--batch', action='store_true',
                        help='Non-interactive mode: export all results without prompting')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir}")
    
    try:
        # Initialize searcher
        searcher = PubMedSearcher(email=args.email, api_key=args.api_key)
        
        # Search PubMed
        articles = searcher.search(
            query=args.query,
            max_results=args.max_results,
            date_from=args.date_from,
            date_to=args.date_to
        )
        
        if not articles:
            logger.warning("No articles found. Try a different query.")
            return
        
        # Select articles to download
        if args.batch:
            selected_pmids = [a['pmid'] for a in articles]
        else:
            selected_pmids = interactive_selection(articles)
        
        if not selected_pmids:
            logger.warning("No articles selected.")
            return
        
        # Export to CSV
        selected_articles = [a for a in articles if a['pmid'] in selected_pmids]
        
        logger.info(f"\nExporting {len(selected_articles)} articles to CSV...")
        
        # Create CSV filename with query keywords and date
        # Sanitize query for filename (remove special chars, limit length)
        import re
        sanitized_query = re.sub(r'[^\w\s-]', '', args.query)  # Remove special chars
        sanitized_query = re.sub(r'\s+', '_', sanitized_query)  # Replace spaces with underscores
        sanitized_query = sanitized_query[:50]  # Limit to 50 characters
        
        timestamp = datetime.now().strftime("%Y%m%d")
        csv_filename = f"pubmed_results_{sanitized_query}_{timestamp}.csv"
        csv_filepath = output_dir / csv_filename
        
        # Write to CSV
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['PMID', 'PMC_ID', 'Title', 'Citation_Count', 'Authors', 'Journal', 'Year', 'DOI', 'DOI_Link', 'PDF_Link', 'PubMed_URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for article in selected_articles:
                writer.writerow({
                    'PMID': article['pmid'],
                    'PMC_ID': article.get('pmc_id', 'N/A'),
                    'Title': article['title'],
                    'Citation_Count': article.get('citation_count', 'N/A'),
                    'Authors': article['authors'],
                    'Journal': article['journal'],
                    'Year': article['year'],
                    'DOI': article['doi'],
                    'DOI_Link': article['doi_link'],
                    'PDF_Link': article.get('pdf_link', 'N/A'),
                    'PubMed_URL': article['url']
                })
        
        logger.info(f"✓ CSV file created: {csv_filepath}")
        
        # Save metadata
        metadata = {
            "search_query": args.query,
            "search_date": datetime.now().isoformat(),
            "total_results": len(articles),
            "exported_articles": len(selected_articles),
            "csv_file": str(csv_filename),
            "articles": selected_articles
        }
        
        metadata_file = output_dir / "search_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved to: {metadata_file}")
        
        # Summary
        print(f"\n{'='*80}")
        print(f"SUMMARY")
        print(f"{'='*80}")
        print(f"Exported articles: {len(selected_articles)}")
        print(f"CSV file: {csv_filepath}")
        print(f"Output directory: {output_dir}")
        print(f"Metadata file: {metadata_file}")
        print()
        print(f"CSV contains: PMID, Title, Authors, Journal, Year, DOI, DOI_Link, PubMed_URL")
        print()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
