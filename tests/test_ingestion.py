from src.ingestion import custom_legal_splitter

def test_splitter_separa_artigos_corretamente(texto_cdc_mock):
    docs = custom_legal_splitter(texto_cdc_mock)
    
    assert len(docs) == 2
    assert "Art. 42" in docs[0].metadata["article"]
    assert "repetição do indébito" in docs[0].text
    assert "Art. 43" in docs[1].metadata["article"]