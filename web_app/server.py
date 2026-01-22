#!/usr/bin/env python3
"""
Flask backend API for PubMed Search Web App
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import sys
import os
import subprocess
import json
import csv
import zipfile
import io
import urllib.request
import urllib.error
import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Path to the PubMed script
SCRIPT_DIR = Path(__file__).parent.parent
PUBMED_SCRIPT = SCRIPT_DIR / "pubmed_notebook_lm.py"
WEB_DIR = Path(__file__).parent

@app.route('/api/search', methods=['POST'])
def search_pubmed():
    """Handle PubMed search requests"""
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('email') or not data.get('query'):
            return jsonify({'error': 'Email and query are required'}), 400
        
        # Build command - ALWAYS use batch mode for web interface
        cmd = [
            'python3',
            str(PUBMED_SCRIPT),
            '--email', data['email'],
            '--query', data['query'],
            '--max-results', str(data.get('maxResults', 50)),
            '--output-dir', str(SCRIPT_DIR / 'pubmed_downloads'),
            '--batch'  # Always use batch mode for web
        ]
        
        if data.get('apiKey'):
            cmd.extend(['--api-key', data['apiKey']])
        
        if data.get('dateFrom'):
            cmd.extend(['--date-from', data['dateFrom']])
        
        if data.get('dateTo'):
            cmd.extend(['--date-to', data['dateTo']])
        
        # Run the command
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180  # 3 minute timeout (PubMed API is faster: ~0.4 sec per article)
        )
        
        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout[:500]}")
        print(f"STDERR: {result.stderr[:500]}")
        
        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else "Unknown error"
            return jsonify({'error': f'Search failed: {error_msg}'}), 500
        
        # Find the most recent CSV file
        downloads_dir = SCRIPT_DIR / 'pubmed_downloads'
        csv_files = list(downloads_dir.glob('pubmed_results_*.csv'))
        
        if not csv_files:
            return jsonify({'error': 'No results file generated'}), 500
        
        # Get the most recent CSV
        latest_csv = max(csv_files, key=lambda p: p.stat().st_mtime)
        
        # Read CSV and convert to JSON
        results = []
        with open(latest_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            results = list(reader)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Search timeout (>5 minutes). Try reducing max results or disable citation fetching.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'script_exists': PUBMED_SCRIPT.exists()
    })

@app.route('/api/download-pdfs', methods=['POST'])
def download_pdfs():
    """Download PDFs for selected articles as a zip file"""
    try:
        data = request.json
        selected_articles = data.get('articles', [])
        query = data.get('query', 'pubmed_search')
        
        if not selected_articles:
            return jsonify({'error': 'No articles selected'}), 400
        
        # Try to create a text file with links instead of actual PDFs
        # This is because PMC requires JavaScript to get actual PDFs
        zip_buffer = io.BytesIO()
        download_info = {'success': [], 'failed': [], 'restricted': [], 'links': []}
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Create a manifest file with all article links
            manifest_lines = [
                "# PubMed Article Download Links\n",
                f"# Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                f"# Query: {query}\n",
                f"# Total articles: {len(selected_articles)}\n",
                "\n",
                "## Instructions:\n",
                "This file contains links to PubMed articles. Most articles are behind paywalls.\n",
                "- Open Access articles: Click link to access free full-text PDF\n",
                "- Restricted articles: Available through your institution or by purchase\n",
                "\n",
                "---\n\n"
            ]
            
            for idx, article in enumerate(selected_articles, 1):
                pmid = article.get('PMID', 'unknown')
                pmc_id = article.get('PMC_ID', 'N/A')
                title = article.get('Title', 'Untitled')
                doi = article.get('DOI', 'N/A')
                doi_link = article.get('DOI_Link', 'N/A')
                pdf_link = article.get('PDF_Link', 'N/A')
                pubmed_url = article.get('PubMed_URL', '')
                
                # Build article info
                article_info = f"{idx}. {title}\n"
                article_info += f"   PMID: {pmid}\n"
                if pmc_id and pmc_id != 'N/A':
                    article_info += f"   PMC ID: {pmc_id}\n"
                    article_info += f"   PMC Link: https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/\n"
                if doi and doi != 'N/A':
                    article_info += f"   DOI: {doi}\n"
                if pubmed_url:
                    article_info += f"   PubMed: {pubmed_url}\n"
                article_info += "\n"
                
                manifest_lines.append(article_info)
                download_info['links'].append({
                    'pmid': pmid,
                    'pmc_id': pmc_id,
                    'has_pmc': pmc_id != 'N/A' and pmc_id
                })
            
            # Add the manifest file to zip
            manifest_content = ''.join(manifest_lines)
            zip_file.writestr('ARTICLE_LINKS.txt', manifest_content)
        
        # Return zip with link manifest
        zip_buffer.seek(0)
        sanitized_query = query.replace(' ', '_').replace('/', '_')[:40]
        zip_filename = f"pubmed_articles_{sanitized_query}.zip"
        
        print(f"✓ Created zip with links for {len(selected_articles)} articles")
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_filename
        )
        
    except Exception as e:
        print(f"ERROR in download_pdfs: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)[:100]}'}), 500

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (JS, CSS, etc.)"""
    return send_from_directory(WEB_DIR, path)

if __name__ == '__main__':
    print("="*80)
    print("PubMed Search Web App")
    print("="*80)
    print(f"Script location: {PUBMED_SCRIPT}")
    print(f"")
    print(f"🌐 Open in browser: http://localhost:5000")
    print(f"")
    print("="*80)
    
    app.run(debug=True, port=5000, host='127.0.0.1')
