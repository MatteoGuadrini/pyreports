import unittest
import reports
from tablib import Dataset


class TestExecutor(unittest.TestCase):

    data = reports.Executor(Dataset(['Matteo', 'Guadrini', 35]))

    def test_executor_instance(self):
        self.assertIsInstance(self.data, reports.Executor)


if __name__ == '__main__':
    unittest.main()
