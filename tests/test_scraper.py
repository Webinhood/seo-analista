import pytest
from bs4 import BeautifulSoup
from app.core.scraper import SEOScraper

@pytest.fixture
def scraper():
    return SEOScraper()

@pytest.fixture
def sample_html():
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <header>Header content</header>
            <nav>Navigation</nav>
            <main>
                <h1>Main Title</h1>
                <p>Main content paragraph 1</p>
                <p>Main content paragraph 2</p>
            </main>
            <footer>Footer content</footer>
        </body>
    </html>
    """

@pytest.mark.asyncio
async def test_extract_main_content(scraper, sample_html):
    """Testa a extração do conteúdo principal"""
    content = await scraper.extract_main_content(sample_html)
    assert "Main Title" in content
    assert "Main content paragraph" in content
    assert "Header content" not in content
    assert "Footer content" not in content

@pytest.mark.asyncio
async def test_extract_headings(scraper, sample_html):
    """Testa a extração de headings"""
    headings = await scraper.extract_headings(sample_html)
    assert len(headings) == 1
    assert "H1: Main Title" in headings

@pytest.mark.asyncio
async def test_clean_url_handling():
    """Testa a limpeza de URLs"""
    scraper = SEOScraper()
    urls = await scraper.get_google_results("test keyword", num_results=1)
    assert isinstance(urls, list)
    if urls:  # Se conseguiu obter resultados
        assert all(isinstance(url, str) for url in urls)
        assert all(url.startswith(('http://', 'https://')) for url in urls)

@pytest.mark.asyncio
async def test_error_handling_invalid_url(scraper):
    """Testa o tratamento de erros para URLs inválidas"""
    result = await scraper.get_page_content("https://invalid-url-that-does-not-exist.com")
    assert result is None

@pytest.mark.asyncio
async def test_empty_html_handling(scraper):
    """Testa o tratamento de HTML vazio"""
    content = await scraper.extract_main_content("")
    assert content == ""
    
    headings = await scraper.extract_headings("")
    assert headings == []
