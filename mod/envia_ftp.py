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
    
    arquivos_cip = dados['cip']['dir_saida']
 
    # print(arquivos_cip, dados['ftp']['host'], dados['ftp']['username'],
    #      dados['ftp']['password'], dados['ftp']['dir'])
    
    conn_ftp = FTP(dados['ftp']['host'],
                   dados['ftp']['username'],
                   dados['ftp']['password'])

    f_htpasswd = open(dados['cip']['dir_dados'] + '/' + '.htpasswd', 'rb')
    print('FTP: .htpasswd')
    conn_ftp.storbinary('STOR .htpasswd', f_htpasswd)

    conn_ftp.cwd(dados['ftp']['dir'])
    
    def upload_ftp(path):
        files = os.listdir(path)
        os.chdir(path)
        for f in files:
            if os.path.isfile(path + r'/{}'.format(f)):
                fh = open(f, 'rb')
                print(path + '/%s' % f)
                conn_ftp.storbinary('STOR %s' % f, fh)
                fh.close()
            elif os.path.isdir(path + r'/{}'.format(f)):
                try:
                    print('FTP:', f)
                    conn_ftp.mkd(f)
                except:
                    print('FTP:', f, "já existe")
                conn_ftp.cwd(f)
                upload_ftp(path + r'/{}'.format(f))
        conn_ftp.cwd('..')
        os.chdir('..')
    upload_ftp(arquivos_cip)   

