import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.core.processor import ContentProcessor

@pytest.fixture
def processor():
    return ContentProcessor()

@pytest.fixture
def mock_scraper():
    with patch('app.core.processor.SEOScraper') as mock:
        instance = mock.return_value
        # Mock para get_google_results
        instance.get_google_results.return_value = [
            "http://test1.com",
            "http://test2.com",
            "http://test3.com",
            "http://test4.com"
        ]
        # Mock para get_page_content
        instance.get_page_content.return_value = "<html><body><h1>Test</h1><p>Content</p></body></html>"
        # Mock para extract_main_content
        instance.extract_main_content.return_value = "Test Content"
        # Mock para extract_headings
        instance.extract_headings.return_value = ["H1: Test Title"]
        yield instance

@pytest.mark.asyncio
async def test_process_keyword(processor, mock_scraper):
    """Testa o processamento completo de uma keyword"""
    results = await processor.process_keyword("test")
    
    assert "top3_content" in results
    assert "remaining_headings" in results
    assert len(results["top3_content"]) <= 3
    assert isinstance(results["remaining_headings"], dict)

@pytest.mark.asyncio
async def test_error_handling():
    """Testa o tratamento de erros no processamento"""
    with patch('app.core.processor.SEOScraper') as mock:
        # Configura o mock
        instance = mock.return_value
        instance.get_google_results = AsyncMock(side_effect=Exception("Test error"))
        instance.close = AsyncMock()
        
        processor = ContentProcessor()
        with pytest.raises(Exception) as exc_info:
            await processor.process_keyword("test")
        
        assert "Erro ao processar keyword" in str(exc_info.value)
        await instance.close()

def test_format_markdown(processor):
    """Testa a formatação para markdown"""
    html = "<h1>Test</h1><p>This is a <b>test</b></p>"
    markdown = processor.format_markdown(html)
    
    # Verifica se o conteúdo está presente, independente do formato exato
    assert "Test" in markdown
    assert "This is a **test**" in markdown
