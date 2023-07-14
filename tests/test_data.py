import unittest

import tablib

import pyreports
from tablib import Dataset


class TestDataTools(unittest.TestCase):
    data = Dataset(*[('Matteo', 'Guadrini', 35), ('Arthur', 'Dent', 42), ('Ford', 'Prefect', 42)])
    data.headers = ['name', 'surname', 'age']

    def test_average(self):
        self.assertEqual(int(pyreports.average(self.data, 'age')), 39)

    def test_most_common(self):
        self.assertEqual(pyreports.most_common(self.data, 'age'), 42)

    def test_percentage(self):
        self.assertEqual(int(pyreports.percentage(self.data, 42)), 66)

    def test_counter(self):
        c = pyreports.counter(self.data, 2)
        self.assertEqual(list(c.keys()), [35, 42])
        self.assertEqual(c.most_common(1), [(42, 2)])

    def test_aggregate(self):
        names = self.data.get_col(0)
        surnames = self.data.get_col(1)
        ages = self.data.get_col(2)
        self.assertEqual(pyreports.aggregate(names, surnames, ages)[0], ('Matteo', 'Guadrini', 35))
        ages = ['Name', 'Surname']
        self.assertRaises(tablib.InvalidDimensions, pyreports.aggregate, names,
                          surnames, ages)
        self.assertRaises(pyreports.ReportDataError, pyreports.aggregate, names)

    def test_aggregate_fill_empty(self):
        names = self.data.get_col(0)
        surnames = self.data.get_col(1)
        ages = ['Name', 'Surname']
        self.assertEqual(pyreports.aggregate(names, surnames, ages,
                                             fill_empty=True)[2],
                         ('Ford', 'Prefect', None))

    def test_chunks(self):
        data = Dataset(*[('Matteo', 'Guadrini', 35), ('Arthur', 'Dent', 42), ('Ford', 'Prefect', 42)])
        data.extend([('Matteo', 'Guadrini', 35), ('Arthur', 'Dent', 42), ('Ford', 'Prefect', 42)])
        data.headers = ['name', 'surname', 'age']
        self.assertEqual(list(pyreports.chunks(data, 4))[0][0], ('Matteo', 'Guadrini', 35))

    def test_merge(self):
        self.assertEqual(pyreports.merge(self.data, self.data)[3],
                         ('Matteo', 'Guadrini', 35))

    def test_deduplication(self):
        data = Dataset(*[('Matteo', 'Guadrini', 35),
                         ('Arthur', 'Dent', 42),
                         ('Matteo', 'Guadrini', 35)])
        self.assertEqual(len(pyreports.deduplicate(data)), 2)


if __name__ == '__main__':
    unittest.main()
