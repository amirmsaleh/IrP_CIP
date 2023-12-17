#!/usr/bin/env python3
# encoding: utf-8

"""
Processos da IrP

Processos disponíveis:

  maladireta          cria arquivo CSV com mala direta dos cadastrados
  cip                 cria arquivos do CIP
  ftp                 envia arquivos do CIP via FTP
  dados_admissao      mostra dados individuais de admissão
  dados_divulgacao    mostra dados individuais de divulgação
  
  --cip               número do CIP, necessário para os processos:
                          dados_admissao
                          dados_divulgacao

  Exemplo: 
    ./python-modelo dados_admissao --cip 999
    
  (c) 2023, AMS
    
"""

import argparse
import sys

from func.maladireta import gera_maladireta
from func.cip import gera_cip
from func.individual import dados_admissao, dados_divulgacao
from mod.dados_cip import baixa_csv
from mod.envia_ftp import envia_ftp
    
def incorreto():
    # Mostra o docstring do início do código
    print(__import__('__main__').__doc__)
    sys.exit()      

def main_parser():
       
    parser = argparse.ArgumentParser(
                        # Mostra o docstring do início do código
                        description=__import__('__main__').__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('processo',
                help='\"maladireta\"       gera CSV com mala direta | '
                     '\"cip\"              gera arquivos do CIP | '
                     '\"ftp\"              envia arquivos do CIP via FTP | '                     
                     '\"dados_admissao\"   dados individuais de admissão | '
                     '\"dados_divulgacao\" dados individuais de divulgação | '
                     )
    parser.add_argument('--cip', help='número do CIP')
    
    args = parser.parse_args()
    
    if (args.processo == "maladireta"):
        baixa_csv()
        gera_maladireta()

    elif (args.processo == "cip"):
        baixa_csv()
        gera_cip()
        
    elif (args.processo == "ftp"):
        baixa_csv()
        gera_cip()
        envia_ftp()

    elif (args.processo == "dados_admissao"):
        if args.cip:
            baixa_csv()
            dados_admissao(int(args.cip))
        else:
            incorreto()
                   
    elif (args.processo == "dados_divulgacao"):
        if args.cip:
            baixa_csv()
            dados_divulgacao(int(args.cip))
        else:
            incorreto()   
                
    else:
        incorreto()  

if __name__ == '__main__':
    main_parser()


