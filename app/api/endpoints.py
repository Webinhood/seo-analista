from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.processor import ContentProcessor

router = APIRouter()

class KeywordRequest(BaseModel):
    keyword: str
    language: str

@router.post("/scrape-content")
async def scrape_content(request: KeywordRequest):
    """
    Endpoint para análise de conteúdo SEO baseado em uma keyword
    
    Args:
        request: Objeto contendo a keyword e idioma para análise
        
    Returns:
        Dict contendo o conteúdo dos top 3 resultados e headings dos demais
    """
    try:
        # Validar idioma
        if request.language not in ["pt-BR", "en"]:
            raise HTTPException(
                status_code=400,
                detail="Idioma não suportado. Use 'pt-BR' ou 'en'"
            )
        
        # Adicionar parâmetro de idioma à keyword
        search_query = f"language:{request.language} {request.keyword}"
        
        processor = ContentProcessor()
        results = await processor.process_keyword(search_query)
        return results
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a requisição: {str(e)}"
        )
