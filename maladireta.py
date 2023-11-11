#!/usr/bin/env python3
# encoding: utf-8

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import pyqrcodeng as qr
import hashlib
import os
import pandas as pd
import configparser
import html.entities
import subprocess

acentos = {k: '&{};'.format(v) for k, v in html.entities.codepoint2name.items()}

def variaveis():
    # Lê arquivo de configuração
    arqini = 'cip.ini'
    
    ini = configparser.ConfigParser(dict_type=dict)
    ini.read(arqini)

    return ini._sections

def gera_maladireta(var_ini):
    # Faz a leitura do arquivo CSV com os dados
    cadastro = pd.read_csv(var_ini['cip']['arq_csv'])
    
    # Define variável com lista de membros de saída
    lista_membros = []
    
    for ind in cadastro.index:
        # Gera lista para mala direta excluindo os inativos
        if cadastro['Ativo'][ind] == 'Sim':
            celular = cadastro['Celular com DDD'][ind]
            for caracter in '()- ':
                celular = celular.replace(caracter, '')
            # Gera lista para mala direta
            lista_membros.append([cadastro['CIP'][ind],
                                  cadastro['Tratamento'][ind], 
                                  cadastro['Apelido'][ind],
                                  cadastro['Nome completo'][ind], 
                                  cadastro['Senha'][ind],
                                  cadastro['Regional'][ind],
                                  '55' + str(celular)])
            
        # Mostra o andamento na tela
        print(cadastro['CIP'][ind], cadastro['Nome completo'][ind])

    
    # Gera arquivo CSV com a lista de membros
    campos = ['CIP', 'Tratamento', 'Apelido', 'Nome', 'Senha', 'Regional', 'Celular']
    df = pd.DataFrame(lista_membros, columns = campos)
    destino = var_ini['cip']['dir_dados'] + '/' + 'mala_direta.csv'
    df.to_csv(destino, index = False)
    print("Arquivo CSV:",destino)
        
    
if __name__ == '__main__':
    gera_maladireta(variaveis())
    
