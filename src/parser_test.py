from parser import parse
import unittest
import json
from google.protobuf.json_format import MessageToDict
from data import load


class TestParser(unittest.TestCase):
    def test_jan_2018(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open("src/output_test/expected/expected_01_2018.json", "r") as fp:
            expected_01_2018 = json.load(fp)

        files = ["src/output_test/sheets/membros-ativos-contracheque-01-2018.ods"]

        dados = load(files, "2018", "01", "src/output_test/sheets")
        result_data = parse(dados, "mpmt/01/2018", 1, 2018)
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        print(f'{expected_01_2018}\n ###### \n {result_to_dict}')
        self.assertEqual(expected_01_2018, result_to_dict)

    def test_jul_2019(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open("src/output_test/expected/expected_07_2019.json", "r") as fp:
            expected_07_2019 = json.load(fp)

        files = [
            "src/output_test/sheets/membros-ativos-contracheque-07-2019.xlsx",
            "src/output_test/sheets/membros-ativos-verbas-indenizatorias-07-2019.xlsx",
        ]

        dados = load(files, "2019", "07", "src/output_test/sheets")
        result_data = parse(dados, "mpmt/07/2019", 7, 2019)
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        self.assertEqual(expected_07_2019, result_to_dict)


if __name__ == "__main__":
    unittest.main()
