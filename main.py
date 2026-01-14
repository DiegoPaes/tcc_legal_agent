import os
import sys
from src.ingestion import build_pipeline
from src.rag_engine import get_rag_engine
from src.validator import validate_response
from src.config import settings

def main():
    print("⚖️  [TCC] AGENTE JURÍDICO BRASILEIRO ⚖️")
    print(f"📂 Diretório de Dados: {settings.DATA_DIR}")

    # 1. Verificação de Dados
    if not os.path.exists(settings.VECTOR_DB_PATH):
        print("⚡ Banco vetorial não encontrado. Iniciando ingestão automática...")
        try:
            build_pipeline()
        except Exception as e:
            print(f"❌ Erro Crítico na Ingestão: {e}")
            return

    # 2. Inicialização
    print("⚙️  Carregando modelos de IA...")
    try:
        engine = get_rag_engine()
    except Exception as e:
        print(f"❌ Erro ao carregar RAG Engine: {e}")
        print("Verifique sua OPENAI_API_KEY no arquivo .env")
        return
        
    print("\n🤖 Agente Pronto! (Digite 'sair' para encerrar)")
    print("-" * 60)

    # 3. Loop de Interação
    while True:
        user_query = input("\n[Usuário]: ")
        if user_query.lower() in ['sair', 'exit']:
            break
            
        print("... Consultando legislação ...")
        
        # Execução
        raw_response = engine.query(user_query)
        processed_response = validate_response(raw_response)
        
        # Exibição
        print("\n" + "="*20 + " RESPOSTA DA IA " + "="*20)
        print(processed_response.response_text)
        print("\n" + "-"*20 + " AUDITORIA TÉCNICA " + "-"*20)
        
        if processed_response.validation_passed:
            print("✅ VALIDAÇÃO: APROVADA (Citação verificada no contexto)")
        else:
            print("⚠️ VALIDAÇÃO: ALERTA (Possível alucinação ou falta de citação explícita)")
            
        print("📚 Fontes Consultadas:")
        for src in processed_response.sources_found:
            print(f"   - {src.article}")

if __name__ == "__main__":
    main()