from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API e Modelo
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Configuração de Chunking
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    
    # Caminhos Dinâmicos
    BASE_DIR: Path = Path(__file__).parent.parent
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def DATA_DIR(self) -> Path:
        return self.BASE_DIR / "data"

    @property
    def RAW_DATA_PATH(self) -> Path:
        return self.DATA_DIR / "raw" / "cdc.txt"

    @property
    def VECTOR_DB_PATH(self) -> Path:
        return self.DATA_DIR / "chroma_db"

settings = Settings()