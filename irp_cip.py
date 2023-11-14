#!/usr/bin/env python3
# encoding: utf-8

"""
Processos da IrP

Processos disponíveis:

  maladireta      gera arquivo CSV com mala direta dos cadastrados 

  Exemplo: 
    ./python-modelo maladireta
    
  (c) 2023, AMS
    
"""

import argparse
import sys
import json

# Crie as funções relativas ao programa no diretório func, ou use outro nome se
# achar mais conveniente
from func.maladireta import gera_maladireta
    
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
                help='\"maladireta\" gera CSV com mala direta '
                     '\"\" ')
    
    args = parser.parse_args()
    
    if (args.processo == "maladireta"):
        gera_maladireta()

    elif (args.processo == "consultadb"):
        dados_mysql = conn_mysql(consulta_mysql)
        print(dados_mysql)
        
        dados_sqlite = conn_sqlite(consulta_sqlite)
        print(dados_sqlite)
        
    else:
        incorreto()  

if __name__ == '__main__':
    main_parser()


