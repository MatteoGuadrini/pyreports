import unittest
import reports
from tablib import Dataset
from unittest.mock import MagicMock


class TestDB(unittest.TestCase):

    def test_connection(self):
        # Simulate reports.io.Connection object
        conn = reports.io.Connection()
        self.assertIsInstance(conn, reports.io.Connection)



if __name__ == '__main__':
    unittest.main()
