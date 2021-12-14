from coleta import coleta_pb2 as Coleta


def captura(mes, ano):
    metadado = Coleta.Metadados()
    metadado.nao_requer_login = True
    metadado.nao_requer_captcha = True
    metadado.acesso = Coleta.Metadados.FormaDeAcesso.AMIGAVEL_PARA_RASPAGEM
    metadado.extensao = Coleta.Metadados.Extensao.ODS
    metadado.estritamente_tabular = False
    """
     Em Julho de 2019 é disponibilizado o arquivo de Verbas Indenizatórias.
     Juntamente com isso, o arquivo Membros ativos-contracheque perde algumas
     colunas e ganha outras, fazendo assim com que o órgão perca o formato
     constante de seus dados nesse mês.
    """
    if ano == 2019 and mes == 7:
        metadado.formato_consistente = False
    else:
        metadado.formato_consistente = True
    metadado.tem_matricula = True
    metadado.tem_lotacao = True
    metadado.tem_cargo = True
    """
     O detalhamento dos dados, principalmente outras_receitas, não sofrem 
     alterações com a entrada ou saída do arquivo Verbas Indenizatorias, 
     pois o arquivo contracheque sempre carrega colunas como gratificação natalina,
     abono de permanência, função de confiança e férias.
    """
    metadado.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    if int(ano) == 2018 or (int(ano) == 2019 and int(mes) < 7):
        metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.SUMARIZADO
    else:
        metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO


    return metadado
