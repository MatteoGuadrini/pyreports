import unittest
import reports
from tablib import Dataset
from tempfile import gettempdir

tmp_folder = gettempdir()


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

    def test_filter_by_list_and_column(self):
        self.data.headers(['name', 'surname', 'age'])
        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        self.data.filter([42], column='age')
        self.assertEqual(self.data.get_data()[0], 42)
        self.data.reset()

    def test_map(self):

        def int_to_string(number):
            if isinstance(number, int):
                return str(number)
            else:
                return number

        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        self.data.map(int_to_string)
        self.assertEqual(self.data.get_data()[1], ('Arthur', 'Dent', '42'))
        self.assertEqual(self.data.get_data()[2], ('Ford', 'Prefect', '42'))
        self.data.reset()

    def test_select_column(self):
        self.data.headers(['name', 'surname', 'age'])
        self.data.data.append(['Arthur', 'Dent', 42])
        self.data.data.append(['Ford', 'Prefect', 42])
        # By name
        self.assertEqual(self.data.select_column('age'), [35, 42, 42])
        # By number
        self.assertEqual(self.data.select_column(2), [35, 42, 42])
        self.data.reset()

    def test_count(self):
        self.assertEqual(len(self.data), 1)
        self.assertEqual(self.data.count_rows(), 1)
        self.data.headers(['name', 'surname', 'age'])
        self.assertEqual(self.data.count_column(), 3)

    def test_clone(self):
        new_data = self.data.clone()
        self.assertNotEqual(new_data, self.data)
        self.assertIsInstance(new_data, reports.Executor)
        self.assertEqual(type(new_data), type(self.data))


class TestReport(unittest.TestCase):
    input_data = Dataset(*[('Matteo', 'Guadrini', 35), ('Arthur', 'Dent', 42)])
    output_data = reports.manager('csv', f'{tmp_folder}/test_csv.csv')
    title = 'Test report'
    filters = ['42']
    column = 'age'
    count = True
    report = reports.Report(input_data=input_data,
                            title=title,
                            filters=filters,
                            map_func=lambda item: str(item) if isinstance(item, int) else item,
                            column=column,
                            count=count,
                            output=output_data)

    def test_report_object(self):
        self.assertIsInstance(self.report, reports.Report)

    def test_exec(self):
        self.report.exec()
        self.assertEqual(self.report.report[0][0], ('Arthur', 'Dent', '42'))
        self.assertEqual(self.report.report[1], 1)

    def test_export(self):
        self.report.export()
        self.assertIsInstance(self.report.output.read(), Dataset)


class TestReportBook(unittest.TestCase):
    input_data = Dataset(*[('Matteo', 'Guadrini', 35), ('Arthur', 'Dent', 42)])
    output_data = reports.manager('csv', f'{tmp_folder}/test_csv.csv')
    title = 'Test report'
    filters = ['42']
    column = 'age'
    count = True
    report1 = reports.Report(input_data=input_data,
                             title=title + '1',
                             filters=filters,
                             map_func=lambda item: str(item) if isinstance(item, int) else item,
                             column=column,
                             count=count,
                             output=output_data)
    report2 = reports.Report(input_data=input_data,
                             title=title + '2',
                             filters=filters,
                             map_func=lambda item: str(item) if isinstance(item, int) else item,
                             column=column,
                             count=count,
                             output=output_data)
    book = reports.ReportBook([report1])

    def test_report_book_instance(self):
        self.assertIsInstance(self.book, reports.ReportBook)

    def test_add_report(self):
        self.book.add(self.report2)
        self.assertRaises(reports.exception.ReportDataError, self.book.add, [self.report2])
        self.assertEqual(len(self.book), 2)

    def test_remove_report(self):
        self.book.remove()
        self.book.remove(0)
        self.assertEqual(len(self.book), 0)

    def test_merge_report_books(self):
        book1 = reports.ReportBook([self.report1])
        book2 = reports.ReportBook([self.report2])
        final_book1 = book1 + book2
        final_book1 += book1
        self.assertEqual(book1, final_book1)
        self.assertEqual(len(final_book1), 4)
        self.assertRaises(reports.exception.ReportDataError, final_book1.__add__, [final_book1])


if __name__ == '__main__':
    unittest.main()
