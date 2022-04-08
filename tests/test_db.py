import unittest
import pyreports
from tablib import Dataset
from unittest.mock import MagicMock, patch


class TestDBConnection(unittest.TestCase):

    def test_connection(self):
        # pyreports.io.Connection object
        self.assertRaises(TypeError, pyreports.io.Connection)

    def test_sqllite_connection(self):
        # Simulate pyreports.io.SQLliteConnection object
        conn = MagicMock()
        with patch(target='sqlite3.connect') as mock:
            # Test connect
            conn.connection = mock.return_value
            conn.cursor = conn.connection.cursor.return_value
            conn.connection.database = 'mydb.db'
            self.assertEqual(conn.connection.database, 'mydb.db')
            # Test close
            conn.cursor.close()

    def test_mysql_connection(self):
        # Simulate pyreports.io.MySQLConnection object
        conn = MagicMock()
        with patch(target='mysql.connector.connect') as mock:
            # Test connect
            conn.connection = mock.return_value
            conn.cursor = conn.connection.cursor.return_value
            conn.connection.host = 'mysqldb.local'
            conn.connection.database = 'mydb'
            conn.connection.username = 'username'
            conn.connection.password = 'password'
            conn.connection.port = 3306
            self.assertEqual(conn.connection.host, 'mysqldb.local')
            self.assertEqual(conn.connection.database, 'mydb')
            self.assertEqual(conn.connection.username, 'username')
            self.assertEqual(conn.connection.password, 'password')
            self.assertEqual(conn.connection.port, 3306)
            # Test close
            conn.cursor.close()

    def test_mssqldb_connection(self):
        # Simulate pyreports.io.MSSQLConnection object
        conn = MagicMock()
        with patch(target='pymssql.connect') as mock:
            # Test connect
            conn.connection = mock.return_value
            conn.cursor = conn.connection.cursor.return_value
            conn.connection.host = 'mssqldb.local'
            conn.connection.database = 'mydb'
            conn.connection.username = 'username'
            conn.connection.password = 'password'
            conn.connection.port = 1433
            self.assertEqual(conn.connection.host, 'mssqldb.local')
            self.assertEqual(conn.connection.database, 'mydb')
            self.assertEqual(conn.connection.username, 'username')
            self.assertEqual(conn.connection.password, 'password')
            self.assertEqual(conn.connection.port, 1433)
            # Test close
            conn.cursor.close()

    def test_postgresqldb_connection(self):
        # Simulate pyreports.io.PostgreSQLConnection object
        conn = MagicMock()
        with patch(target='psycopg2.connect') as mock:
            # Test connect
            conn.connection = mock.return_value
            conn.cursor = conn.connection.cursor.return_value
            conn.connection.host = 'postgresqldb.local'
            conn.connection.database = 'mydb'
            conn.connection.username = 'username'
            conn.connection.password = 'password'
            conn.connection.port = 5432
            self.assertEqual(conn.connection.host, 'postgresqldb.local')
            self.assertEqual(conn.connection.database, 'mydb')
            self.assertEqual(conn.connection.username, 'username')
            self.assertEqual(conn.connection.password, 'password')
            self.assertEqual(conn.connection.port, 5432)
            # Test close
            conn.cursor.close()


class TestDBManager(unittest.TestCase):

    conn = MagicMock()
    with patch(target='psycopg2.connect') as mock:
        conn.connection = mock.return_value
        conn.cursor = conn.connection.cursor.return_value
        conn.connection.host = 'postgresqldb.local'
        conn.connection.database = 'mydb'
        conn.connection.username = 'username'
        conn.connection.password = 'password'
        conn.connection.port = 5432

    def test_db_manager(self):
        # Test database manager
        db_manager = pyreports.io.DatabaseManager(connection=self.conn)
        self.assertIsInstance(db_manager, pyreports.io.DatabaseManager)
        # Test reconnect
        db_manager.reconnect()
        # Test SELECT query
        db_manager.execute('SELECT * from test')
        data = db_manager.fetchall()
        self.assertIsInstance(data, Dataset)
        # Test store procedure
        db_manager.callproc('myproc')
        data = db_manager.fetchone()
        self.assertIsInstance(data, Dataset)


class TestNoSQLManager(unittest.TestCase):

    conn = MagicMock()
    with patch(target='nosqlapi.Connection') as mock:
        conn.connection = mock.return_value
        conn.session = conn.connection.connect()
        conn.connection.host = 'mongodb.local'
        conn.connection.database = 'mydb'
        conn.connection.username = 'username'
        conn.connection.password = 'password'
        conn.connection.port = 27017

    def test_nosql_manager(self):
        # Test nosql database manager
        nosql_manager = pyreports.io.NoSQLManager(connection=self.conn)
        self.assertIsInstance(nosql_manager, pyreports.io.NoSQLManager)
        # Test get data
        data = nosql_manager.get('doc1')
        self.assertIsInstance(data, Dataset)
        # Test find data
        data = nosql_manager.find({"name": "Arthur"})
        self.assertIsInstance(data, Dataset)


class TestLDAPManager(unittest.TestCase):

    conn = MagicMock()
    with patch(target='ldap3.Server') as mock:
        conn.connector = mock.return_value
    with patch(target='ldap3.Connection') as mock:
        conn.bind = mock.return_value

    def test_bind(self):
        self.conn.bind.bind()
        self.conn.bind.unbind()

    def test_query(self):
        self.conn.bind.search('OU=test,DC=test,DC=local', 'objectCategory=person', ['name', 'sn', 'phone'])


if __name__ == '__main__':
    unittest.main()
