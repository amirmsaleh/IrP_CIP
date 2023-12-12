"""
# envia_ftp.py

Envio de informações do CIP via FTP

Este arquivo é parte do programa Irp_CIP
Para mais detalhes verifique os arquivos README, NOTICE e LICENSE

Copyright (C) 2023 Irmandade Progressista
"""

import os
from ftplib import FTP

from mod.dados_ini import dados_ini

def envia_ftp():       
    """Envia arquivos do CIP via FTP

    :param 
      
    :return:       
    :rtype: 
    """

    dados = dados_ini()
    
    arquivos_cip = '/home/amir/dev/IrP_CIP_dados/cip' # dados['cip']['dir_saida']
 
    print(arquivos_cip, dados['ftp']['host'], dados['ftp']['username'],
          dados['ftp']['password'], dados['ftp']['dir'])
    

    conn_ftp = FTP(dados['ftp']['host'],
                   dados['ftp']['username'],
                   dados['ftp']['password'])

    print('cwd ' + dados['ftp']['dir'])
    conn_ftp.cwd(dados['ftp']['dir'])
       
    def upload_ftp(path):
        files = os.listdir(path)
        os.chdir(path)
        for f in files:
            # print(path + r'/{}'.format(f))
            if os.path.isfile(path + r'/{}'.format(f)):
                fh = open(f, 'rb')
                print('STOR %s' % f)
                conn_ftp.storbinary('STOR %s' % f, fh)
                fh.close()
            elif os.path.isdir(path + r'/{}'.format(f)):
                print('mkd ' + f)
                conn_ftp.mkd(f)
                print('cwd ' + f)
                conn_ftp.cwd(f)
                upload_ftp(path + r'/{}'.format(f))
        print('cwd ..')
        conn_ftp.cwd('..')
        os.chdir('..')
    upload_ftp(arquivos_cip)   

