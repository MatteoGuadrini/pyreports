import unittest

import tablib

import pyreports
from tablib import Dataset


class TestDataTools(unittest.TestCase):
    data = Dataset(
        *[("Matteo", "Guadrini", 35), ("Arthur", "Dent", 42), ("Ford", "Prefect", 42)]
    )
    data.headers = ["name", "surname", "age"]

    def test_average(self):
        self.assertEqual(int(pyreports.average(self.data, "age")), 39)

    def test_most_common(self):
        self.assertEqual(pyreports.most_common(self.data, "age"), 42)

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
        self.assertEqual(
            pyreports.aggregate(names, surnames, ages)[0], ("Matteo", "Guadrini", 35)
        )
        ages = ["Name", "Surname"]
        self.assertRaises(
            tablib.InvalidDimensions, pyreports.aggregate, names, surnames, ages
        )
        self.assertRaises(pyreports.ReportDataError, pyreports.aggregate, names)

    def test_aggregate_fill_empty(self):
        names = self.data.get_col(0)
        surnames = self.data.get_col(1)
        ages = ["Name", "Surname"]
        self.assertEqual(
            pyreports.aggregate(names, surnames, ages, fill_empty=True)[2],
            ("Ford", "Prefect", None),
        )

    def test_chunks(self):
        data = Dataset(
            *[
                ("Matteo", "Guadrini", 35),
                ("Arthur", "Dent", 42),
                ("Ford", "Prefect", 42),
            ]
        )
        data.extend(
            [
                ("Matteo", "Guadrini", 35),
                ("Arthur", "Dent", 42),
                ("Ford", "Prefect", 42),
            ]
        )
        data.headers = ["name", "surname", "age"]
        self.assertEqual(
            list(pyreports.chunks(data, 4))[0][0], ("Matteo", "Guadrini", 35)
        )

    def test_merge(self):
        self.assertEqual(
            pyreports.merge(self.data, self.data)[3], ("Matteo", "Guadrini", 35)
        )

    def test_deduplication(self):
        data = Dataset(
            *[
                ("Matteo", "Guadrini", 35),
                ("Arthur", "Dent", 42),
                ("Matteo", "Guadrini", 35),
            ]
        )
        self.assertEqual(len(pyreports.deduplicate(data)), 2)

    def test_data_adapters(self):
        data = pyreports.DataAdapters(Dataset(*[("Matteo", "Guadrini", 35)]))
        self.assertIsInstance(data, pyreports.DataAdapters)

    def test_data_adapters_aggregate(self):
        names = self.data.get_col(0)
        surnames = self.data.get_col(1)
        ages = self.data.get_col(2)
        data = pyreports.DataAdapters(Dataset())
        self.assertRaises(
            pyreports.ReportDataError, data.aggregate, names, surnames, ages
        )
        data = pyreports.DataAdapters(Dataset(*[("Heart",)]))
        data.aggregate(names, surnames, ages)
        self.assertEqual(data.data[0], ("Heart", "Matteo", "Guadrini", 35))

    def test_data_adapters_merge(self):
        data = pyreports.DataAdapters(Dataset())
        self.assertRaises(pyreports.ReportDataError, data.merge, self.data)
        data = pyreports.DataAdapters(Dataset(*[("Arthur", "Dent", 42)]))
        data.merge(self.data)

    def test_data_adapters_counter(self):
        data = pyreports.DataAdapters(Dataset(*[("Arthur", "Dent", 42)]))
        data.merge(self.data)
        counter = data.counter()
        self.assertEqual(counter["Arthur"], 2)

    def test_adapters_chunks(self):
        data = pyreports.DataAdapters(
            Dataset(
                *[
                    ("Matteo", "Guadrini", 35),
                    ("Arthur", "Dent", 42),
                    ("Ford", "Prefect", 42),
                ]
            )
        )
        data.data.extend(
            [
                ("Matteo", "Guadrini", 35),
                ("Arthur", "Dent", 42),
                ("Ford", "Prefect", 42),
            ]
        )
        data.data.headers = ["name", "surname", "age"]
        self.assertEqual(list(data.chunks(4))[0][0], ("Matteo", "Guadrini", 35))

    def test_data_adapters_deduplicate(self):
        data = pyreports.DataAdapters(
            Dataset(
                *[
                    ("Matteo", "Guadrini", 35),
                    ("Arthur", "Dent", 42),
                    ("Matteo", "Guadrini", 35),
                ]
            )
        )
        data.deduplicate()
        self.assertEqual(len(data.data), 2)

    def test_data_adapters_iter(self):
        data = pyreports.DataAdapters(
            Dataset(
                *[
                    ("Matteo", "Guadrini", 35),
                    ("Arthur", "Dent", 42),
                    ("Matteo", "Guadrini", 35),
                ]
            )
        )
        self.assertEqual(list(iter(data.data))[1], ("Arthur", "Dent", 42))

    def test_data_adapters_get_items(self):
        data = pyreports.DataAdapters(
            Dataset(
                *[
                    ("Matteo", "Guadrini", 35),
                    ("Arthur", "Dent", 42),
                    ("Matteo", "Guadrini", 35),
                ],
                headers=("name", "surname", "age"),
            )
        )
        # Get row
        self.assertEqual(data[1], ("Arthur", "Dent", 42))
        # Get column
        self.assertEqual(data["name"], ["Matteo", "Arthur", "Matteo"])


if __name__ == "__main__":
    unittest.main()
