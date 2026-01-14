from llama_index.core.base.response.schema import Response
from llama_index.core.schema import NodeWithScore, TextNode
from src.validator import validate_response

def test_validador_aprova_citacao():
    # Mock da resposta do LlamaIndex
    node = NodeWithScore(node=TextNode(text="...", metadata={"article": "Art. 42"}), score=1.0)
    mock_response = Response(
        response="Conforme o Art. 42, o consumidor tem direito...",
        source_nodes=[node]
    )
    
    result = validate_response(mock_response)
    assert result.validation_passed is True
    assert result.sources_found[0].article == "Art. 42"

def test_validador_rejeita_sem_citacao():
    node = NodeWithScore(node=TextNode(text="...", metadata={"article": "Art. 42"}), score=1.0)
    mock_response = Response(
        response="O consumidor tem direitos gerais.", # Não citou o artigo
        source_nodes=[node]
    )
    
    result = validate_response(mock_response)
    assert result.validation_passed is False