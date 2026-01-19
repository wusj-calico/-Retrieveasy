#!/usr/bin/env python3
"""
Advanced Integration Examples

This file shows how to integrate the PubMed script into your own workflows
"""

# ============================================================================
# EXAMPLE 1: Use as a Python Library (Not CLI)
# ============================================================================

def example_library_usage():
    """Show how to use the script as a Python library"""
    
    from pubmed_notebook_lm import PubMedSearcher, NotebookLMManager
    from pathlib import Path
    
    # Initialize searcher
    searcher = PubMedSearcher(
        email="your.email@example.com",
        api_key="YOUR_API_KEY"  # Optional
    )
    
    # Search PubMed
    articles = searcher.search(
        query="immunotherapy AND cancer",
        max_results=50,
        date_from="2023",
        date_to="2024"
    )
    
    # Filter articles by criteria
    recent_articles = [a for a in articles if int(a['year']) >= 2023]
    high_impact = [a for a in articles if 'cancer' in a['title'].lower()]
    
    # Download PDFs
    output_dir = Path("./my_research_pdfs")
    output_dir.mkdir(exist_ok=True)
    
    downloaded = []
    for article in recent_articles[:10]:  # First 10
        pdf_url = searcher.get_full_text_url(article['pmid'])
        if pdf_url:
            filename = f"{article['pmid']}_{article['title'][:40]}.pdf"
            filepath = output_dir / filename
            if searcher.download_pdf(pdf_url, str(filepath)):
                downloaded.append(str(filepath))
    
    print(f"Downloaded {len(downloaded)} PDFs")
    
    # Open Notebook LM
    manager = NotebookLMManager()
    manager.open_notebook_lm()


# ============================================================================
# EXAMPLE 2: Batch Processing Multiple Topics
# ============================================================================

def example_batch_topics():
    """Search multiple topics and organize by folder"""
    
    from pubmed_notebook_lm import PubMedSearcher
    from pathlib import Path
    import json
    
    topics = {
        "immunotherapy": "immunotherapy cancer treatment 2024",
        "gene_therapy": "gene therapy CRISPR clinical trials",
        "ai_medicine": "deep learning artificial intelligence medicine",
    }
    
    searcher = PubMedSearcher(email="your.email@example.com")
    results = {}
    
    for topic_name, query in topics.items():
        print(f"Searching: {topic_name}...")
        
        articles = searcher.search(query, max_results=30)
        topic_dir = Path(f"./research/{topic_name}")
        topic_dir.mkdir(parents=True, exist_ok=True)
        
        # Download PDFs
        for article in articles[:5]:
            pdf_url = searcher.get_full_text_url(article['pmid'])
            if pdf_url:
                filename = f"{article['pmid']}.pdf"
                searcher.download_pdf(pdf_url, str(topic_dir / filename))
        
        # Save metadata
        with open(topic_dir / "metadata.json", 'w') as f:
            json.dump(articles, f, indent=2)
        
        results[topic_name] = {
            "total_found": len(articles),
            "folder": str(topic_dir)
        }
        
        print(f"  ✓ Downloaded PDFs to {topic_dir}")
    
    return results


# ============================================================================
# EXAMPLE 3: Automatic Filtering by Criteria
# ============================================================================

def example_smart_filtering():
    """Download only high-quality recent papers"""
    
    from pubmed_notebook_lm import PubMedSearcher
    import json
    
    searcher = PubMedSearcher(email="your.email@example.com")
    
    # Search broadly
    articles = searcher.search(
        "machine learning biology",
        max_results=100,
        date_from="2022"
    )
    
    # Filter criteria
    high_quality = []
    for article in articles:
        # Criteria:
        # 1. Recent (2024)
        # 2. Has multiple authors (likely well-resourced)
        # 3. Contains methodology keywords
        
        is_recent = int(article['year']) >= 2024
        has_team = len(article['authors'].split(',')) >= 2
        is_methods = any(kw in article['title'].lower() 
                        for kw in ['deep learning', 'neural', 'framework'])
        
        if is_recent and has_team and is_methods:
            high_quality.append(article)
    
    print(f"Filtered to {len(high_quality)} high-quality articles")
    
    # Download top 10
    for article in high_quality[:10]:
        pdf_url = searcher.get_full_text_url(article['pmid'])
        if pdf_url:
            print(f"  ✓ {article['title']}")


# ============================================================================
# EXAMPLE 4: Citation Analysis with Downloaded PDFs
# ============================================================================

def example_citation_export():
    """Export search results in various citation formats"""
    
    from pubmed_notebook_lm import PubMedSearcher
    
    searcher = PubMedSearcher(email="your.email@example.com")
    articles = searcher.search("CRISPR", max_results=20)
    
    # BibTeX format (for LaTeX/Overleaf)
    bibtex = []
    for article in articles:
        authors = article['authors'].replace(', ', ' and ')
        bibtex.append(f"""@article{{PMID{article['pmid']},
  title={{{article['title']}}},
  author={{{authors}}},
  year={{{article['year']}}},
  url={{{article['url']}}}
}}""")
    
    with open("citations.bib", 'w') as f:
        f.write('\n'.join(bibtex))
    
    print("✓ Saved as BibTeX: citations.bib")
    
    # CSV format
    import csv
    with open("articles.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=articles[0].keys())
        writer.writeheader()
        writer.writerows(articles)
    
    print("✓ Saved as CSV: articles.csv")


# ============================================================================
# EXAMPLE 5: Scheduled Daily Searches
# ============================================================================

def example_scheduled_search():
    """Set up a periodic search (for scheduling with APScheduler)"""
    
    from pubmed_notebook_lm import PubMedSearcher
    from pathlib import Path
    from datetime import datetime
    import json
    
    def run_daily_search(topic, query):
        """Function to run as scheduled task"""
        
        searcher = PubMedSearcher(email="your.email@example.com")
        
        # Create date-based folder
        today = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path(f"./research/daily/{topic}/{today}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Search and download
        articles = searcher.search(query, max_results=50)
        
        for article in articles[:5]:
            pdf_url = searcher.get_full_text_url(article['pmid'])
            if pdf_url:
                filename = f"{article['pmid']}.pdf"
                searcher.download_pdf(pdf_url, str(output_dir / filename))
        
        # Save metadata
        with open(output_dir / "articles.json", 'w') as f:
            json.dump(articles, f, indent=2)
        
        print(f"✓ Daily search completed: {output_dir}")
        return output_dir
    
    # To use with APScheduler:
    # from apscheduler.schedulers.background import BackgroundScheduler
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(run_daily_search, 'cron', hour=9, 
    #                   args=("cancer", "immunotherapy cancer"))
    # scheduler.start()


# ============================================================================
# EXAMPLE 6: Integration with Pandas for Analysis
# ============================================================================

def example_pandas_analysis():
    """Analyze search results with Pandas"""
    
    from pubmed_notebook_lm import PubMedSearcher
    import pandas as pd
    
    searcher = PubMedSearcher(email="your.email@example.com")
    articles = searcher.search("deep learning", max_results=100)
    
    # Convert to DataFrame
    df = pd.DataFrame(articles)
    
    # Analysis
    print("Publication by year:")
    print(df['year'].value_counts().sort_index(ascending=False))
    
    print("\nMost common authors:")
    all_authors = ' '.join(df['authors']).split(', ')
    author_counts = pd.Series(all_authors).value_counts().head(10)
    print(author_counts)
    
    # Find papers with specific keywords
    df['has_neural'] = df['title'].str.contains('neural', case=False, na=False)
    df['has_learning'] = df['title'].str.contains('learning', case=False, na=False)
    
    print(f"\nPapers with 'neural': {df['has_neural'].sum()}")
    print(f"Papers with 'learning': {df['has_learning'].sum()}")
    
    # Export analysis
    df.to_csv('analysis_results.csv', index=False)
    print("\n✓ Saved analysis to: analysis_results.csv")


# ============================================================================
# EXAMPLE 7: Custom HTML Report Generation
# ============================================================================

def example_html_report():
    """Generate a beautiful HTML report from search results"""
    
    from pubmed_notebook_lm import PubMedSearcher
    from datetime import datetime
    
    searcher = PubMedSearcher(email="your.email@example.com")
    articles = searcher.search("immunotherapy", max_results=20)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>PubMed Search Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .article {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .title {{ font-size: 18px; font-weight: bold; color: #0066cc; }}
        .authors {{ color: #666; font-size: 14px; }}
        .metadata {{ color: #999; font-size: 12px; }}
        .pmid {{ background: #f0f0f0; padding: 5px; border-radius: 3px; font-family: monospace; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f9f9f9; padding: 10px; border-left: 3px solid #0066cc; }}
    </style>
</head>
<body>
    <h1>PubMed Search Report</h1>
    <div class="summary">
        <p><strong>Search Query:</strong> immunotherapy</p>
        <p><strong>Results Found:</strong> {len(articles)}</p>
        <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h2>Articles</h2>
"""
    
    for i, article in enumerate(articles, 1):
        html += f"""
    <div class="article">
        <div class="title">{i}. {article['title']}</div>
        <div class="authors">by {article['authors']}</div>
        <div class="metadata">
            Year: {article['year']} | 
            <span class="pmid">PMID: {article['pmid']}</span>
        </div>
        <p>{article['abstract']}</p>
        <a href="{article['url']}" target="_blank">View on PubMed</a>
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    with open('pubmed_report.html', 'w') as f:
        f.write(html)
    
    print("✓ Report saved to: pubmed_report.html")


# ============================================================================
# MAIN: Run Examples
# ============================================================================

if __name__ == "__main__":
    print("Advanced Integration Examples for PubMed → Notebook LM\n")
    print("These are code examples you can adapt for your needs.\n")
    print("Uncomment the example(s) you want to run below:\n")
    
    # Uncomment any example to run:
    # example_library_usage()
    # example_batch_topics()
    # example_smart_filtering()
    # example_citation_export()
    # example_scheduled_search()
    # example_pandas_analysis()
    # example_html_report()
    
    print("""
    ✓ Copy & adapt any of these examples for your workflow!
    
    Examples included:
    1. Use as Python library (import and use in your code)
    2. Batch process multiple topics
    3. Smart filtering (download only high-quality papers)
    4. Citation export (BibTeX, CSV)
    5. Scheduled daily searches
    6. Pandas analysis and statistics
    7. HTML report generation
    """)
