# SEO Content Analysis Tool

This tool automates SEO content analysis by scraping Google search results and extracting content from web pages.

## Features

- Google search results scraping
- Full content extraction from top 3 results
- Heading extraction from remaining 7 results
- Content conversion to Markdown format
- FastAPI-based REST API

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd seo
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the API server:
```bash
uvicorn app.main:app --reload
```

2. Make a request to analyze content:
```bash
curl -X POST "http://localhost:8000/scrape-content" \
     -H "Content-Type: application/json" \
     -d '{"keyword": "your search keyword"}'
```

## API Endpoints

- `POST /scrape-content`: Main endpoint for content analysis
  - Input: `{"keyword": "search term"}`
  - Output: JSON containing analyzed content and headings
- `GET /status`: Health check endpoint

## Configuration

Create a `.env` file in the project root with the following variables:
```
GOOGLE_API_KEY=your_api_key  # Optional
REDIS_URL=redis://localhost:6379  # If using Celery
```

## Error Handling

The API includes comprehensive error handling for:
- Failed web requests
- Blocked scraping attempts
- Invalid input
- Server errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License
