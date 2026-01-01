#!/usr/bin/env python3
# encoding: utf-8

"""
# maladireta.py
Gera arquivo com mala direta

Este arquivo é parte do programa IrP_CIP
Para mais detalhes verifique os arquivos README e LICENSE

Copyright © 2023 AMS
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
    
    # Define variáveis com lista de membros de saída
    lista_membros = []
    lista_membros_zapsimples = []
    
    for ind in cadastro.index:
        # Gera lista para mala direta excluindo os inativos
        if cadastro['Ativo'][ind] == 'Sim':

            # Formatação para o formato suportado para discagem
            celular = cadastro['Celular com DDD'][ind]
            for caracter in '()- ':
                celular = celular.replace(caracter, '')
            
            # Remove os parênteses
            celular_coord = cadastro['Celular do coordenador'][ind]
            for caracter in '()':
                celular_coord = celular_coord.replace(caracter, '')

            num_cip = cadastro['CIP'][ind]

            # Gera lista para mala direta
            contato = False
            if str(celular)[0] == '+':
                contato = str(celular)[1:]
            else:
                contato = '55' + str(celular)
    
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
                contato,                                 # Contato
                cadastro['Endereço de e-mail'][ind],	 # E-mail
            ])

            lista_membros_zapsimples.append([
                # campo Nome: tratamento + apelido
                f"{cadastro['Tratamento'][ind]} {cadastro['Apelido'][ind]}",
                # Campo Número: número do celular
                contato,
                # campo E-mail: URL
                cadastro['Endereço de e-mail'][ind], # E-mail
                # dados_cip(num_cip)['url'], # URL para acesso ao cartão CIP
                # campo Var1: CIP
                num_cip,
                # campo Var2: senha
                cadastro['Senha'][ind],
                # Campo Var3: regional, coordenador e contato do cordenador
                f"Regional: {cadastro['Regional'][ind]} | "
                f"Aos cuidados de {cadastro['Coordenador regional'][ind]}: "
                f"{celular_coord}",
            ])

        # Mostra o andamento na tela
        # print(cadastro['CIP'][ind], cadastro['Nome completo'][ind])

    # Gera arquivo CSV com a mala direta
    # campos = ['CIP', 'Tratamento', 'Apelido', 'Nome', 'URL', 'Senha',
    #           'Regional', 'CoordRegional', 'ContatoCoord', 'Contato','Email']
    campos = ['Position', 'Title', 'First Name', 'Last Name', 'Website', 'Zip Code', 'City', 'Address Line 1', 'Address Line 2', 'Mobile','Email']
    df = pd.DataFrame(lista_membros, columns = campos)
    # df.sort_values('Nome', ascending=True, inplace=True)
    df.sort_values('First Name', ascending=True, inplace=True)
    destino = var_ini['cip']['dir_dados'] + '/' + 'mala_direta.csv'
    df.to_csv(destino, index = False)
    print("Mala direta com", len(df), "registros:",destino)

    # Gera arquivo CSV para o ZapSimples
    campos_zap_simples = ['Nome', 'Número', 'E-mail', 'Var1', 'Var2', 'Var3']
    df_zap_simples = pd.DataFrame(lista_membros_zapsimples,
                                  columns = campos_zap_simples)
    df_zap_simples.sort_values('Nome', ascending=True, inplace=True)
    destino = var_ini['cip']['dir_dados'] + '/' + 'mala_direta_zapsimples.csv'
    df_zap_simples.to_csv(destino, index = False)
    print("Mala direta com", len(df_zap_simples), "registros:",destino)
    
