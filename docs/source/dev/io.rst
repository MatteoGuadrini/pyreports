.. toctree::

io
##

In this section, you will find information on how to add new types of ``*Connection`` objects, ``*File`` objects, or ``*Manager`` objects.

Connection
**********

Each ``*Connection`` object inherits from the abstract ``Connection`` class, which forces each type of connection object to
accept these arguments when creating the object:

- ``host``, *hostname* of the machine where the database is hosted
- ``port``, *port* number of database server
- ``database``, *database* name
- ``username``, *username* who has access permissions
- ``password``, *password* of the *username* specified

Besides this, the class must have a ``connect`` and a ``close`` method, respectively to connect to the database and one to close the connection,
respectively.

.. note::
    Each argument to the ``__init__`` method defaults to ``None`` and saves the value in the instance.

.. autoclass:: pyreports.io.Connection
    :noindex:

Example ``Connection`` based class:

.. code-block:: python

    class SQLliteConnection(Connection):
        """Connection sqlite class"""

        def connect(self):
            self.connection = sqlite3.connect(database=self.database)
            self.cursor = self.connection.cursor()

        def close(self):
            self.connection.close()
            self.cursor.close()
