import unittest
from tempfile import gettempdir
from unittest.mock import MagicMock, mock_open, patch

from tablib import Dataset
import pyreports

tmp_folder = gettempdir()


class TestFile(unittest.TestCase):

    def test_file(self):
        # Simulate pyreports.io.File object
        file = MagicMock()
        file.raw_data = ['Matteo\n', 'Guadrini\n', '35']
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
        # Real pyreports.io.File object
        file_real = pyreports.io.TextFile(f'{tmp_folder}/test_file.txt')
        real_data = file_real.read()
        self.assertIsInstance(real_data, Dataset)
        file_real.write(real_data)
        self.assertEqual(file_real.read()[0][0], 'Matteo')

    def test_log(self):
        log_real = pyreports.io.LogFile(f'{tmp_folder}/test_log.log')
        # Write data
        log_real.write(
            (["111.222.333.123", "HOME", "- [01/Feb/1998:01:08:39 -0800]", "GET", "/bannerad/ad.htm", "HTTP/1.0", "200",
              "198", "http://www.referrer.com/bannerad/ba_intro.htm", "Mozilla/4.01", "(Macintosh; I; PPC)"],
             ["111.222.333.123", "AWAY", "- [01/Feb/1998:01:08:39 -0800]", "GET", "/bannerad/ad7.gif", "HTTP/1.0",
              "200", "9332", "http://www.referrer.com/bannerad/ba_intro.htm", "Mozilla/4.01", "(Macintosh; I; PPC)"],
             ["111.222.333.123", "AWAY", "- [01/Feb/1998:01:08:39 -0800]", "GET", "/bannerad/click.htm", "HTTP/1.0",
              "200", "28083", "http://www.referrer.com/bannerad/ba_intro.htm", "Mozilla/4.01", "(Macintosh; I; PPC)"]
             ))
        # Read data
        real_data = log_real.read("([(\d\.)]+) (.*) \[(.*?)\] (.*?) (\d+) (\d+) (.*?) (.*?) (\(.*?\))",
                                  headers=('ip', 'user', 'date', 'req', 'ret', 'size', 'url', 'browser', 'host')
                                  )
        self.assertIsInstance(real_data, Dataset)

    def test_csv(self):
        csv_real = pyreports.io.CsvFile(f'{tmp_folder}/test_csv.csv')
        # Write data
        csv_real.write(['Matteo', 'Guadrini', 35])
        # Read data
        real_data = csv_real.read()
        self.assertIsInstance(real_data, Dataset)
        # Iterate csv
        for row in csv_real:
            self.assertIsInstance(row, str)

    def test_json(self):
        json_real = pyreports.io.JsonFile(f'{tmp_folder}/test_json.json')
        # Write data
        json_real.write(['Matteo', 'Guadrini', 35])
        # Read data
        real_data = json_real.read()
        self.assertIsInstance(real_data, Dataset)

    def test_yaml(self):
        yaml_real = pyreports.io.YamlFile(f'{tmp_folder}/test_yaml.yml')
        # Write data
        yaml_real.write(['Matteo', 'Guadrini', 35])
        # Read data
        real_data = yaml_real.read()
        self.assertIsInstance(real_data, Dataset)

    def test_excel(self):
        excel_real = pyreports.io.ExcelFile(f'{tmp_folder}/test_excel.xlsx')
        # Write data
        excel_real.write(['Matteo', 'Guadrini', 35])
        # Read data
        real_data = excel_real.read()
        self.assertIsInstance(real_data, Dataset)


class TestFileManager(unittest.TestCase):

    def test_file_manager(self):
        # Test file manager
        file_manager = pyreports.io.create_file_manager('file', f'{tmp_folder}/test_file.txt')
        # Write file
        file_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(file_manager.read(), Dataset)

    def test_log_manager(self):
        # Test log manager
        log_manager = pyreports.io.create_file_manager('log', f'{tmp_folder}/test_log.txt')
        # Write file
        log_manager.write(
            (["111.222.333.123", "HOME", "- [01/Feb/1998:01:08:39 -0800]", "GET", "/bannerad/ad.htm", "HTTP/1.0", "200",
              "198", "http://www.referrer.com/bannerad/ba_intro.htm", "Mozilla/4.01", "(Macintosh; I; PPC)"],
             ["111.222.333.123", "AWAY", "- [01/Feb/1998:01:08:39 -0800]", "GET", "/bannerad/ad7.gif", "HTTP/1.0",
              "200",
              "9332", "http://www.referrer.com/bannerad/ba_intro.htm", "Mozilla/4.01", "(Macintosh; I; PPC)"],
             ["111.222.333.123", "AWAY", "- [01/Feb/1998:01:08:39 -0800]", "GET", "/bannerad/click.htm", "HTTP/1.0",
              "200",
              "28083", "http://www.referrer.com/bannerad/ba_intro.htm", "Mozilla/4.01", "(Macintosh; I; PPC)"]
             ))
        # Read file
        self.assertIsInstance(log_manager.read("([(\d\.)]+) (.*) \[(.*?)\] (.*?) (\d+) (\d+) (.*?) (.*?) (\(.*?\))",
                                               headers=(
                                                   'ip', 'user', 'date', 'req', 'ret', 'size', 'url', 'browser',
                                                   'host')),
                              Dataset)

    def test_csv_manager(self):
        # Test csv manager
        csv_manager = pyreports.io.create_file_manager('csv', f'{tmp_folder}/test_csv.csv')
        # Write file
        csv_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(csv_manager.read(), Dataset)

    def test_json_manager(self):
        # Test json manager
        json_manager = pyreports.io.create_file_manager('json', f'{tmp_folder}/test_json.json')
        # Write file
        json_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(json_manager.read(), Dataset)

    def test_yaml_manager(self):
        # Test yaml manager
        yaml_manager = pyreports.io.create_file_manager('yaml', f'{tmp_folder}/test_yaml.yml')
        # Write file
        yaml_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(yaml_manager.read(), Dataset)

    def test_excel_manager(self):
        # Test excel manager
        excel_manager = pyreports.io.create_file_manager('xlsx', f'{tmp_folder}/test_excel.xlsx')
        # Write file
        excel_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(excel_manager.read(), Dataset)

    def test_manager_for_file(self):
        # Test file manager
        file_manager = pyreports.io.manager('file', f'{tmp_folder}/test_file.txt')
        # Write file
        file_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(file_manager.read(), Dataset)

    def test_manager_for_csv(self):
        # Test csv manager
        csv_manager = pyreports.io.manager('csv', f'{tmp_folder}/test_csv.csv')
        # Write file
        csv_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(csv_manager.read(), Dataset)

    def test_manager_for_json(self):
        # Test json manager
        json_manager = pyreports.io.manager('csv', f'{tmp_folder}/test_json.json')
        # Write file
        json_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(json_manager.read(), Dataset)

    def test_manager_for_yaml(self):
        # Test yaml manager
        yaml_manager = pyreports.io.manager('csv', f'{tmp_folder}/test_yaml.yml')
        # Write file
        yaml_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(yaml_manager.read(), Dataset)

    def test_manager_for_excel(self):
        # Test excel manager
        excel_manager = pyreports.io.manager('csv', f'{tmp_folder}/test_excel.xlsx')
        # Write file
        excel_manager.write(['Matteo', 'Guadrini', 45])
        # Read file
        self.assertIsInstance(excel_manager.read(), Dataset)


if __name__ == '__main__':
    unittest.main()
