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

# endregion
