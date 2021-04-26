import unittest
import reports
from tablib import Dataset


class TestDataTools(unittest.TestCase):
    data = Dataset(*[('Matteo', 'Guadrini', 35), ('Arthur', 'Dent', 42), ('Ford', 'Prefect', 42)])
    data.headers = ['name', 'surname', 'age']

    def test_average(self):
        self.assertEqual(int(reports.average(self.data, 'age')), int(39.666666666666664))

    def test_most_common(self):
        self.assertEqual(reports.most_common(self.data, 'age'), 42)


if __name__ == '__main__':
    unittest.main()
