"""
# listaconf.py
Lista as configurações que estão no arquivo conf.ini

Este arquivo é parte do programa python-modelo
Para mais detalhes verifique os arquivos README, NOTICE e LICENSE

Copyright (C) 2023 Ultrix
"""

# Importa variáveis globais de configuração
from mod.dados_ini import dados_ini

def listaconf():
    """
    # listaconf - Função para listar configurações do arquivo conf.ini 
    
    Usar na descrição da função o formato sugerido pelo Sphinx
    https://www.sphinx-doc.org/en/master/tutorial/describing-code.html#python    

    :param:

    :return: dados do arquivo INI
    :rtype: dict
    """
    
    dados = dados_ini()
    
    return(dados)
    
