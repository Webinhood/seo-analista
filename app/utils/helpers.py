from urllib.parse import urlparse, urlunparse
from typing import Optional

def clean_url(url: str) -> str:
    """Remove parâmetros de rastreamento e fragmentos da URL"""
    parsed = urlparse(url)
    # Remove fragmentos e query parameters
    clean = parsed._replace(fragment="", query="")
    return urlunparse(clean)

def sanitize_filename(filename: str) -> str:
    """Sanitiza um nome de arquivo removendo caracteres inválidos"""
    return "".join(c for c in filename if c.isalnum() or c in ("-", "_", ".")).rstrip()
