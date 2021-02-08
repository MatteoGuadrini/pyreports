#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# inputs -- reports
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

"""Contains all input management."""

# region Imports
import sqlite3
import pymssql
import mysql.connector


# endregion


# region Classes
class Connection:
    """Connection base class"""

    def __init__(self):
        """Connection base object"""
        self.connection = None
        self.host = None
        self.port = None
        self.database = None
        self.username = None
        self.password = None
        self.cursor = None

    def connect(self, **kwargs):
        pass

    def close(self):
        pass


class SQLliteConnection(Connection):
    """Connection sqlite class"""

    def connect(self, database):
        self.host = database
        self.connection = sqlite3.connect(database=self.host)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()


class MSSQLConnection(Connection):
    """Connection microsoft sql class"""

    def connect(self, host, username, password, database=None):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = pymssql.connect(self.host, self.username, self.password, self.database)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()


class MySQLConnection(Connection):
    """Connection mysql class"""

    def connect(self, host, username, password, database=None):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(self.host, self.username, self.password, self.database)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

# endregion
