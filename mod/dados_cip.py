"""
# dados_cip.py

Define as variáveis usadas no CIP

Este arquivo é parte do programa Irp_CIP
Para mais detalhes verifique os arquivos README, NOTICE e LICENSE

Copyright (C) 2023 Ultrix
"""
import hashlib

from mod.dados_ini import dados_ini

def dados_cip(cip):       
    """Gera código hash e URL de cada usuário

    :param int cip: Nùmero do CIP 
      
    :return: cip_codigo, url      
    :rtype: dict
    """
 
    var_ini = dados_ini()
    
    retorno = {}
    
    retorno['cip_codigo'] = hashlib.md5((var_ini['cip']['chave'] + str(cip)).encode('utf-8')).hexdigest()
    
    # Define a URL a partir do hash
    retorno['url'] = var_ini['cip']['url_base'] + '/' + var_ini['cip']['url_base_dir'] + '/' + retorno['cip_codigo']
 
    return retorno
