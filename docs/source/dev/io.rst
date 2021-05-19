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
    :members:




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

File
****

The ``File`` is the class that the other ``*File`` classes are based on.
It contains only the ``file`` attribute, where the path of the file is saved during the creation of the object and two methods:
``read`` to read the contents of the file (must return a Dataset object) and write (accept a Dataset) and writes to the destination file.



.. autoclass:: pyreports.io.File
    :members:




Example ``File`` based class:

.. code-block:: python

    class CsvFile(File):
    """CSV file class"""

    def write(self, data):
        """
        Write data on csv file

        :param data: data to write on csv file
        :return: None
        """
        if not isinstance(data, tablib.Dataset):
            data = tablib.Dataset(data)
        with open(self.file, mode='w') as file:
            file.write(data.export('csv'))

    def read(self, **kwargs):
        """
        Read csv format

        :return: Dataset object
        """
        with open(self.file) as file:
            return tablib.Dataset().load(file, **kwargs)

Alias
*****

When creating a ``Connection`` or ``File`` class, if you want to use the ``manager`` function to create the returning ``*Manager`` object,
you need to create an alias. There are two dicts in the ``io`` module, which represent the aliases of these objects.
If you have created a new ``Connection`` class, you will need to enter your alias in the ``DBTYPE`` *dict* while for File-type classes,
enter it in the ``FILETYPE`` *dict*. Here is an example: ``'ods': ODSFile``



