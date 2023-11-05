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
   
def variaveis():
    # Lê arquivo de configuração
    arqini = '../IrP_CIP_dados/cip.ini'
    ini = configparser.ConfigParser(dict_type=dict)
    ini.read(arqini)
    return ini._sections

def gera_cip(var_ini):
    chave = var_ini['cip']['chave']
    # URL para gerar o link
    url_base = var_ini['cip']['url_base']
    # Diretório dentro da URL base
    url_base_dir = var_ini['cip']['url_base_dir']
    # Arquivo modelo do cartão do CIP
    arq_cip = var_ini['cip']['arq_cip']
    # Arquivo temporário para o código QR
    arq_qr = var_ini['cip']['arq_qr']
    # Diretório de saída
    # A FAZER: enviar diretamente para o FTP do provedor
    dir_saida = var_ini['cip']['dir_saida']
    # Arquivo com a base de dados    
    arq_csv = var_ini['cip']['arq_csv']
        
    # Faz a leitura do arquivo CSV com os dados
    cadastro = pd.read_csv(arq_csv)
    
    for ind in cadastro.index:
        # Separa os dados que serão incluídos no CIP
        # Data de cadastro
        cip_data = cadastro['Carimbo de data/hora'][ind][0:10]
        # Nome completo
        cip_nome = cadastro['Nome completo'][ind]
        # Número do CIP
        cip_num = str(int(cadastro['CIP'][ind]))
        
        print(cip_num,cip_nome,cip_data)

        # Define o hash de cada pessoa
        cip_codigo = hashlib.md5((chave + cip_num).encode('utf-8')).hexdigest()
        
        # Define a URL a partir do hash
        url = url_base + '/' + url_base_dir + '/' + cip_codigo

        # Cria o código QR a partir da URL
        urlqr = qr.create(url)
        urlqr.png(arq_qr, scale=5, background=(255,255,255),module_color=(0,0,0))

        # Abre a imagem base do CIP
        img_base = Image.open(arq_cip, 'r')

        # Insere o código QR
        img_qr = Image.open(arq_qr, 'r')
        img_base.paste(img_qr,(600,245))

        # Insere os dados pessoais na imagem
        font = ImageFont.truetype("DejaVuSans.ttf", 30)
        escreve = ImageDraw.Draw(img_base)
        escreve.text((25, 310),cip_nome,(0,0,0),font=font)
        escreve.text((25, 390),cip_num,(0,0,0),font=font)
        escreve.text((25, 470),cip_data,(0,0,0),font=font)
        
        # Define URL para atualização de cadastro
        url_atualiza = """
            <p><a href="{cip_num}/{cip_num}.html">Clique aqui para 
            verificar se seu cadastro est&aacute atualizado</a></p>
            """.format(cip_num=cip_num)
        # Se o membro é ativo ou não
        if cadastro['Ativo'][ind] != 'Sim': 
            # Zera URL de cadastro caso seja inativo
            url_atualiza = ""
            largura, altura = img_base.size 
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 85)
            escreve.text((210, 200),'INATIVO',(255,0,0),font=font)

        # Cria um diretóriop para cada CIP
        dir_cip = dir_saida + '/' + cip_codigo
        if not os.path.exists(dir_cip):
            os.makedirs(dir_cip)
        # Cria um diretório para cada cadastro pessoal
        dir_pessoal = dir_cip + '/' + cip_num
        if not os.path.exists(dir_pessoal):
            os.makedirs(dir_pessoal)

        # Mostra imagem na tela. Usado para testes
        #img_base.show()
        
        # Grava o arquivo do CIP de saída
        arq_saida = cip_codigo + '.png'
        img_base.save(dir_cip + '/' + arq_saida)

        # Gera o index.html de cada diretório
        index_html = """
        <html>
            <head>
                <title>CIP</title>
            </head>
            <body>
                <center>
                    <br>
                    <img src="{arq_saida}" alt="CIP"/>
                    <p>CIP: {cip_num}</p>
                    {url_atualiza}
                </center>
            </body>
        </html>""".format(arq_saida=arq_saida,cip_num=cip_num,url_atualiza=url_atualiza)

        with open(dir_cip + '/' + 'index.html', 'w') as f:
            f.write(index_html)

        htaccess = """AuthType Basic
AuthName "CIP"
AuthUserFile {arq_htaccess}
require valid-user""".format(arq_htaccess=var_ini['cip']['arq_htaccess'])

        with open(dir_pessoal + '/' + '.htaccess', 'w') as f:
            f.write(htaccess)

        # Gera arquivo com o cadastro
        arq_cadastro = """
        <html>
            <head>
                <title>CIP</title>
            </head>
            <style>
                body {{
                background-color: #ffffff;
            }}
            </style>
            <body>
                    <p><h2>Dados cadastrais</h2></p>
                    <p>
                    <b>Nome:</b> {v1}<br>
                    <b>Endere&ccedil;o residencial:</b> {v2}<br>
                    <b>Cidade de resid&ecirc;ncia:</b> {v3}<br>
                    <b>Estado de resid&ecirc;ncia:</b> {v4}<br>
                    <b>CEP de resid&ecirc;ncia:</b> {v5}<br>
                    <b>Celular com DDD:</b> {v6}<br>
                    <b>Endere&ccedil;o de e-mail:</b> {v7}<br>
                    <b>Profiss&atilde;o:</b> {v8}<br>
                    <b>Endere&ccedil;os de contas em redes sociais:</b> {v9}<br>
                    <b>Ativo ou adormecido?:</b> {v10}<br>
                    <b>Grau:</b> {v11}<br>
                    <b>Mestre Instalado?:</b> {v12}<br>
                    <b>CIM:</b> {v13}<br>
                    <b>Nome e n&uacute;mero da Loja</b> (se adormecido, a Loja mais recente): {v14}<br>
                    <b>Rito</b>: {v15}<br>
                    <b>Pot&ecirc;ncia/Obedi&ecirc;ncia:</b> {v16}<br>
                    <b>Cidade e estado da Loja (Oriente):</b> {v17}<br>
                    <b>Endere&ccedil;o da Loja:</b> {v18}<br>
                    <b>Site ou rede social da Loja:</b> {v19}<br>
                    <b>Dias das sess&ocirc;es:</b> {v20}<br>
                    </p>                    
                    <p><a href="{form_atualiza}">Clique aqui para 
                        atualizar seu cadastro</a></p>
                    
            </body>
        </html>""".format(
        v1=cadastro['Nome completo'][ind],
        v2 = cadastro['Endereço residencial (rua, número, apto., bairro)'][ind],
        v3 = cadastro['Cidade de residência'][ind],
        v4 = cadastro['Estado de residência'][ind],
        v5 = cadastro['CEP de residência'][ind],
        v6 = cadastro['Celular com DDD'][ind],
        v7 = cadastro['Endereço de e-mail'][ind],
        v8 = cadastro['Profissão'][ind],
        v9 = cadastro['Endereços de contas em redes sociais (Facebook, LinkedIn, Twitter, Instagram, etc.)'][ind],
        v10 = cadastro['Ativo ou adormecido?'][ind],
        v11 = cadastro['Grau'][ind],
        v12 = cadastro['Mestre Instalado?'][ind],
        v13 = cadastro['CIM'][ind],
        v14 = cadastro['Nome e número da Loja (se adormecido, a Loja mais recente)'][ind],
        v15 = cadastro['Rito'][ind],
        v16 = cadastro['Potência/Obediência'][ind],
        v17 = cadastro['Cidade e estado da Loja (Oriente)'][ind],
        v18 = cadastro['Endereço da Loja'][ind],
        v19 = cadastro['Site ou rede social da Loja (se houver)'][ind],
        v20 = cadastro['Dias das sessões'][ind],
        form_atualiza=var_ini['cip']['form_atualiza']
        )

        if cadastro['Ativo'][ind] != 'Sim':
            arq_cadastro = "INATIVO"
            
        with open(dir_pessoal + '/' + cip_num + '.html', 'w') as f:
            f.write(arq_cadastro)
        

if __name__ == '__main__':
    gera_cip(variaveis())
    

# Gera senhas para uso no .htpasswd
#
# openssl passwd -apr1 8320
#
# Formato do .htpasswd:
# 1000:$apr1$q0zgYVO4$db2AE3WnUl3euhKTozvJV1
# 1001:$apr1$T9VVSX5w$kQw5ceuXL58ufdTKKEV2A.


# -------------------------------------------------------
#cadastro['Carimbo de data/hora'] = pd.to_datetime(cadastro['Carimbo de data/hora'], infer_datetime_format=True)



# img1 = Image.open(arq_cip, 'r')
# img1_w, img1_h = img1.size
# img1_w = img1_w // 3
# img1_h = img1_h // 3
# img = img1.resize((img1_w,img1_h))
# img_w, img_h = img.size
# background = Image.new('RGB', (856,539), (255, 255, 255))
# bg_w, bg_h = background.size
# offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
# background.paste(img, offset)

# font = ImageFont.truetype("DroidSans.ttf", 25)

# draw = ImageDraw.Draw(background)
# draw.text((0, 0),"Nome da Pessoa",(0,0,0),font=font)

# background.save('out.png')