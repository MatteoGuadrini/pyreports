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
import mysql.connector as mdb
import psycopg2
import csv
import json
import yaml


# endregion


# region Classes
class Connection:
    """Connection base class"""

    def __init__(self, host=None, port=None, database=None, username=None, password=None):
        """Connection base object"""
        self.connection = None
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.cursor = None

    def connect(self):
        pass

    def close(self):
        pass


class File:
    """File base class"""

    def __init__(self, filename, mode='r'):
        """
        File base object

        :param filename: file path
        :param mode: mode of open file. Default is read.
        """
        with open(filename, mode=mode) as f:
            self.file = filename
            self.raw_data = f

    def write(self, data):
        """
        Write data on file

        :param data: data to write on file
        :return: None
        """
        with self.raw_data as file:
            file.write(data)

    def read(self, **kargs):
        """
        Read with format

        :return: file
        """
        return self.raw_data


class CsvFile(File):
    """CSV file class"""

    def write(self, data):
        """
        Write data on csv file

        :param data: data to write on csv file
        :return: None
        """
        with self.raw_data as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def read(self, **kargs):
        """
        Read csv format

        :return: csv file
        """
        with self.raw_data as file:
            reader = csv.reader(file, **kargs)
            return reader


class JsonFile(File):
    """JSON file class"""

    def write(self, data):
        """
        Write data on json file

        :param data: data to write on json file
        :return: None
        """
        with self.raw_data as file:
            json.dump(data, file, indent=4)

    def read(self, **kwargs):
        """
        Read json format

        :return: json file
        """
        with self.raw_data as file:
            return json.load(file, **kwargs)


class YamlFile(File):
    """YAML file class"""

    def write(self, data):
        """
        Write data on yaml file

        :param data: data to write on yaml file
        :return: None
        """
        with self.raw_data as file:
            yaml.dump(data, file)

    def read(self, **kargs):
        """
        Read yaml format

        :return: yaml file
        """
        with self.raw_data as file:
            return yaml.full_load(file)


class SQLliteConnection(Connection):
    """Connection sqlite class"""

    def connect(self):
        self.connection = sqlite3.connect(database=self.host)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()


class MSSQLConnection(Connection):
    """Connection microsoft sql class"""

    def connect(self):
        self.connection = pymssql.connect(self.host, self.username, self.password, self.database, port=self.port)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()


class MySQLConnection(Connection):
    """Connection mysql class"""

    def connect(self):
        self.connection = mdb.connect(self.host, self.username, self.password, self.database, port=self.port)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()


class PostgreSQLConnection(Connection):
    """Connection postgresql class"""

    def connect(self):
        self.connection = psycopg2.connect(
            self.host,
            self.username,
            self.password,
            database=self.database,
            port=self.port
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()


class DatabaseManager:
    """Database manager class for SQL connection"""

    def __init__(self, connection: Connection):
        """
        Database manager object for SQL connection

        :param connection: Connection based object
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


class FileManager:
    """File manager class for various readable file format"""

    def __init__(self, file: File):
        """
        File manager object for various readable file format

        :param file: file object
        """
        self.data = file


# endregion

# region Variables
DBTYPE = {
    'sqlite': SQLliteConnection,
    'mssql': MSSQLConnection,
    'mysql': MySQLConnection,
    'postgresql': PostgreSQLConnection
}


# endregion


# region Functions
def create_database_manager(dbtype, host=None, port=None, database=None, username=None, password=None):
    """
    Creates a DatabaseManager object

    :param dbtype: type of database connection
    :param host: server host name
    :param port: port on server
    :param database: name of database
    :param username: username of database connection
    :param password: password of username of database connection
    :return: DatabaseManager
    """
    # Create connection
    connection = DBTYPE[dbtype](host=host, port=port, database=database, username=username, password=password)
    return DatabaseManager(connection=connection)

# endregion
