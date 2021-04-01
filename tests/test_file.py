import unittest
import reports
from tablib import Dataset
from tempfile import gettempdir
from unittest.mock import MagicMock, mock_open, patch

tmp_folder = gettempdir()


class TestFile(unittest.TestCase):

    def test_file(self):
        # Simulate reports.io.File object
        file = MagicMock()
        file.raw_data = ['first line\n', 'second line\n', 'third line']
        data = Dataset()
        for line in file.raw_data:
            data.append([line])
        # Read file data
        file.read = MagicMock(return_value=data)
        lines = file.read()
        self.assertIsInstance(lines, Dataset)
        # Write file data
        read_data = ''.join(file.raw_data)
        with open(f'{tmp_folder}/test_file.txt', 'w') as wf:
            wf.write(read_data)
        with patch('__main__.open', mock_open(read_data=read_data)):
            with open(f'{tmp_folder}/test_file.txt') as rf:
                result = rf.read()
        self.assertEqual(read_data, result)
        # Real reports.io.File object
        file_real = reports.io.File(f'{tmp_folder}/test_file.txt')
        real_data = file_real.read()
        self.assertIsInstance(real_data, Dataset)
        file_real.write(real_data)
        self.assertEqual(file_real.read()[0][0], 'first line')

    def test_csv(self):
        csv_real = reports.io.CsvFile(f'{tmp_folder}/test_csv.csv')
        # Write data
        csv_real.write(['Matteo', 'Guadrini', 35])
        # Read data
        real_data = csv_real.read()
        self.assertIsInstance(real_data, Dataset)

    def test_json(self):
        json_real = reports.io.JsonFile(f'{tmp_folder}/test_json.json')
        # Write data
        json_real.write(['Matteo', 'Guadrini', 35])
        # Read data
        real_data = json_real.read()
        self.assertIsInstance(real_data, Dataset)

    def test_yaml(self):
        yaml_real = reports.io.YamlFile(f'{tmp_folder}/test_yaml.yaml')
        # Write data
        yaml_real.write(['Matteo', 'Guadrini', 35])
        # Read data
        real_data = yaml_real.read()
        self.assertIsInstance(real_data, Dataset)

    def test_excel(self):
        excel_real = reports.io.YamlFile(f'{tmp_folder}/test_excel.xlsx')
        # Write data
        excel_real.write(['Matteo', 'Guadrini', 35])
        # Read data
        real_data = excel_real.read()
        self.assertIsInstance(real_data, Dataset)


if __name__ == '__main__':
    unittest.main()
