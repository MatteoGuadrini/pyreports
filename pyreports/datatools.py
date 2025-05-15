#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# datatools -- pyreports
#
#     Copyright (C) 2025 Matteo Guadrini <matteo.guadrini@hotmail.it>
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
from .exception import DataObjectError
from collections import Counter
from tablib import Dataset, InvalidDimensions


# endregion


# region Classes
class DataObject:
    """Data object class"""

    def __init__(self, input_data: Dataset):
        # Discard all objects that are not Datasets
        if isinstance(input_data, Dataset):
            self._data = input_data
        else:
            raise DataObjectError("only Dataset object is allowed for input")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, dataset: Dataset):
        if not isinstance(dataset, Dataset):
            raise DataObjectError(f"{dataset} is not a Dataset object")
        self._data = dataset

    def clone(self):
        """Clone itself

        :return: Dataset
        """
        return DataObject(self.data)

    def column(self, index):
        _select_column(self.data, column=index)


class DataAdapters(DataObject):
    """Data adapters class"""

    def aggregate(self, *columns, fill_value=None):
        """Aggregate in the current Dataset other columns

        :param columns: columns added
        :param fill_value: fill value for empty field
        :return: None
        """
        if not self.data:
            raise DataObjectError("dataset is empty")
        local_columns = [self.data.get_col(col) for col in range(self.data.width)]
        local_columns.extend(columns)
        self.data = aggregate(*local_columns, fill_empty=True, fill_value=fill_value)

    def merge(self, *datasets):
        """Merge in the current Dataset other Dataset objects

        :param datasets: datasets that will merge
        :return: None
        """
        datasets = list(datasets)
        datasets.append(self.data)
        # Check if all Datasets are not empties
        if not all([data for data in datasets]):
            raise DataObjectError("one or more Datasets are empties")
        self.data = merge(*datasets)

    def counter(self):
        """Count value into the rows

        :return: Counter
        """
        return Counter((item for row in self.data for item in row))

    def chunks(self, length):
        """
        Yield successive n-sized chunks from Dataset

        :param length: n-sized chunks
        :return: generator
        """
        for idx in range(0, len(self.data), length):
            yield self.data[idx : idx + length]

    def deduplicate(self):
        """Remove duplicated rows

        :return: None
        """
        self.data.remove_duplicates()

    def subset(self, *columns):
        """New dataset with only columns added

        :param columns: select columns of new Dataset
        :return: Dataset
        """
        return self.data.subset(cols=columns)

    def sort(self, column, reverse=False):
        """Sort a Dataset by a specific column

        :param column: column to sort
        :param reverse: reversed order
        :return: Dataset
        """
        return self.data.sort(col=column, reverse=reverse)

    def __iter__(self):
        return (row for row in self.data)

    def __getitem__(self, item):
        return self.data[item]


class DataPrinters(DataObject):
    """Data printers class"""

    def print(self):
        """Print data

        :return: None
        """
        print(self)

    def average(self, column):
        """Average of list of integers or floats

        :param column: column name or index
        :return: float
        """
        return average(self.data, column)

    def most_common(self, column):
        """The most common element in a column

        :param column: column name or index
        :return: Any
        """
        return most_common(self.data, column)

    def percentage(self, filter_):
        """Calculating the percentage according to filter

        :param filter_: equality filter
        :return: float
        """
        return percentage(self.data, filter_)

    def __repr__(self):
        """Representation of DataObject

        :return: string
        """
        return f"<DataObject, headers={self.data.headers if self.data.headers else []}, rows={len(self)}>"

    def __str__(self):
        """Pretty representation of DataObject

        :return: string
        """
        return str(self.data)

    def __len__(self):
        """Measure length of DataSet

        :return: int
        """
        return len(self.data)


# endregion


# region Functions
def _select_column(data: Dataset, column):
    """Select Dataset column

    :param data: Dataset object
    :param column: column name or index
    :return: list
    """
    if isinstance(column, int):
        return data.get_col(column)
    else:
        return data[column]


def average(data: Dataset, column):
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
        raise DataObjectError("the column contains only int or float")
    # Calculate average
    return float(sum(data) / len(data))


def most_common(data: Dataset, column):
    """
    The most common element in a column

    :param data: Dataset object
    :param column: column name or index
    :return: Any
    """
    # Select column
    data = _select_column(data, column)
    return max(data, key=data.count)


def percentage(data: Dataset, filter_):
    """
    Calculating the percentage according to filter

    :param data: Dataset object
    :param filter_: equality filter
    :return: float
    """
    # Filtering data...
    data_filtered = [item for row in data for item in row if filter_ == item]
    quotient = len(data_filtered) / len(data)
    return quotient * 100


def counter(data: Dataset, column):
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
    :param fill_value: fills value for empty field if "fill_empty" argument is specified
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
                    raise InvalidDimensions("the columns are not the same length")
                max_len = len(list_)
        # Aggregate columns
        for column in columns:
            new_data.append_col(column)
        return new_data
    else:
        raise DataObjectError("you can aggregate two or more columns")


def merge(*datasets):
    """
    Merge two or more dataset in only one

    :param datasets: Dataset object collection
    :return: Dataset
    """
    if len(datasets) >= 2:
        new_data = Dataset()
        # Check len of row
        length_row = max([len(dataset[0]) for dataset in datasets])
        for data in datasets:
            if length_row != len(data[0]):
                raise InvalidDimensions("the row are not the same length")
            new_data.extend(data)
        return new_data
    else:
        raise DataObjectError("you can merge two or more dataset object")


def chunks(data: Dataset, length):
    """
    Yield successive n-sized chunks from data

    :param data: Dataset object
    :param length: n-sized chunks
    :return: generator
    """
    for idx in range(0, len(data), length):
        yield data[idx : idx + length]


def deduplicate(data: Dataset):
    """Remove duplicated rows

    :param data: Dataset object
    :return: Dataset
    """
    data.remove_duplicates()
    return data


def subset(data: Dataset, *columns):
    """Create a new Dataset with only the given columns

    :param data: Dataset object
    :param columns: selected columns
    :return: Dataset
    """
    return data.subset(cols=columns)


def sort(data, column, reverse=False):
    """Sort a Dataset by a specific column

    :param data: Dataset object
    :param column: column to sort
    :param reverse: reversed order
    :return: Dataset
    """
    return data.sort(col=column, reverse=reverse)


# endregion
