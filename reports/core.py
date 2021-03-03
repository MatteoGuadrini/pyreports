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

    def __init__(self, manager):
        """
        Create Executor object

        :param manager: object received by the manager function
        """
        self.manager = manager
        self.data = None
        # Check type of manager
        if self.manager.type is 'database':
            self.reader = getattr(self.manager, 'execute')
            self.writer = getattr(self.manager, 'execute')
        elif self.manager.type is 'file':
            self.reader = getattr(self.manager, 'read')
            self.writer = getattr(self.manager, 'write')
        elif self.manager.type is 'ldap':
            self.reader = getattr(self.manager, 'query')
            self.writer = None
        else:
            self.reader = None
            self.writer = None

    def read(self, *args, **kwargs):
        """
        Read data

        :return: None
        """
        self.data = self.reader(*args, **kwargs)

    def write(self, *args, **kwargs):
        """
        Write data

        :return: None
        """
        self.writer(*args, **kwargs)

# endregion
