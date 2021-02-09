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
import pymongo
import cloudant

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


class SQLliteConnection(Connection):
    """Connection sqlite class"""

    def connect(self):
        self.connection = sqlite3.connect(database=self.host)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()


class MSSQLConnection(Connection):
    """Connection microsoft sql class"""

    def connect(self):
        self.connection = pymssql.connect(self.host, self.username, self.password, self.database, port=self.port)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()


class MySQLConnection(Connection):
    """Connection mysql class"""

    def connect(self):
        self.connection = mdb.connect(self.host, self.username, self.password, self.database, port=self.port)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()


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


class MongoDBConnection(Connection):
    """Connection mongodb class"""

    def connect(self):
        self.connection = pymongo.MongoClient(
            self.host,
            username=self.username,
            password=self.password,
            authSource=self.database,
            authMechanism='SCRAM-SHA-1',
            port=self.port
        )
        self.cursor = self.connection

    def close(self):
        self.connection = None


class CouchDBConnection(Connection):
    """Connection couchdb class"""

    def connect(self):
        self.connection = cloudant.CouchDB(
            self.username,
            self.password,
            url=self.host,
            connect=True,
            auto_renew=True,
            port=self.port
        )
        self.cursor = self.connection

    def close(self):
        self.connection = None

# endregion
