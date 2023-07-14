#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# datatools -- pyreports
#
#     Copyright (C) 2023 Matteo Guadrini <matteo.guadrini@hotmail.it>
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

"""Contains all functions for data processing."""

# region Imports
from .exception import ReportDataError
from collections import Counter
from tablib import Dataset, InvalidDimensions


# endregion

# region Functions
def _select_column(data, column):
    """Select Dataset column

    :param data: Dataset object
    :param column: column name or index
    :return: list
    """
    # Check if dataset have a column
    if not data.headers:
        raise ReportDataError('dataset object must have the headers')
    # Select column
    if isinstance(column, int):
        return data.get_col(column)
    else:
        return data[column]


def average(data, column):
    """
    Average of list of integers or floats

    :param data: Dataset object
    :param column: column name or index
    :return: float
    """
    # Select column
    data = _select_column(data, column)
    # Check if all item is integer or float
    if not all(isinstance(item, (int, float)) for item in data):
        raise ReportDataError('the column contains only int or float')
    # Calculate average
    return float(sum(data) / len(data))


def most_common(data, column):
    """
    The most common element in a column

    :param data: Dataset object
    :param column: column name or index
    :return: Any
    """
    # Select column
    data = _select_column(data, column)
    return max(data, key=data.count)


def percentage(data, filter_):
    """
    Calculating the percentage according to filter

    :param data: Dataset object
    :param filter_: filter
    :return: float
    """
    # Filtering data...
    data_filtered = [item
                     for row in data
                     for item in row
                     if filter_ == item]
    quotient = len(data_filtered) / len(data)
    return quotient * 100


def counter(data, column):
    """
    Count all row value

    :param data: Dataset object
    :param column: column name or index
    :return: Counter
    """
    # Select column
    data = _select_column(data, column)
    # Return Counter object
    return Counter((item for item in data))


def aggregate(*columns, fill_empty: bool = False, fill_value=None):
    """
    Aggregate in a new Dataset the columns

    :param columns: columns added
    :param fill_empty: fill the empty field of data with "fill_value" argument
    :param fill_value: fill value for empty field if "fill_empty" argument is specified
    :return: Dataset
    """
    if len(columns) >= 2:
        new_data = Dataset()
        # Check max len of all columns
        max_len = max([len(column) for column in columns])
        for list_ in columns:
            if fill_empty:
                while max_len != len(list_):
                    list_.append(fill_value() if callable(fill_value) else fill_value)
            else:
                if max_len != len(list_):
                    raise InvalidDimensions('the columns are not the same length')
                max_len = len(list_)
        # Aggregate columns
        for column in columns:
            new_data.append_col(column)
        return new_data
    else:
        raise ReportDataError('you can aggregate two or more columns')


def merge(*datasets):
    """
    Merge two or more dataset in only one

    :param datasets: Dataset object collection
    :return: Dataset
    """
    if len(datasets) >= 2:
        new_data = Dataset()
        # Check len of row
        length_row = len(datasets[0][0])
        for data in datasets:
            if length_row != len(data[0]):
                raise InvalidDimensions('the row are not the same length')
            new_data.extend(data)
        return new_data
    else:
        raise ReportDataError('you can merge two or more dataset object')


def chunks(data, length):
    """
    Yield successive n-sized chunks from data

    :param data: Dataset object
    :param length: n-sized chunks
    :return: generator
    """
    for i in range(0, len(data), length):
        yield data[i:i + length]


def deduplicate(data):
    """Remove duplicated rows

    :param data: Dataset object
    :return: Dataset
    """
    return Dataset(*list(dict.fromkeys(data)))

# endregion
