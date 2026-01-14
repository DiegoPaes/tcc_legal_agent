import re
import chromadb
from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from src.config import settings

def load_legal_text(filepath):
    """Lê o arquivo txt da lei."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def custom_legal_splitter(text: str) -> list[Document]:
    """
    Divide o texto em chunks baseados em Artigos (Regex).
    Padrão: Procura 'Art. X' até o próximo 'Art. Y' ou fim do texto.
    """
    pattern = r"(Art\.\s\d+.*?)(?=Art\.\s\d+|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    
    documents = []
    for match in matches:
        clean_content = " ".join(match.split()) # Remove quebras de linha excessivas
        
        # Tenta extrair 'Art. 42' para metadata
        try:
            parts = clean_content.split()
            art_number = f"{parts[0]} {parts[1]}"
        except IndexError:
            art_number = "Desconhecido"
            
        doc = Document(
            text=clean_content,
            metadata={"source": "CDC", "article": art_number}
        )
        documents.append(doc)
    
    return documents

def build_pipeline():
    """Executa o pipeline completo de ingestão."""
    print("🚀 [ETL] Iniciando Ingestão de Dados...")
    
    if not settings.RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {settings.RAW_DATA_PATH}")
        
    raw_text = load_legal_text(settings.RAW_DATA_PATH)
    documents = custom_legal_splitter(raw_text)
    print(f"📄 Texto processado: {len(documents)} artigos identificados.")

    # Configuração do ChromaDB persistente
    db = chromadb.PersistentClient(path=str(settings.VECTOR_DB_PATH))
    chroma_collection = db.get_or_create_collection("legal_rag")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    embed_model = OpenAIEmbedding(model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY)
    
    # Criação do índice (Gera embeddings e salva no disco)
    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )
    
    print("✅ [ETL] Indexação concluída e salva no disco!")

if __name__ == "__main__":
    build_pipeline()