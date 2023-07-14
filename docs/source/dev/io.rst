.. toctree::

io
##

In this section, you will find information on how to add new types of ``*Connection`` objects, ``*File`` objects, or ``*Manager`` objects.

Connection
**********

Each ``*Connection`` object inherits from the abstract ``Connection`` class, which forces each type of connection object to
accept these arguments when creating the object:

- ``args``, various positional arguments
- ``kwargs``, various keyword arguments

Besides this, the class must have a ``connect`` and a ``close`` method, respectively to connect to the database and one to close the connection,
respectively.


.. literalinclude:: ../../../pyreports/io.py
    :language: python
    :pyobject: Connection


Example ``Connection`` based class:


.. literalinclude:: ../../../pyreports/io.py
    :language: python
    :pyobject: SQLiteConnection

.. warning::
    All connections are `DBAPI 2.0 <https://www.python.org/dev/peps/pep-0249/>`_ compliant. If you need to create your own, it must adhere to these APIs.

File
****

The ``File`` is the abstract class that the other ``*File`` classes are based on.
It contains only the ``file`` attribute, where the path of the file is saved during the creation of the object and two methods:
``read`` to read the contents of the file (must return a Dataset object) and ``write`` (accept a Dataset) and writes to the destination file.



.. literalinclude:: ../../../pyreports/io.py
    :language: python
    :pyobject: File




Example ``File`` based class:

.. literalinclude:: ../../../pyreports/io.py
    :language: python
    :pyobject: CsvFile

Alias
*****

When creating a ``Connection`` or ``File`` class, if you want to use the ``manager`` function to create the returning ``*Manager`` object,
you need to create an alias. There are two dicts in the ``io`` module, which represent the aliases of these objects.
If you have created a new ``Connection`` class, you will need to enter your alias in the ``DBTYPE`` *dict* while for File-type classes,
enter it in the ``FILETYPE`` *dict*. Here is an example: ``'ods': ODSFile``



Manager
*******

Managers are classes that represent an input and output manager. For example, the ``DatabaseManager`` class accepts a
``Connection`` object and implements methods on these types of objects representing database connections.



.. literalinclude:: ../../../pyreports/io.py
    :language: python
    :pyobject: DatabaseManager


Manager function
----------------

Each ``*Manager`` class has associated a function of type ``create_<type of manager>_manager(*args, **kwargs)``.
This function will then be used by the ``manager`` function to create the corresponding ``*Manager`` object based on its alias.

For example, the ``DatabaseManager`` class has associated the ``create_database_manager`` function which will be called by the
``manager`` function to create the object based on the type of alias passed.



.. literalinclude:: ../../../pyreports/io.py
    :language: python
    :pyobject: manager



.. literalinclude:: ../../../pyreports/io.py
    :language: python
    :pyobject: create_database_manager

Example
*******

Here we will see how to create your own ``*Connection`` class to access a specific database.

.. code-block:: python

    import pyreports
    import DB2

    # class for connect DB2 database
    class DB2Connection(pyreports.io.Connection):

        def connect(self):
            self.connection = DB2.connect(*self.args, **self.kwargs)
            self.cursor = self.connection

        def close(self):
            self.connection.close()
            self.cursor.close()

    # Create an alias for DB2Connection object
    pyreports.io.DBTYPE['db2'] = DB2Connection

    # Create my DatabaseManager object
    mydb2 = pyreports.manager('db2', dsn='sample', uid='db2inst1', pwd='ibmdb2')
