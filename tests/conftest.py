import pytest

@pytest.fixture
def texto_cdc_mock():
    return """
    Art. 42. Na cobrança de débitos, o consumidor inadimplente não será exposto a ridículo.
    Parágrafo único. O consumidor cobrado em quantia indevida tem direito à repetição do indébito.
    
    Art. 43. O consumidor, sem prejuízo do disposto no art. 86, terá acesso às informações.
    """