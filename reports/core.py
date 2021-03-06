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

# endregion
