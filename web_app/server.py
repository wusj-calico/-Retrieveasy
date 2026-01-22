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
        selected_pmids = data.get('pmids', [])
        selected_articles = data.get('articles', [])
        query = data.get('query', 'pubmed_search')
        
        if not selected_articles:
            return jsonify({'error': 'No articles selected'}), 400
        
        # Create in-memory zip file
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            downloaded_count = 0
            failed_count = 0
            
            for article in selected_articles:
                pdf_link = article.get('PDF_Link', 'N/A')
                pmid = article.get('PMID', 'unknown')
                title = article.get('Title', f'Article_{pmid}')
                
                # Skip if no PDF link available
                if pdf_link == 'N/A' or not pdf_link:
                    failed_count += 1
                    continue
                
                try:
                    # Download the PDF
                    pdf_filename = f"{pmid}_{title[:50].replace('/', '_').replace(' ', '_')}.pdf"
                    pdf_data = urllib.request.urlopen(pdf_link, timeout=10).read()
                    
                    # Add to zip file
                    zip_file.writestr(pdf_filename, pdf_data)
                    downloaded_count += 1
                    
                except Exception as e:
                    print(f"Failed to download PDF for PMID {pmid}: {e}")
                    failed_count += 1
                    continue
        
        # Prepare response
        zip_buffer.seek(0)
        sanitized_query = query.replace(' ', '_').replace('/', '_')[:50]
        zip_filename = f"pubmed_pdfs_{sanitized_query}.zip"
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_filename
        )
        
    except Exception as e:
        return jsonify({'error': f'Failed to create PDF zip: {str(e)}'}), 500

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
