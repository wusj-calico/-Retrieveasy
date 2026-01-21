const { createApp } = Vue;

createApp({
    data() {
        return {
            formData: {
                email: '',
                query: '',
                maxResults: 50,
                apiKey: '',
                dateFrom: '',
                dateTo: ''
            },
            results: [],
            isLoading: false,
            alertMessage: '',
            alertType: 'info',
            showAdvanced: false,
            sortColumn: null,
            sortDirection: 'asc',
            selectedArticles: []
        };
    },
    computed: {
        sortedResults() {
            if (!this.sortColumn) {
                return this.results;
            }

            const sorted = [...this.results].sort((a, b) => {
                let aVal = a[this.sortColumn];
                let bVal = b[this.sortColumn];

                // Handle numeric sorting for PMID, Year, and Citation_Count
                if (this.sortColumn === 'PMID' || this.sortColumn === 'Year' || this.sortColumn === 'Citation_Count') {
                    aVal = parseInt(aVal) || 0;
                    bVal = parseInt(bVal) || 0;
                } else {
                    // String sorting
                    aVal = String(aVal).toLowerCase();
                    bVal = String(bVal).toLowerCase();
                }

                if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1;
                if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1;
                return 0;
            });

            return sorted;
        }
    },
    methods: {
        getCitationColor(count) {
            // Color code citations based on impact
            if (count >= 100) return '#2e7d32'; // Dark green for high impact
            if (count >= 50) return '#66bb6a';  // Medium green
            if (count >= 10) return '#a5d6a7';  // Light green
            return '#e0e0e0';  // Gray for low citations
        },
        sortBy(column) {
            // If clicking the same column, toggle direction
            if (this.sortColumn === column) {
                this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                // New column, sort ascending
                this.sortColumn = column;
                this.sortDirection = 'asc';
            }
        },
        toggleArticleSelection(pmid) {
            const index = this.selectedArticles.indexOf(pmid);
            if (index > -1) {
                // Already selected, remove it
                this.selectedArticles.splice(index, 1);
            } else {
                // Not selected, add it
                this.selectedArticles.push(pmid);
            }
        },
        toggleSelectAll() {
            if (this.selectedArticles.length === this.results.length) {
                // All selected, deselect all
                this.selectedArticles = [];
            } else {
                // Not all selected, select all
                this.selectedArticles = this.results.map(article => article.PMID);
            }
        },
        async searchPubMed() {
            this.isLoading = true;
            this.alertMessage = 'Searching PubMed (this may take 30-60 seconds)...';
            this.alertType = 'info';
            this.results = [];

            try {
                // Build command arguments
                const args = [
                    '--email', this.formData.email,
                    '--query', this.formData.query,
                    '--max-results', this.formData.maxResults.toString()
                ];

                if (this.formData.apiKey) {
                    args.push('--api-key', this.formData.apiKey);
                }

                if (this.formData.dateFrom) {
                    args.push('--date-from', this.formData.dateFrom);
                }

                if (this.formData.dateTo) {
                    args.push('--date-to', this.formData.dateTo);
                }

                if (this.formData.batchMode) {
                    args.push('--batch');
                }

                // Call Python script via backend API
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.formData.email,
                        query: this.formData.query,
                        maxResults: this.formData.maxResults,
                        apiKey: this.formData.apiKey,
                        dateFrom: this.formData.dateFrom,
                        dateTo: this.formData.dateTo,
                        batchMode: this.formData.batchMode
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    this.results = data.results;
                    this.alertType = 'success';
                    this.alertMessage = `Successfully found ${data.results.length} articles!`;
                } else {
                    throw new Error(data.error || 'Search failed');
                }

            } catch (error) {
                this.alertType = 'error';
                this.alertMessage = `Error: ${error.message}`;
                console.error('Search error:', error);
            } finally {
                this.isLoading = false;
            }
        },

        exportToCSV() {
            if (this.selectedArticles.length === 0) {
                this.alertType = 'error';
                this.alertMessage = 'Please select at least one article to export';
                return;
            }

            // Filter results to only include selected articles
            const selectedResults = this.results.filter(article => 
                this.selectedArticles.includes(article.PMID)
            );

            // Create CSV content
            const headers = ['PMID', 'Title', 'Citation_Count', 'Authors', 'Journal', 'Year', 'DOI', 'DOI_Link', 'PubMed_URL'];
            const csvRows = [headers.join(',')];

            selectedResults.forEach(article => {
                const row = [
                    article.PMID,
                    `"${article.Title.replace(/"/g, '""')}"`, // Escape quotes
                    article.Citation_Count || 'N/A',
                    `"${article.Authors.replace(/"/g, '""')}"`,
                    `"${article.Journal.replace(/"/g, '""')}"`,
                    article.Year,
                    article.DOI,
                    article.DOI_Link,
                    article.PubMed_URL
                ];
                csvRows.push(row.join(','));
            });

            const csvContent = csvRows.join('\n');

            // Create download
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            
            // Generate filename
            const sanitizedQuery = this.formData.query
                .replace(/[^\w\s-]/g, '')
                .replace(/\s+/g, '_')
                .substring(0, 50);
            const date = new Date().toISOString().split('T')[0].replace(/-/g, '');
            const filename = `pubmed_results_${sanitizedQuery}_${date}.csv`;

            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            this.alertType = 'success';
            this.alertMessage = `CSV file "${filename}" with ${this.selectedArticles.length} articles downloaded successfully!`;
        },

        resetForm() {
            this.formData = {
                email: '',
                query: '',
                maxResults: 50,
                apiKey: '',
                dateFrom: '',
                dateTo: ''
            };
            this.results = [];
            this.selectedArticles = [];
            this.alertMessage = '';
            this.showAdvanced = false;
        }
    },

    mounted() {
        // Load saved email from localStorage
        const savedEmail = localStorage.getItem('pubmed_email');
        if (savedEmail) {
            this.formData.email = savedEmail;
        }

        // Auto-dismiss alerts after 5 seconds
        this.$watch('alertMessage', (newVal) => {
            if (newVal) {
                setTimeout(() => {
                    this.alertMessage = '';
                }, 5000);
            }
        });

        // Save email to localStorage when changed
        this.$watch('formData.email', (newVal) => {
            if (newVal && newVal.includes('@')) {
                localStorage.setItem('pubmed_email', newVal);
            }
        });
    }
}).mount('#app');
