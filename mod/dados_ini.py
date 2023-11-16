"""
# dados_ini.py

Configura as variáveis a serem utilizadas globalmente

Deve ser inserido nos programas que forem utilizar

Exemplo:

from mod.dados_ini import dados_ini

Este arquivo é parte do programa Irp_CIP
Para mais detalhes verifique os arquivos README, NOTICE e LICENSE

Copyright (C) 2023 Ultrix
"""

import configparser

def dados_ini():       
    """Lê arquivo INI de configuração.
      
    :return: variáveis do arquivo INI      
    :rtype: dict
    """
    arqini = 'cip.ini'
    ini = configparser.ConfigParser(dict_type=dict)
    ini.read(arqini)
    
    var_ini = ini._sections

    # Lê arquivo que contém a chave    
    ini.read(var_ini['cip']['arq_ini_chave'])
  
    return var_ini
