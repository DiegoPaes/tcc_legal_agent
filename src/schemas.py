from pydantic import BaseModel, Field
from typing import List, Optional

class SourceMetadata(BaseModel):
    """Metadados da fonte recuperada (Artigo de Lei)."""
    source: str
    article: str
    text_snippet: str

class AgentResponse(BaseModel):
    """Modelo estruturado da resposta do Agente."""
    response_text: str = Field(..., description="A resposta em linguagem natural")
    sources_found: List[SourceMetadata] = Field(default_factory=list, description="Fontes reais recuperadas do banco")
    validation_passed: bool = Field(False, description="Se a validação de citação foi aprovada")