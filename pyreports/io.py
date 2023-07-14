#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# io -- pyreports
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

"""Contains all input management."""

# region Imports
import sqlite3
from typing import Union, List
import nosqlapi
import pymssql
import mysql.connector as mdb
import psycopg2
import tablib
import ldap3
import re
from nosqlapi import Manager as APIManager
from nosqlapi import Connection as APIConnection
from abc import ABC, abstractmethod


# endregion


# region Classes
class Connection(ABC):
    """Connection base class"""

    def __init__(self, *args, **kwargs):
        """Connection base object."""

        self.connection = None
        self.cursor = None
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def __bool__(self):
        return True if self.connection and self.cursor else False

    def __repr__(self):
        return f"<{self.__class__.__name__} object, connection={self.connection}, cursor={self.cursor}>"

    def __iter__(self):
        if self.cursor:
            return (e for e in self.cursor)
        else:
            return iter([])


class File(ABC):
    """File base class"""

    def __init__(self, filename):
        """File base object

        :param filename: file path
        """
        self.file = filename

    @abstractmethod
    def write(self, data):
        """Write data on file

        :param data: data to write on file
        :return: None
        """
        pass

    @abstractmethod
    def read(self, **kwargs):
        """Read with format

        :return: Dataset object
        """
        pass

    def __bool__(self):
        return True if self.file else False

    def __repr__(self):
        return f"<{self.__class__.__name__} object, file={self.file}>"

    def __iter__(self):
        with open(self.file) as file:
            for line in file:
                yield line


class Manager(ABC):
    """Manager base class"""
    pass


class TextFile(File):
    """Text file class"""

    def write(self, data):
        """Write data on file

        :param data: data to write on file
        :return: None
        """
        if not isinstance(data, tablib.Dataset):
            data = tablib.Dataset(data)
        with open(self.file, mode='w') as file:
            file.write('\n'.join(str(line) for row in data for line in row))

    def read(self, **kwargs):
        """Read with format

        :return: Dataset object
        """
        data = tablib.Dataset(**kwargs)
        with open(self.file) as file:
            for line in file:
                data.append([line.strip('\n')])
        return data


class LogFile(File):
    """Log file class"""

    def write(self, data):
        """Write data on file

        :param data: data to write on file
        :return: None
        """
        if not isinstance(data, tablib.Dataset):
            data = tablib.Dataset(*data)
        with open(self.file, mode='w') as file:
            file.write('\n'.join([' '.join(row).strip('\n') for row in data]))

    def read(self, pattern=r'(.*\n|.*$)', **kwargs):
        """Read with format

        :param pattern: regular expression pattern
        :return: Dataset object
        """
        data = tablib.Dataset(**kwargs)
        with open(self.file) as file:
            for line in file:
                result = re.findall(pattern, line)
                if result:
                    if isinstance(result[0], (tuple, list)):
                        data.append(*result)
                    else:
                        data.append([result])
        return data


class CsvFile(File):
    """CSV file class"""

    def write(self, data):
        """Write data on csv file

        :param data: data to write on csv file
        :return: None
        """
        if not isinstance(data, tablib.Dataset):
            data = tablib.Dataset(data)
        with open(self.file, mode='w') as file:
            file.write(data.export('csv'))

    def read(self, **kwargs):
        """Read csv format

        :return: Dataset object
        """
        with open(self.file) as file:
            return tablib.Dataset().load(file, **kwargs)


class JsonFile(File):
    """JSON file class"""

    def write(self, data):
        """Write data on json file

        :param data: data to write on json file
        :return: None
        """
        if not isinstance(data, tablib.Dataset):
            data = tablib.Dataset(data)
        with open(self.file, mode='w') as file:
            file.write(data.export('json'))

    def read(self, **kwargs):
        """Read json format

        :return: Dataset object
        """
        with open(self.file) as file:
            return tablib.Dataset().load(file, **kwargs)


class YamlFile(File):
    """YAML file class"""

    def write(self, data):
        """Write data on yaml file

        :param data: data to write on yaml file
        :return: None
        """
        if not isinstance(data, tablib.Dataset):
            data = tablib.Dataset(data)
        with open(self.file, mode='w') as file:
            file.write(data.export('yaml'))

    def read(self, **kwargs):
        """Read yaml format

        :return: Dataset object
        """
        with open(self.file) as file:
            return tablib.Dataset().load(file, **kwargs)


class ExcelFile(File):
    """Excel file class"""

    def write(self, data):
        """Write data on xlsx file

        :param data: data to write on yaml file
        :return: None
        """
        if not isinstance(data, tablib.Dataset):
            data = tablib.Dataset(data)
        with open(self.file, mode='wb') as file:
            file.write(data.export('xlsx'))

    def read(self, **kwargs):
        """Read xlsx format

        :return: Dataset object
        """
        with open(self.file, 'rb') as file:
            return tablib.import_set(file, **kwargs)


class SQLiteConnection(Connection):
    """Connection sqlite class"""

    def connect(self):
        self.connection = sqlite3.connect(*self.args, **self.kwargs)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()


class MSSQLConnection(Connection):
    """Connection microsoft sql class"""

    def connect(self):
        self.connection = pymssql.connect(*self.args, **self.kwargs)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()


class MySQLConnection(Connection):
    """Connection mysql class"""

    def connect(self):
        self.connection = mdb.connect(*self.args, **self.kwargs)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()


class PostgreSQLConnection(Connection):
    """Connection postgresql class"""

    def connect(self):
        self.connection = psycopg2.connect(*self.args, **self.kwargs)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
        self.cursor.close()


class DatabaseManager(Manager):
    """Database manager class for SQL connection"""

    def __init__(self, connection: Connection):
        """Database manager object for SQL connection

        :param connection: Connection based object
        """
        self.type = 'sql'
        self.connector = connection
        # Connect database
        self.connector.connect()
        # Set description
        self.description = None
        self.data = None
        # Row properties
        self.lastrowid = None
        self.rowcount = 0

    def __repr__(self):
        """Representation of DatabaseManager object

        :return: string
        """
        ret = f"<{self.__class__.__name__} object, "
        ret += f"connection={self.connector.__class__.__name__}>"
        return ret

    def __iter__(self):
        if self.connector.cursor:
            return (e for e in self.connector.cursor)
        else:
            return iter([])

    def reconnect(self):
        """Close and start connection

        :return: None
        """
        # Close connection
        self.connector.close()
        # Start connection, again
        self.connector.connect()

    def execute(self, query, params=None):
        """Execute query on database cursor

        :param query: SQL query language
        :param params: parameters of the query
        :return: None
        """
        if params:
            self.connector.cursor.execute(query, params)
        else:
            self.connector.cursor.execute(query)
        # Set last row id
        self.lastrowid = self.connector.cursor.lastrowid
        # Set row cont
        self.rowcount = self.connector.cursor.rowcount
        # Set description
        self.description = self.connector.cursor.description

    def executemany(self, query, params):
        """Execute query on database cursor with many parameters

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
        # Set description
        self.description = self.connector.cursor.description

    def fetchall(self) -> tablib.Dataset:
        """Fetches all (or all remaining) rows of a query result set

        :return: Dataset object
        """
        header = [field[0] for field in self.description]
        self.data = tablib.Dataset(headers=header)
        for row in self.connector.cursor.fetchall():
            self.data.append(list(row))
        return self.data

    def fetchone(self) -> tablib.Dataset:
        """Retrieves the next row of a query result set

        :return: Dataset object
        """
        header = [field[0] for field in self.description]
        self.data = tablib.Dataset(list(self.connector.cursor.fetchone()), headers=header)
        return self.data

    def fetchmany(self, size=1) -> tablib.Dataset:
        """Fetches the next set of rows of a query result

        :param size: the number of rows returned
        :return: Dataset object
        """
        header = [field[0] for field in self.description]
        self.data = tablib.Dataset(headers=header)
        for row in self.connector.cursor.fetchmany(size):
            self.data.append(list(row))
        return self.data

    def callproc(self, proc_name, params=None) -> tablib.Dataset:
        """Calls the stored procedure named

        :param proc_name: name of store procedure
        :param params: sequence of parameters must contain one entry for each argument that the procedure expects
        :return: Dataset object
        """
        if params is None:
            params = []
        header = [field[0] for field in self.description]
        self.data = tablib.Dataset(headers=header)
        for row in self.connector.cursor.callproc(proc_name, params):
            self.data.append(list(row))
        return self.data

    def commit(self):
        """This method sends a COMMIT statement to the server

        :return: None
        """
        self.connector.connection.commit()


class NoSQLManager(Manager, APIManager):
    """Database manager class for NOSQL connection"""

    def __init__(self, connection: APIConnection, *args, **kwargs):
        APIManager.__init__(self, connection, *args, **kwargs)
        self.type = 'nosql'

    @staticmethod
    def _response_to_dataset(
            obj: Union[List[tuple], List[list], dict, nosqlapi.Response]
    ) -> tablib.Dataset:
        """Transform receive data into Dataset object"""
        data = tablib.Dataset()
        if isinstance(obj, (list, tuple)):
            data = tablib.Dataset([row for row in obj])
        elif isinstance(obj, dict):
            data = tablib.Dataset([obj[key] for key in obj], headers=list(obj.keys()))
        elif isinstance(obj, nosqlapi.Response):
            if isinstance(obj.data, (list, tuple)):
                data = tablib.Dataset([row for row in obj.data])
            elif isinstance(obj.data, dict):
                data = tablib.Dataset([obj.data[key] for key in obj], headers=list(obj.data.keys()))
        else:
            data.append(obj)

        return data

    def get(self, *args, **kwargs) -> tablib.Dataset:
        """Get data from database session"""
        return self._response_to_dataset(self.session.get(*args, **kwargs))

    def find(self, *args, **kwargs) -> tablib.Dataset:
        """Find data from database session"""
        return self._response_to_dataset(self.session.find(*args, **kwargs))


class FileManager(Manager):
    """File manager class for various readable file format"""

    def __init__(self, file: File):
        """File manager object for various readable file format

        :param file: file object
        """
        self.type = 'file'
        self.data = file

    def __repr__(self):
        """Representation of FileManager object

        :return: string
        """
        return f"<{self.__class__.__name__} object, file={self.data.file}>"

    def __iter__(self):
        with open(self.data.file) as file:
            for line in file:
                yield line

    def write(self, data):
        """Write data on file

        :param data: data to write on file
        :return: None
        """
        self.data.write(data)

    def read(self, pattern=None, **kwargs) -> tablib.Dataset:
        """Read file

        :return: Dataset object
        """
        if pattern:
            data = self.data.read(pattern=pattern, **kwargs)
        else:
            data = self.data.read(**kwargs)
        return data


class LdapManager(Manager):
    """LDAP manager class"""

    def __init__(self, server, username, password, ssl=False, tls=True):
        """LDAP manager object

        :param server: fqdn server name or ip address
        :param username: username for bind operation
        :param password: password of the username used for bind operation
        :param ssl: disable or enable SSL. Default is False.
        :param tls: disable or enable TLS. Default is True.
        """
        self.type = 'ldap'
        # Check ssl connection
        port = 636 if ssl else 389
        self.connector = ldap3.Server(server,
                                      get_info=ldap3.ALL,
                                      port=port,
                                      use_ssl=ssl)
        # Check tls connection
        self.auto_bind = ldap3.AUTO_BIND_TLS_BEFORE_BIND if tls else ldap3.AUTO_BIND_NONE
        # Create a bind connection with user and password
        self.bind = ldap3.Connection(self.connector, user=f'{username}', password=f'{password}',
                                     auto_bind=self.auto_bind, raise_exceptions=True)
        self.bind.bind()

    def __repr__(self):
        """Representation of LdapManager object

        :return: string
        """
        obj_repr = f"<{self.__class__.__name__} object, "
        obj_repr += f"server={self.connector.host}, "
        obj_repr += f"ssl={self.connector.ssl}, tls={self.connector.tls}>"
        return obj_repr

    def rebind(self, username, password):
        """Re-bind with specified username and password

        :param username: username for bind operation
        :param password: password of the username used for bind operation
        :return: None
        """
        # Disconnect LDAP server
        self.bind.unbind()
        self.bind = ldap3.Connection(self.connector, user=f'{username}', password=f'{password}',
                                     auto_bind=self.auto_bind, raise_exceptions=True)
        self.bind.bind()

    def unbind(self):
        """Unbind LDAP connection

        :return: None
        """
        self.bind.unbind()

    def query(self, base_search, search_filter, attributes) -> tablib.Dataset:
        """Search LDAP element on subtree base search directory

        :param base_search: distinguishedName of LDAP base search
        :param search_filter: LDAP query language
        :param attributes: list of returning LDAP attributes
        :return: Dataset object
        """
        if self.bind.search(search_base=base_search, search_filter=f'{search_filter}', attributes=attributes,
                            search_scope=ldap3.SUBTREE):
            # Build Dataset
            data = tablib.Dataset()
            data.headers = attributes
            for result in self.bind.response:
                if result.get('attributes'):
                    row = list()
                    for index, _ in enumerate(attributes):
                        row.append(result.get('attributes').get(attributes[index]))
                    data.append(row)
            # Return object
            return data


# endregion


# region Variables
DBTYPE = {
    'sqlite': SQLiteConnection,
    'mssql': MSSQLConnection,
    'mysql': MySQLConnection,
    'postgresql': PostgreSQLConnection
}

FILETYPE = {
    'file': TextFile,
    'log': LogFile,
    'csv': CsvFile,
    'json': JsonFile,
    'yaml': YamlFile,
    'xlsx': ExcelFile,
}

READABLE_MANAGER = ('FileManager', 'DatabaseManager', 'LdapManager', 'NoSQLManager')

WRITABLE_MANAGER = ('FileManager', 'DatabaseManager', 'NoSQLManager')


# endregion


# region Functions
def create_database_manager(dbtype, *args, **kwargs):
    """Creates a DatabaseManager object

    :param dbtype: type of database connection
    :return: DatabaseManager
    """
    # Create DatabaseManager object
    connection = DBTYPE[dbtype](*args, **kwargs)
    return DatabaseManager(connection=connection)


def create_file_manager(filetype, filename):
    """Creates a FileManager object

    :param filetype: type of file
    :param filename: path of file
    :return: FileManager
    """
    # Create FileManager object
    file = FILETYPE[filetype](filename=filename)
    return FileManager(file=file)


def create_ldap_manager(server, username, password, ssl=False, tls=True):
    """Creates a LdapManager object

    :param server: fqdn server name or ip address
    :param username: username for bind operation
    :param password: password of the username used for bind operation
    :param ssl: disable or enable SSL. Default is False.
    :param tls: disable or enable TLS. Default is True.
    """
    # Create LdapManager object
    return LdapManager(server, username, password, ssl=ssl, tls=tls)


def create_nosql_manager(connection, *args, **kwargs):
    """Creates a NoSQLManager object

    :param connection: Connection object
    :return: NoSQLManager
    """
    # Check if connection class is API compliant with nosqlapi
    if not hasattr(connection, 'connect'):
        raise nosqlapi.ConnectError('the Connection class is not API compliant. See https://nosqlapi.rtfd.io/')
    # Create NoSQLManager object
    return NoSQLManager(connection=connection, *args, **kwargs)


def manager(datatype, *args, **kwargs):
    """Creates manager object based on datatype

    :param datatype: type of manager
    :param args: various positional arguments
    :param kwargs: various keyword arguments
    :return: Manager object
    """
    # Choose manager type
    if datatype in DBTYPE:
        return create_database_manager(datatype, *args, **kwargs)
    elif datatype in FILETYPE:
        return create_file_manager(datatype, *args, **kwargs)
    elif datatype == 'ldap':
        return create_ldap_manager(*args, **kwargs)
    elif datatype == 'nosql':
        connection = kwargs.get('connection') or args[0]
        nargs = args[1:]
        try:
            kwargs.pop('connection')
        except KeyError:
            pass
        return create_nosql_manager(connection, *nargs, **kwargs)
    else:
        raise ValueError(f"data type {datatype} doesn't exists!")

# endregion
