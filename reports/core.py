#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# core -- reports
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
        self.data = tablib.Dataset(*data, headers=header) if not isinstance(data, tablib.Dataset) else data
        self.origin = self.data

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
        self.data = self.origin

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
        for row in self.data:
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
        for row in self.data:
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

    def count_column(self):
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

    def __init__(self, input_data, title=None, filters=None, map_func=None, column=None, count=False, output=None):
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
            raise ValueError('Only Dataset object is allowed for input')
        # Set other arguments
        self.title = title
        self.filter = filters
        self.map = map_func
        self.column = column
        self.count = bool(count)
        if isinstance(output, FileManager):
            self.output = output
        else:
            raise ValueError('Only FileManager object is allowed for output')
        # Data for report
        self.report = None

    def __repr__(self):
        return f"<Report object title={self.title if self.title else None}>"

    def _print_data(self):
        """
        Print data and count

        :return: data and count
        """
        if isinstance(self.report, tuple):
            print(self.report[0])
            print(f'rows: {self.report[1]}')
        else:
            print(self.report)

    def exec(self):
        """
        Create Executor object to apply filters and map function to all inputs

        :return: None
        """
        # Create a temporary Executor object
        ex = Executor(self.data, header=self.data.headers)
        # Apply map function
        if self.map:
            ex.map(self.map)
        # Apply filters
        if self.filter:
            ex.filter(self.filter)
        # Count element
        if self.count:
            self.report = (ex.get_data(), len(ex))
        else:
            self.report = ex.get_data()

    def export(self):
        """
        Save data on output

        :return: if count is True, return row count
        """
        if self.output:
            self.output.write(self.report)
        else:
            self._print_data()

# endregion
