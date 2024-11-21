from typing import List, Dict, Optional
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search
from app.utils.helpers import clean_url

class SEOScraper:
    def __init__(self):
        self.user_agent = UserAgent()
        self.client = None
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    async def get_google_results(self, keyword: str, num_results: int = 10) -> List[str]:
        """Busca os resultados orgânicos do Google para uma keyword"""
        try:
            urls = []
            for url in search(keyword, num_results=num_results):
                urls.append(clean_url(url))
            return urls[:num_results]
        except Exception as e:
            raise Exception(f"Erro ao buscar resultados do Google: {str(e)}")
    
    async def get_page_content(self, url: str) -> Optional[str]:
        """Obtém o conteúdo HTML de uma página"""
        if not self.client:
            self.client = httpx.AsyncClient(timeout=30.0)
            
        headers = {"User-Agent": self.user_agent.random}
        try:
            response = await self.client.get(url, headers=headers, follow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Erro ao acessar {url}: {str(e)}")
            return None
    
    async def extract_main_content(self, html: str) -> str:
        """Extrai o conteúdo principal de uma página"""
        if not html:
            return ""
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove elementos indesejados
        for element in soup.find_all(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Tenta encontrar o conteúdo principal
        main_content = soup.find("main") or soup.find("article")
        if not main_content:
            # Fallback para o maior conjunto de parágrafos
            paragraphs = soup.find_all("p")
            if paragraphs:
                main_content = max(
                    [p.parent for p in paragraphs],
                    key=lambda x: len(x.get_text())
                )
        
        return main_content.get_text(strip=True) if main_content else ""
    
    async def extract_headings(self, html: str) -> List[str]:
        """Extrai os headings (h1-h6) de uma página"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, "html.parser")
        headings = []
        
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            for heading in soup.find_all(tag):
                text = heading.get_text(strip=True)
                if text:
                    headings.append(f"{tag.upper()}: {text}")
        
        return headings
    
    async def close(self):
        """Fecha o cliente HTTP"""
        if self.client:
            await self.client.aclose()
            self.client = None
