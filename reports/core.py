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
from .io import Connection


# endregion

class SQLDatabaseManager:
    """Database manager class for SQL connection"""

    def __init__(self, connection: Connection):
        """
        Database manager object for SQL connection

        :param connection: Connection based object
        :return None
        """
        self.connector = connection
        # Connect database
        self.connector.connect()
        # Set description
        self.description = self.connector.cursor.description
        # Row properties
        self.lastrowid = None
        self.rowcount = 0

    def reconnect(self):
        """
        Close and start connection

        :return: None
        """
        # Close connection
        self.connector.close()
        # Start connection, again
        self.connector.connect()

    def execute(self, query, params=None):
        """
        Execute query on database cursor

        :param query: SQL query language
        :param params: parameters of the query
        :return: None
        """
        # See if query was cached
        self.connector.cursor.execute(query, params)
        # Set last row id
        self.lastrowid = self.connector.cursor.lastrowid
        # Set row cont
        self.rowcount = self.connector.cursor.rowcount

    def executemany(self, query, params):
        """
        Execute query on database cursor with many parameters

        :param query: SQL query language
        :param params: list of parameters of the query
        :return: None
        """
        # See if query was cached
        self.connector.cursor.executemany(query, params)
        # Set last row id
        self.lastrowid = self.connector.cursor.lastrowid
        # Set row cont
        self.rowcount = self.connector.cursor.rowcount

    def fetchall(self):
        """
        Fetches all (or all remaining) rows of a query result set

        :return: list of tuples
        """
        return self.connector.cursor.fetchall()

    def fetchone(self):
        """
        Retrieves the next row of a query result set

        :return: list
        """
        return self.connector.cursor.fetchone()

    def fetchmany(self, size=1):
        """
        Fetches the next set of rows of a query result

        :param size: the number of rows returned
        :return: list of tuples
        """
        return self.connector.cursor.fetchmany(size)

    def callproc(self, proc_name, params=None):
        """
        Calls the stored procedure named

        :param proc_name: name of store procedure
        :param params: sequence of parameters must contain one entry for each argument that the procedure expects
        :return: sequence of parameters with modified output and input/output parameters
        """
        return self.connector.cursor.callproc(proc_name, params)


class NoSQLDatabaseManager:
    """Database manager class for NO-SQL connection"""

    def __init__(self, connection: Connection):
        """
        Database manager object for NO-SQL connection

        :param connection: Connection based object
        :return None
        """
        self.connector = connection
        # Connect database
        self.connector.connect()
