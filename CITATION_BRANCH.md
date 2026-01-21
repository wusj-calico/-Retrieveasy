# Citation Feature Branch

This branch focuses on displaying citation counts for research articles in Retrieveasy.

## Branch Name
`citation`

## Objectives

This branch will implement features to display how many times each article has been cited by other literature:

### Citation Count Features to Support
- [ ] Fetch citation count from PubMed Central or Google Scholar API
- [ ] Display citation count in results table
- [ ] Sort articles by citation count (highest to lowest)
- [ ] Filter by minimum citation count threshold
- [ ] Show citation statistics for selected articles
- [ ] Include citation count in CSV export

### Features to Implement

1. **Citation Count Retrieval**
   - Query PubMed Central or Google Scholar API for citation counts
   - Cache results to avoid repeated API calls
   - Handle articles with zero citations gracefully
   - Implement timeout handling for slow API responses

2. **Citation Count Display**
   - Show citation count as badge in results table (e.g., "Cited by: 245")
   - Add visual indicator with color coding for impact level
   - Highlight highly-cited articles (50+, 100+, 500+ citations)
   - Show citation count in article details

3. **Sorting and Filtering**
   - Add "Citation Count" as sortable column in results table
   - Filter articles by minimum citation threshold
   - Sort from most to least cited
   - Calculate and display total citations for selected articles

4. **Statistics and Analytics**
   - Show average citation count of selected articles
   - Identify impact metrics in selection
   - Display citation trends
   - Export citation statistics with results

5. **Integration with Current Features**
   - Integrate with existing checkbox selection system
   - Include citation_count in CSV export as new column
   - Maintain compatibility with existing search and sort features
   - Display citation data in article preview

### Technical Implementation

**Backend (server.py)**
- Add citation count fetching using PubMed Central eutils API
- Implement caching mechanism to reduce API calls
- Handle API rate limiting and timeouts gracefully
- Return citation_count field in search results

**PubMed Script (pubmed_notebook_lm.py)**
- Add method to fetch citation counts from PubMed Central
- Implement Google Scholar scraping as fallback (with rate limiting)
- Cache citation data locally with timestamps
- Update PubMedSearcher class to include citation retrieval

**Frontend (index.html & app.js)**
- Add citation_count column to results table
- Make citation_count a sortable column with visual sorting indicators
- Add color-coded badges (green for 100+, yellow for 50+, gray for <50)
- Show total and average citations for selected articles
- Add citation impact filter controls

### Example Use Case

User searches for "CRISPR gene therapy":
1. Results display with "Cited by: 245" badge next to each article
2. User sorts by citation count (highest first) by clicking column header
3. User filters to show only articles with 50+ citations
4. Selects top 5 most-cited articles
5. CSV export includes citation_count column
6. Stats show: "Selected articles: 5 | Total citations: 1,250 | Average: 250"

### Example Output Format

```
Title: Gene therapy applications
Authors: Smith J, et al.
Year: 2025
Cited by: 245
DOI: 10.xxxx/xxxxx

Title: CRISPR mechanisms  
Authors: Johnson K, et al.
Year: 2024
Cited by: 487
DOI: 10.xxxx/xxxxx

Title: Clinical outcomes
Authors: Williams M, et al.
Year: 2025
Cited by: 156
DOI: 10.xxxx/xxxxx
```

### Data Structure Updates

Article objects will include:
- PMID
- Title
- Authors
- Journal
- Year
- DOI
- **citation_count** (new) - integer, total times article has been cited
- **citation_source** (optional) - string, source of citation data (PMC, Scholar)

## Development Progress

- [ ] Research PubMed Central API for citation count endpoints
- [ ] Implement citation count retrieval in pubmed_notebook_lm.py
- [ ] Add caching mechanism for citation data
- [ ] Update Flask API to return citation counts
- [ ] Add citation_count column to results table
- [ ] Implement sortable citation count column (with ▲/▼ indicators)
- [ ] Add citation count color-coding badge display
- [ ] Create citation statistics for selected articles display
- [ ] Add citation count filter/threshold controls
- [ ] Update CSV export to include citation_count field
- [ ] Test with various PubMed searches
- [ ] Test sorting and filtering functionality
- [ ] Merge back to main branch

## Related Issues

None yet - this is a new feature branch.

## How to Contribute

1. Make changes on this branch
2. Test citation exports
3. Submit pull request to `main` with details
4. Require review before merging

## Notes

- Keep CSV export functionality intact
- Don't break existing features
- Test with real PubMed data
- Consider edge cases (missing authors, special characters)
