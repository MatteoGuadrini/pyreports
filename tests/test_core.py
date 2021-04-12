import unittest
import reports
from tablib import Dataset


class TestExecutor(unittest.TestCase):

    data = reports.Executor(Dataset(['Matteo', 'Guadrini', 35]))

    def test_executor_instance(self):
        self.assertIsInstance(self.data, reports.Executor)

    def test_get_data(self):
        self.assertIsInstance(self.data.get_data(), Dataset)
        self.assertEqual(str(self.data.get_data()), 'Matteo|Guadrini|35')


if __name__ == '__main__':
    unittest.main()
