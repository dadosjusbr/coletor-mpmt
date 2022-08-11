
import pandas as pd
import sys
import os

# Se for erro de não existir planilhas o retorno vai ser esse:
STATUS_DATA_UNAVAILABLE = 4
# Caso o erro for a planilha, que é invalida por algum motivo, o retorno vai ser esse:
STATUS_INVALID_FILE = 5


def _read(file):
    try:
        data = pd.read_excel(file, engine="odf").to_numpy()
        return data
    except Exception as excep:
        print(f"Erro lendo as planilhas: {excep} : {file}", file=sys.stderr)
        if 'verbas-indenizatorias' in file:
            pass
        else:
            sys.exit(STATUS_INVALID_FILE)


def load(file_names, year, month, output_path):
    """Carrega os arquivos passados como parâmetros.
    
     :param file_names: slice contendo os arquivos baixados pelo coletor.
    Os nomes dos arquivos devem seguir uma convenção e começar com 
    Membros ativos-contracheque e Membros ativos-Verbas Indenizatorias
     :param year e month: usados para fazer a validação na planilha de controle de dados
     :return um objeto Data() pronto para operar com os arquivos
    """

    if int(year) == 2018 or (int(year) == 2019 and int(month) < 7):
        # Não existe dados exclusivos de verbas indenizatórias nesse período de tempo.
        if not (
            os.path.isfile(
                output_path
                + f"/membros-ativos-contracheque-{month}-{year}.ods"
            )
        ):
            sys.stderr.write(f"Não existe planilha para {month}/{year}.")
            sys.exit(STATUS_DATA_UNAVAILABLE)

        contracheque = _read([c for c in file_names if "contracheque" in c][0])
    
        return Data_2018(contracheque, year, month)

    if not (
        os.path.isfile(
            output_path
            + f"/membros-ativos-contracheque-{month}-{year}.ods"
        )
        or os.path.isfile(
            output_path
            + f"/membros-ativos-verbas-indenizatorias-{month}-{year}.ods"
        )
    ):
        sys.stderr.write(f"Não existe planilhas para {month}/{year}.")
        sys.exit(STATUS_DATA_UNAVAILABLE)
    

    contracheque = _read([c for c in file_names if "contracheque" in c][0])
        
    if len(contracheque) < 30:
        sys.stderr.write(f"Planilha de contracheque vazia.")
        sys.exit(STATUS_DATA_UNAVAILABLE)

    # Quando a planilha de indenizações não é disponibilizada pelo órgão, o coletor baixa um arquivo limpo 
    # e entende que a planilha existe, dando erro já dentro da função _read, perdendo os dados do contracheque.
    indenizacoes = _read([i for i in file_names if "indenizatorias" in i][0])
    
    if 'NoneType' in str(type(indenizacoes)):
        return Data_2018(contracheque, year, month)
    
    if len(indenizacoes) < 30:
        sys.stderr.write(f"Planilha de verbas indenizatórias vazia.")
        return Data_2018(contracheque, year, month)
    return Data(contracheque, indenizacoes, year, month)

    


class Data:
    def __init__(self, contracheque, indenizacoes, year, month):
        self.year = year
        self.month = month
        self.contracheque = contracheque
        self.indenizacoes = indenizacoes

class Data_2018:
    def __init__(self, contracheque, year, month):
        self.year = year
        self.month = month
        self.contracheque = contracheque
