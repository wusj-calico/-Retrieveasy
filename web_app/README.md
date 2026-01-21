# PubMed Search Web App

Modern Vue.js web interface for PubMed literature search with CSV export.

## Features

- 🔍 **Intuitive Search Interface** - Clean, modern design following Google Material guidelines
- 🎨 **Green Theme (#30BC5B)** - Professional medical research aesthetic
- 📊 **Real-time Results** - View search results in an interactive table
- 💾 **CSV Export** - Download results directly from the browser
- 🎯 **Advanced Filters** - Date ranges, batch mode, and API key support
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices

## Quick Start

### 1. Install Dependencies

```bash
# Install Flask and CORS support
pip install flask flask-cors
```

### 2. Start the Backend Server

```bash
cd web_app
python3 server.py
```

The API server will start on `http://localhost:5000`

### 3. Open the Web Interface

Simply open `index.html` in your web browser:

```bash
# macOS
open index.html

# Or just double-click the file
```

## How It Works

### Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌──────────────────┐
│   Browser UI    │  HTTP   │  Flask API      │  Shell  │ PubMed Script    │
│   (Vue.js)      │ ◄─────► │  (server.py)    │ ◄─────► │ (Python)         │
│   index.html    │         │  Port 5000      │         │ NCBI Entrez API  │
└─────────────────┘         └─────────────────┘         └──────────────────┘
```

1. **Frontend** (index.html + app.js)
   - Vue.js 3 application
   - Material Design UI components
   - Handles form validation and CSV export

2. **Backend** (server.py)
   - Flask REST API
   - Calls the Python PubMed script
   - Converts CSV results to JSON

3. **Core Script** (pubmed_notebook_lm.py)
   - Connects to NCBI PubMed API
   - Fetches article metadata
   - Generates CSV files

## Usage

### Basic Search

1. Enter your email address (required by NCBI)
2. Enter search query (e.g., "CRISPR gene therapy")
3. Click "Search PubMed"
4. View results in the table
5. Click "Download CSV" to export

### Advanced Options

Click "Advanced Options" to access:

- **Date Range** - Filter by publication date (YYYY or YYYY/MM/DD)
- **NCBI API Key** - For faster rate limits (get one at ncbi.nlm.nih.gov/account)
- **Batch Mode** - Export all results without manual selection

## API Endpoints

### POST /api/search

Search PubMed and return results.

**Request Body:**
```json
{
  "email": "user@example.com",
  "query": "CRISPR gene therapy",
  "maxResults": 50,
  "apiKey": "optional_api_key",
  "dateFrom": "2023",
  "dateTo": "2024",
  "batchMode": true
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "PMID": "12345678",
      "Title": "Article title",
      "Authors": "Smith J, Doe A",
      "Journal": "Nature",
      "Year": "2024",
      "DOI": "10.1234/example",
      "DOI_Link": "https://doi.org/10.1234/example",
      "PubMed_URL": "https://pubmed.ncbi.nlm.nih.gov/12345678/"
    }
  ],
  "count": 50
}
```

### GET /api/health

Check if the API server is running.

**Response:**
```json
{
  "status": "healthy",
  "script_exists": true
}
```

## Features in Detail

### 🎨 Design System

- **Primary Color**: #30BC5B (Medical Green)
- **Typography**: Roboto font family
- **Spacing**: 8px base grid system
- **Shadows**: Material Design elevation levels
- **Animations**: Smooth transitions and loading states

### 📱 Responsive Layout

- Desktop: 1200px max-width with two-column forms
- Tablet: Single column layout with full-width buttons
- Mobile: Optimized touch targets and scrolling

### 💾 Local Storage

- Email address is saved automatically
- Reduces repetitive data entry

### ⚡ Performance

- Lazy loading of results table
- Efficient CSV generation in browser
- 2-minute timeout for searches

## Troubleshooting

### Backend won't start

```bash
# Install missing dependencies
pip install flask flask-cors
```

### CORS errors

- Make sure server.py is running on port 5000
- Check that CORS is enabled in server.py

### No results returned

- Check your internet connection
- Verify email format is valid
- Try simpler search queries
- Check server.py console for errors

### CSV download not working

- Check browser download permissions
- Try a different browser
- Check console for JavaScript errors

## File Structure

```
web_app/
├── index.html          # Main HTML interface
├── app.js              # Vue.js application logic
├── server.py           # Flask API server
└── README.md           # This file
```

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Development

### Running in Development Mode

The Flask server runs with `debug=True` by default, enabling:
- Auto-reload on code changes
- Detailed error messages
- Debug toolbar

### Customization

**Change the color theme:**

Edit the CSS in `index.html`:
```css
/* Primary color */
--primary: #30BC5B;

/* Gradient background */
background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
```

**Modify search parameters:**

Edit default values in `app.js`:
```javascript
formData: {
    maxResults: 50,  // Change default max results
    batchMode: true  // Toggle batch mode default
}
```

## Security Notes

⚠️ **This is a development server.** For production:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Add authentication/authorization
3. Implement rate limiting
4. Use environment variables for configuration
5. Enable HTTPS

## License

Same as parent project.

## Credits

- Built with Vue.js 3
- Flask REST API
- Material Design Icons
- Roboto Font Family
