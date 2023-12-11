#!/usr/bin/env python3
# encoding: utf-8

"""
# maladireta.py
Gera arquivo com mala direta

Este arquivo é parte do programa IrP_CIP
Para mais detalhes verifique os arquivos README e LICENSE

Copyright (C) 2023 AMS
"""

import pandas as pd
import html.entities

from mod.dados_ini import dados_ini
from mod.dados_cip import dados_cip

acentos = {k: '&{};'.format(v) for k, v in html.entities.codepoint2name.items()}

def gera_maladireta():
    """
    # gera_maladireta - Gera mala direta para uso com o ZapFácil 
    
    Gera o arquivo de mala direta no diretório que está em 
    var_ini['cip']['dir_dados']/mala_direta.csv
    
    :param:

    :return:
    :rtype:
    """
    
    var_ini = dados_ini()
    
    # Faz a leitura do arquivo CSV com os dados
    cadastro = pd.read_csv(var_ini['cip']['arq_csv'])
    
    # Define variável com lista de membros de saída
    lista_membros = []
    
    for ind in cadastro.index:
        # Gera lista para mala direta excluindo os inativos
        if cadastro['Ativo'][ind] == 'Sim':

            # Formatação para o formato suportado pelo ZapFácil para discagem
            celular = cadastro['Celular com DDD'][ind]
            for caracter in '()- ':
                celular = celular.replace(caracter, '')
            
            # O ZapFácil não suporta parênteses
            celular_coord = cadastro['Celular do coordenador'][ind]
            for caracter in '()':
                celular_coord = celular_coord.replace(caracter, '')

            num_cip = cadastro['CIP'][ind]

            # Gera lista para mala direta
            lista_membros.append([
                num_cip,                                 # CIP
                cadastro['Tratamento'][ind],             # Tratamento
                cadastro['Apelido'][ind],                # Apelido
                cadastro['Nome completo'][ind],          # Nome
                dados_cip(num_cip)['url'],               # URL
                cadastro['Senha'][ind],                  # Senha
                cadastro['Regional'][ind],               # Regional
                cadastro['Coordenador regional'][ind],   # Coord_Regional
                celular_coord,                           # Contato_Coord
                '55' + str(celular),                     # Contato
                ])           
            
        # Mostra o andamento na tela
        # print(cadastro['CIP'][ind], cadastro['Nome completo'][ind])

    
    # Gera arquivo CSV com a lista de membros
    campos = ['CIP', 'Tratamento', 'Apelido', 'Nome', 'URL', 'Senha',
              'Regional', 'CoordRegional', 'ContatoCoord', 'Contato']
    df = pd.DataFrame(lista_membros, columns = campos)
    destino = var_ini['cip']['dir_dados'] + '/' + 'mala_direta.csv'
    df.to_csv(destino, index = False)
    print("Mala direta com", len(df), "registros:",destino)
    
