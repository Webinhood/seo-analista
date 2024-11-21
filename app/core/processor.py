from typing import Dict, List, Tuple
from markdownify import markdownify as md
from app.core.scraper import SEOScraper

class ContentProcessor:
    async def process_keyword(self, keyword: str) -> Dict:
        """Processa uma keyword e retorna os resultados formatados"""
        async with SEOScraper() as scraper:
            try:
                # Obtém os resultados do Google
                urls = await scraper.get_google_results(keyword)
                
                # Processa os 3 primeiros resultados
                top_3_content = {}
                for i, url in enumerate(urls[:3], 1):
                    html = await scraper.get_page_content(url)
                    if html:
                        content = await scraper.extract_main_content(html)
                        top_3_content[url] = {
                            'content': md(content),
                            'status': f'Processado conteúdo principal {i}/3'
                        }
                
                # Processa os 7 resultados restantes
                remaining_headings = {}
                for i, url in enumerate(urls[3:], 1):
                    html = await scraper.get_page_content(url)
                    if html:
                        headings = await scraper.extract_headings(html)
                        remaining_headings[url] = {
                            'headings': [md(heading) for heading in headings],
                            'status': f'Processado headings {i}/7'
                        }
                
                return {
                    "top3_content": top_3_content,
                    "remaining_headings": remaining_headings,
                    "status": "Análise completa"
                }
            
            except Exception as e:
                raise Exception(f"Erro ao processar keyword: {str(e)}")
    
    def format_markdown(self, text: str) -> str:
        """Formata texto para markdown"""
        try:
            return md(text)
        except Exception as e:
            raise Exception(f"Erro ao formatar markdown: {str(e)}")
