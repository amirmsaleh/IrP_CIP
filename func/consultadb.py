"""
# consultadb.py
Faz consulta a um banco de dados MySQL

Este arquivo é parte do programa python-modelo
Para mais detalhes verifique os arquivos README, NOTICE e LICENSE

Copyright (C) 2023 Ultrix
"""

import pandas as pd

# Importa variáveis globais de configuração
from mod.dados_ini import dados_ini


def consulta_mysql(conn):
    """Exemplo de consulta a banco de dados MySQL
    
    Usar na descrição da função o formato sugerido pelo Sphinx
    https://www.sphinx-doc.org/en/master/tutorial/describing-code.html#python

    :param conn conn: Objeto de conexão ao banco de dados 

    :return: dados da consulta        
    :rtype: pandas dataframe
    """
        
    # String para busca dos ids das chamadas dentro da tabela de filas
    busca_sql = ("SELECT partition, time_id, call_id, queue, agent, verb "
                 "FROM {}.queue_log "
                 "LIMIT 5")
       
    # Executa a busca e coloca num dataframe do pandas
    # Procure usar o Pandas para manipulação de dados. Ele já tem inúmeras
    # fucionalidades embutidas que poupam muito trabalho
    df_busca = pd.read_sql(busca_sql.format(dados_ini()['dbs']['nome']),
                           con=conn)
                           
    return df_busca
    
def consulta_sqlite(conn):
    """Exemplo de consulta a banco de dados MySQL
    
    Usar na descrição da função o formato sugerido pelo Sphinx
    https://www.sphinx-doc.org/en/master/tutorial/describing-code.html#python

    :param conn conn: Objeto de conexão ao banco de dados 

    :return: dados da consulta        
    :rtype: pandas dataframe
    """
    editora = "Companhia das Letras"
    
    # String para busca dos ids das chamadas dentro da tabela de filas
    busca_sql = ("SELECT  id, titulo, autor, qtd_paginas, editora "
                 "FROM livros "
                 "WHERE editora = \'{}\'")
           
    # Executa a busca e coloca num dataframe do pandas
    # Procure usar o Pandas para manipulação de dados. Ele já tem inúmeras
    # fucionalidades embutidas que poupam muito trabalho    
    df_busca = pd.read_sql(busca_sql.format(editora), con=conn)
                           
    return df_busca


                           
           
