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

    def test_set_headers(self):
        self.data.headers(['name', 'surname', 'age'])
        self.assertEqual(self.data.data.headers, ['name', 'surname', 'age'])

    def test_filter_by_list(self):
        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        self.data.filter([42])
        self.assertEqual(self.data.get_data()[0], ('Arthur', 'Dent', 42))
        self.data.reset()

    def test_filter_by_key(self):

        def is_answer(number):
            if number == 42:
                return True

        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        self.data.filter(key=is_answer)
        self.assertEqual(self.data.get_data()[0], ('Arthur', 'Dent', 42))
        self.assertEqual(self.data.get_data()[1], ('Ford', 'Prefect', 42))
        self.data.reset()


if __name__ == '__main__':
    unittest.main()
