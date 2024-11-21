from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.endpoints import router

app = FastAPI(
    title="SEO Content Analysis API",
    description="API para análise de conteúdo SEO através de web scraping",
    version="1.0.0"
)

# Montar diretórios estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/seo", response_class=HTMLResponse)
async def home(request: Request):
    """Renderiza a página inicial"""
    return templates.TemplateResponse("index.html", {"request": request})

# Incluir rotas da API com prefixo /seo
app.include_router(router, prefix="/seo")

@app.get("/status")
async def status():
    """Endpoint para verificar o status da API"""
    return {"status": "online"}
