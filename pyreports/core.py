#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# core -- pyreports
#
#     Copyright (C) 2021 Matteo Guadrini <matteo.guadrini@hotmail.it>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Contains all business logic and data processing."""

# region Imports
import tablib
from .io import FileManager
from .exception import ReportManagerError, ReportDataError


# endregion

# region Classes

class Executor:
    """Executor receives, processes, transforms and writes data"""

    def __init__(self, data, header=None):
        """
        Create Executor object

        :param data: everything type of data
        :param header: list header of data
        """
        self.data = tablib.Dataset(*data) if not isinstance(data, tablib.Dataset) else data
        # Set header
        if header or header is None:
            self.headers(header)
        self.origin = tablib.Dataset()
        self.origin.extend(self.data)

    def __len__(self):
        """
        Count data

        :return: integer
        """
        return self.count_rows()

    def __iter__(self):
        """
        Iterate over dataset

        :return: next value
        """
        return (row for row in self.data)

    def get_data(self):
        """
        Get dataset

        :return: dataset
        """
        return self.data

    def reset(self):
        """
        Reset data to original data

        :return: None
        """
        self.data = tablib.Dataset()
        self.data.extend(self.origin)

    def headers(self, header):
        """
        Set header

        :param header: header of data
        :return: None
        """
        self.data.headers = header

    def filter(self, flist=None, key=None, column=None):
        """
        Filter data through a list of strings (equal operator) and/or function key

        :param flist: list of strings
        :param key: function that takes a single argument and returns data
        :param column: select column name or index number
        :return: None
        """
        if flist is None:
            flist = []
        ret_data = tablib.Dataset(headers=self.data.headers)
        # Filter data through filter list
        for row in self:
            for f in flist:
                if f in row:
                    ret_data.append(row)
                    break
            # Filter data through function
            if key and callable(key):
                for field in row:
                    if bool(key(field)):
                        ret_data.append(row)
                        break
        self.data = ret_data
        # Single column
        if column and self.data.headers:
            self.data = self.select_column(column)

    def map(self, key, column=None):
        """
        Apply function to data

        :param key: function that takes a single argument
        :param column: select column name or index number
        :return: None
        """
        ret_data = tablib.Dataset(headers=self.data.headers)
        for row in self:
            # Apply function to data
            if key and callable(key):
                new_row = list()
                for field in row:
                    new_row.append(key(field))
                ret_data.append(new_row)
        self.data = ret_data
        # Return all data or single column
        if column and self.data.headers:
            self.data = self.select_column(column)

    def select_column(self, column):
        """
        Filter dataset by column

        :param column: name or index of column
        :return: Dataset object
        """
        if isinstance(column, int):
            return self.data.get_col(column)
        else:
            return self.data[column]

    def add_column(self, column, value):
        """
        Add column to data

        :param column: column name
        :param value: list value for column, or function with no arguments that returns a value
        :return: None
        """
        self.data.append_col(value, header=column)

    def del_column(self, column):
        """
        Delete column

        :param column: column name
        :return: None
        """
        del self.data[column]

    def count_rows(self):
        """
        Count all rows

        :return: integer
        """
        return len(self.data)

    def count_columns(self):
        """
        Count all column

        :return: integer
        """
        return len(self.data.headers)

    def clone(self):
        """
        Clone Executor object

        :return: executor
        """
        return Executor(self.origin, header=self.origin.headers)


class Report:
    """Report represents the workflow for generating a report"""

    def __init__(self,
                 input_data: tablib.Dataset,
                 title=None,
                 filters=None,
                 map_func=None,
                 column=None,
                 count=False,
                 output: FileManager = None):
        """
        Create Report object

        :param input_data: Dataset object
        :param title: title of Report object
        :param filters: list or function for filter data
        :param map_func: function for modifying data
        :param column: select column name or index
        :param count: count rows
        :param output: FileManager object
        """
        # Discard all objects that are not Datasets
        if isinstance(input_data, tablib.Dataset):
            self.data = input_data
        else:
            raise ReportDataError('Only Dataset object is allowed for input')
        # Set other arguments
        self.title = title
        self.filter = filters
        self.map = map_func
        self.column = column
        self.count = bool(count)
        if isinstance(output, FileManager):
            self.output = output
        else:
            raise ReportManagerError('Only FileManager object is allowed for output')
        # Data for report
        self.report = None

    def __repr__(self):
        return f"<Report object, title={self.title if self.title else None}>"

    def __str__(self):
        return self._print_data()

    def _print_data(self):
        """
        Print data and count

        :return: data and count
        """
        if isinstance(self.report, tuple):
            out = f'{self.report[0]}\nrows: {self.report[1]}'
            return out
        else:
            return self.report

    def exec(self):
        """
        Create Executor object to apply filters and map function to input data

        :return: None
        """
        # Create a temporary Executor object
        ex = Executor(self.data, header=self.data.headers)
        # Apply map function
        if self.map:
            ex.map(self.map)
        # Apply filters
        if self.filter:
            if callable(self.filter):
                ex.filter(key=self.filter)
            else:
                ex.filter(self.filter)
        # Count element
        if bool(self.count):
            self.count = len(ex)
        self.report = ex.get_data()

    def export(self):
        """
        Save data on output

        :return: if count is True, return row count
        """
        if isinstance(self.output, FileManager) or self.output is None:
            if self.output:
                self.output.write(self.report)
            else:
                print(self)
        else:
            raise ReportManagerError('the output object must be FileManager or NoneType object')


class ReportBook:
    """ReportBook represent a collection of Report's object"""

    def __init__(self, reports=None, title=None):
        """
        Create a ReportBook object

        :param reports: Report's object list
        :param title: title of report book
        """

        if reports is None:
            self.reports = list()
        else:
            self.reports = reports
        self.title = title

    def __add__(self, other):
        """
        Add report object

        :param other: Report object
        :return: ReportBook
        """
        if not isinstance(other, ReportBook):
            raise ReportDataError('you can only add ReportBook object')
        self.reports.extend(other.reports)
        return self

    def __iter__(self):
        """
        Return report iterator

        :return: iterable object
        """
        return (report for report in self.reports)

    def __len__(self):
        return len(self.reports)

    def __str__(self):
        output = f'ReportBook {self.title if self.title else None}\n'
        output += '\n'.join('\t' + str(report.title)
                            for report in self.reports)
        return output

    def __repr__(self):
        return f"<ReportBook object, title={self.title if self.title else None}>"

    def add(self, report: Report):
        """
        Add report object

        :param report: Report object
        :return: None
        """
        if not isinstance(report, Report):
            raise ReportDataError('you can only add Report object')
        self.reports.append(report)

    def remove(self, index: int = None):
        """
        Remove Report object, last added or index specified

        :param index: report number to remove
        :return: None
        """
        if index:
            self.reports.pop(index)
        else:
            self.reports.pop(-1)

    def export(self, output=None):
        """
        Save data on report output or an Excel workbook

        :param output: output path for report export
        :return: None
        """
        if output:
            # Prepare pyreports
            for report in self:
                report.exec()
            # Prepare book for export
            book = tablib.Databook(tuple([report.report for report in self]))
            # Save Excel WorkBook
            with open(output, 'wb') as f:
                f.write(book.export('xlsx'))
        else:
            for report in self:
                report.exec()
                report.export()

# endregion
