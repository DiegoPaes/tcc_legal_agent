from llama_index.core.base.response.schema import Response
from src.schemas import AgentResponse, SourceMetadata

def validate_response(engine_response: Response) -> AgentResponse:
    """
    Transforma a resposta bruta do LlamaIndex em um objeto estruturado e validado.
    """
    ai_text = engine_response.response
    source_nodes = engine_response.source_nodes
    
    # 1. Extrair Metadados das Fontes
    found_sources = []
    articles_in_context = []
    
    for node in source_nodes:
        meta = node.metadata
        art = meta.get('article', 'N/A')
        snippet = node.node.get_text()[:100] + "..." # Pega um pedaço do texto
        
        found_sources.append(SourceMetadata(
            source=meta.get('source', 'Unknown'),
            article=art,
            text_snippet=snippet
        ))
        articles_in_context.append(art)
        
    # 2. Validação: A IA citou o artigo que estava no contexto?
    # Busca simples (pode ser melhorada com regex)
    validation_passed = False
    for art in articles_in_context:
        if art in ai_text:
            validation_passed = True
            break
            
    # Se a IA disse que não encontrou, a validação tecnicamente passou (não alucinou lei falsa)
    if "Não encontrei base legal" in ai_text:
        validation_passed = True

    return AgentResponse(
        response_text=ai_text,
        sources_found=found_sources,
        validation_passed=validation_passed
    )