import pandas as pd
import sys
import os
import subprocess

# Se for erro de não existir planilhas o retorno vai ser esse:
STATUS_DATA_UNAVAILABLE = 4
# Caso o erro for a planilha, que é invalida por algum motivo, o retorno vai ser esse:
STATUS_INVALID_FILE = 5


def _read(file):
    try:
        data = pd.read_excel(file, engine="openpyxl").to_numpy()
    except Exception as excep:
        print(f"Erro lendo as planilhas: {excep}", file=sys.stderr)
        sys.exit(STATUS_INVALID_FILE)
    return data


def _convert_file(file, output_path):
    """
    Converte os arquivos ODS que estão corrompidos, para XLSX.
    """
    subprocess.run(
        ["libreoffice", "--headless", "--invisible", "--convert-to", "xlsx", file],
        capture_output=True,
        text=True,
    )  # Pega a saída para não interferir no print dos dados
    file_name = file.split(sep="/")[-1]
    file_name = f'{file_name.split(sep=".")[0]}.xlsx'
    # Move para o diretório passado por parâmetro
    subprocess.run(["mv", file_name, f"{output_path}/{file_name}"])
    return f"{output_path}/{file_name}"


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
                + f"/membros-ativos-contracheque-{month}-{year}.xlsx"
            )
        ):
            sys.stderr.write(f"Não existe planilha para {month}/{year}.")
            sys.exit(STATUS_DATA_UNAVAILABLE)

        contracheque = _read(
            _convert_file([c for c in file_names if "contracheque" in c][0], output_path)
        )
        return Data_2018(contracheque, year, month)

    if not (
        os.path.isfile(
            output_path
            + f"/membros-ativos-contracheque-{month}-{year}.xlsx"
        )
        or os.path.isfile(
            output_path
            + f"/membros-ativos-verbas-indenizatorias-{month}-{year}.xlsx"
        )
    ):
        sys.stderr.write(f"Não existe planilhas para {month}/{year}.")
        sys.exit(STATUS_DATA_UNAVAILABLE)
    

    contracheque = _read(
            _convert_file([c for c in file_names if "contracheque" in c][0], output_path)
        )

    if len(contracheque) < 30:
        sys.stderr.write(f"Planilha de contracheque vazia.")
        sys.exit(STATUS_DATA_UNAVAILABLE)

    indenizatorias = _read(
        _convert_file([i for i in file_names if "indenizatorias" in i][0], output_path)
    )

    if len(indenizatorias) < 30:
        sys.stderr.write(f"Planilha de verbas indenizatórias vazia.")
        sys.exit(STATUS_DATA_UNAVAILABLE)

    return Data(contracheque, indenizatorias, year, month)


class Data:
    def __init__(self, contracheque, indenizatorias, year, month):
        self.year = year
        self.month = month
        self.contracheque = contracheque
        self.indenizatorias = indenizatorias

class Data_2018:
    def __init__(self, contracheque, year, month):
        self.year = year
        self.month = month
        self.contracheque = contracheque
