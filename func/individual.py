#!/usr/bin/env python3
# encoding: utf-8

"""
# individual.py
Gera dados individuais

Este arquivo é parte do programa IrP_CIP
Para mais detalhes verifique os arquivos README e LICENSE

Copyright (C) 2023 AMS
"""

import pandas as pd
import html.entities

from mod.dados_ini import dados_ini
from mod.dados_cip import dados_cip

acentos = {k: '&{};'.format(v) for k, v in html.entities.codepoint2name.items()}

def dados_admissao(cip):
    """
    # dados_admissão - Gera dados individuais de admissão 
    
    :param int CIP: Nùmero do CIP 

    :return:
    :rtype:
    """
    
    var_ini = dados_ini()
    
    # Faz a leitura do arquivo CSV com os dados
    cadastro = pd.read_csv(var_ini['cip']['arq_csv'])
    
    dados_membro = cadastro[cadastro['CIP'] == cip]
       
    # print(dados_cip(cip))

    for ind in dados_membro.index:
        
        mensagem = ("""
*{}* 

CIP: {}

Link para o cartão do CIP e verificação de validade:
{}
                    
Usuário para verificação de atualização de cadastro (CIP): {} 
Senha: {}

Link entrar no grupo de WhatsApp _IrP - Notícias - Irmandade Progressista_:
{}

Ao entrar no grupo de WhatsApp, por favor faça uma breve apresentação.
                    """)
                   
        print(mensagem.format(
                dados_membro['Nome completo'][ind],
                cip,
                dados_cip(cip)['url'],
                cip,
                dados_membro['Senha'][ind],
                dados_ini()['cip']['whatsapp'],
                )
              )
    
        mensagem = ("""
*NOVO MEMBRO DA IRMANDADE PROGRESSISTA*

Caros IIr.'., a partir desse momento a Irmandade Progressista conta com mais um membro:

Nome: *{}*
CIP: {}
Regional: {}
Regional sob coordenação de: {}
 
Cada um dos membros da Irmandade Progressista já recebeu os dados do novo Ir.'. através de mensagem particular.

O Ir.'. foi convidado a participar deste grupo de WhatsApp, e entrará se julgar conveniente. 
Lembrando que a participação em grupos de WhatsApp é opcional, e não é requisito para pertencimento à Irmandade Progressista.
                   """)
    
        print (mensagem.format(
               dados_membro['Nome completo'][ind],
               cip,
               dados_membro['Regional'][ind],
               dados_membro['Coordenador regional'][ind]
               )
            )
    
def dados_divulgacao(cip):
    """
    # dados_admissão - Gera dados individuais para divulgação 
    
    :param int CIP: Nùmero do CIP 

    :return:
    :rtype:
    """

    var_ini = dados_ini()
    
    # Faz a leitura do arquivo CSV com os dados
    cadastro = pd.read_csv(var_ini['cip']['arq_csv'])
    
    dados_membro = cadastro[cadastro['CIP'] == cip]
       
    # print(dados_cip(cip))

    campos = [  'Nome completo',
                'Profissão',  
                'Endereços de contas em redes sociais (Facebook, LinkedIn, Twitter, Instagram, etc.)', 
                'Cidade e estado da Loja (Oriente)', 
                'Ativo ou adormecido?', 
                'Se estiver adormecido, desde quando, e o motivo',  
                'Rito',  
                'Grau', 
                'Mestre Instalado?', 
                'Nome e número da Loja (se adormecido, a Loja mais recente)', 
                'Site ou rede social da Loja (se houver)',  
                'Potência/Obediência', 
                'Endereço da Loja', 
                'Dias das sessões',  
                'Tendência política', 
                'Como avalia a situação política, social e econômica do Brasil atualmente?', 
                'Cidade de residência', 
                'Estado de residência', 
                'Faz parte de algum partido político, sindicato, associação, etc.? Se sim, qual?',  
                'Outras informações que julgar relevantes',  
                'Boa parte dos maçons apoiaram e seguem apoiando ideologias anti-progressistas, muitas vezes de extrema-direita. Qual é sua avaliação sobre essa questão?', 
                'Você leu com atenção e concorda com os termos do manifesto da Irmandade Progressista?', 
                'Você conhece algum Ir.\'. que já seja membro da Irmandade Progressista?', 
                'Se você conhece algum Ir.\'. membro da Irmandade Progressista, qual é o nome dele?',  
                'Regional', 
                'Coordenador regional'] 

    for ind in dados_membro.index:
        print ('*CANDIDATO À IRMANDADE PROGRESSISTA - ' 
               + dados_membro["Nome completo"][ind] + '*')
        print ('')
        print ('{{tratamento}} {{apelido}}, {{periodo-dia}}.')
        print ('')
        print ('Seguem abaixo os dados de *'
               + dados_membro["Nome completo"][ind] + 
               '*, que deseja fazer parte da Irmandade Progressista.')
        print ('')
        print ('Caso haja algum óbice ou observação a ser feita, por favor '
               'encaminhe à regional',
               dados_membro['Regional'][ind] + ' da Irmandade Progressista, que '
               'está sob os cuidados de',
               dados_membro['Coordenador regional'][ind] 
               + ' - ' + dados_membro['Celular do coordenador'][ind] + '.')
        print ('')
        print ('Gostaria de pedir sua paciência e colaboração, pois como '
               'sabemos, nas semanas recentes passamos por um processo de '
               'reestruturação da comunicação interna e das coordenações '
               'regionais. Estamos retomando agora as admissões, por isso ' 
               'haverá uma certa frequência de novos candidatos nos próximos '
               'dias.')
        print ('')
        
        for campo in campos:
            print ('*' + campo + ":*",dados_membro[campo][ind])    
