#!/usr/bin/env python3
"""
Quick-Start Example: PubMed to CSV Export
Usage: python example_usage.py
"""

from pathlib import Path
import sys

# Example search scenarios
EXAMPLES = {
    "1": {
        "name": "Cancer Research",
        "query": "immunotherapy cancer treatment 2024",
        "max_results": 25
    },
    "2": {
        "name": "CRISPR Gene Therapy",
        "query": "CRISPR gene editing clinical trials",
        "max_results": 20
    },
    "3": {
        "name": "AI in Healthcare",
        "query": "deep learning medical imaging diagnosis",
        "max_results": 30
    },
    "4": {
        "name": "COVID-19 Research",
        "query": "COVID-19 vaccine efficacy variants",
        "max_results": 25
    },
    "5": {
        "name": "Alzheimer's Disease",
        "query": "Alzheimer disease amyloid tau treatment",
        "max_results": 20
    },
    "6": {
        "name": "Custom Search",
        "query": None,
        "max_results": None
    }
}

def main():
    print("="*80)
    print("PubMed to CSV Export - Quick Start Example")
    print("="*80)
    print()
    
    # Check if script is installed
    if not Path("pubmed_notebook_lm.py").exists():
        print("❌ Error: pubmed_notebook_lm.py not found in current directory")
        print("   Please run from the directory containing pubmed_notebook_lm.py")
        sys.exit(1)
    
    # Display examples
    print("SELECT A RESEARCH TOPIC:\n")
    for key, example in EXAMPLES.items():
        print(f"  [{key}] {example['name']}")
        if example['query']:
            print(f"      Query: {example['query']}")
        print()
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice not in EXAMPLES:
        print("❌ Invalid choice")
        sys.exit(1)
    
    example = EXAMPLES[choice]
    
    # Get email
    email = input("\nEnter your email (required by NCBI): ").strip()
    if not email or "@" not in email:
        print("❌ Invalid email")
        sys.exit(1)
    
    # Get custom query if needed
    if choice == "6":
        query = input("Enter your search query: ").strip()
        max_results = input("Max results to fetch (default 50): ").strip()
        max_results = int(max_results) if max_results.isdigit() else 50
    else:
        query = example['query']
        max_results = example['max_results']
    
    # Get API key (optional)
    api_key = input("\n(Optional) Enter NCBI API key for faster requests, or press Enter to skip: ").strip()
    api_key_arg = f"--api-key {api_key}" if api_key else ""
    
    # Ask about batch mode
    batch_mode = input("\nExport all results automatically? (y/n, default: n): ").strip().lower()
    batch_arg = "--batch" if batch_mode == "y" else ""
    
    # Build and display command
    print()
    print("="*80)
    print("RUNNING COMMAND:")
    print("="*80)
    
    cmd = f"""python3 pubmed_notebook_lm.py \\
    --email "{email}" \\
    --query "{query}" \\
    --max-results {max_results} \\
    {api_key_arg} \\
    {batch_arg}
""".strip()
    
    print(cmd)
    print()
    
    # Execute
    import subprocess
    result = subprocess.run(cmd, shell=True)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
