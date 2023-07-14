Managers
########

The manager objects are responsible for managing inputs or outputs. We can have three macro types of managers: *database*, *file* and *ldap*.


.. toctree::




Type of managers
****************

Each type of manager is managed by micro types; Below is the complete list:

#. Database
    #. sqlite (SQLite)
    #. mssql (Microsoft SQL)
    #. mysql (MySQL or MariaDB)
    #. postgresql (PostgreSQL or EnterpriseDB)
#. File
    #. file (standard text file)
    #. log (log file)
    #. csv (Comma Separated Value file)
    #. json (JSON file)
    #. yaml (YAML file)
    #. xlsx (Microsoft Excel file)
#. LDAP
    #. ldap (Active Directory Server, OpenLDAP, FreeIPA, etc.)
#. NoSQL
    #. nosql (MongoDB, CouchDB, RavenDB, Redis, Neo4j, Cassandra, etc.)

.. note::
    The connection arguments of a ``DatabaseManager`` vary according to the type of database being accessed.
    Look at the manuals and documentation of each type of database to find out more.

.. code-block:: python

    import pyreports

    # DatabaseManager object
    sqlite_db = pyreports.manager('sqlite', database='/tmp/mydb.db')
    mssql_db = pyreports.manager('mssql', server='mssql1.local', database='test', user='dba', password='dba0000')
    mysql_db = pyreports.manager('mysql', host='mysql1.local', database='test', user='dba', password='dba0000')
    postgresql_db = pyreports.manager('postgresql', host='postgresql1.local', database='test', user='dba', password='dba0000')

    # FileManager object
    file = pyreports.manager('file', '/tmp/text.txt')
    log = pyreports.manager('log', '/tmp/log.log')
    csv = pyreports.manager('csv', '/tmp/csv.csv')
    json = pyreports.manager('json', '/tmp/json.json')
    yaml = pyreports.manager('yaml', '/tmp/yaml.yml')
    xlsx = pyreports.manager('xlsx', '/tmp/xlsx.xlsx')

    # LdapManager object
    ldap = pyreports.manager('ldap', server='ldap.local', username='user', password='password', ssl=False, tls=True)

    # NoSQLManager object (nosql api compliant https://nosqlapi.rtfd.io/)
    nosql = pyreports.manager('nosql', MongoDBConnection, host='mongo1.local', database='test', user='dba', password='dba0000')

Managers at work
****************

A Manager object corresponds to each type of manager. And each Manager object has its own methods for writing and reading data.

DatabaseManager
---------------

**Databasemanager** have eight methods that are used to reconnect, query, commit changes and much more. Let's see these methods in action below.

.. note::
    The following example will be done on a *mysql* type database, but it can be applied to any database because `DB-API 2.0 <https://www.python.org/dev/peps/pep-0249/>`_ is used.

.. code-block:: python

    import pyreports

    # DatabaseManager object
    mysql_db = pyreports.manager('mysql', host='mysql1.local', database='test', user='dba', password='dba0000')

    # Reconnect to database
    mysql_db.reconnect()

    # Query: CREATE
    mysql_db.execute("CREATE TABLE cars(id SERIAL PRIMARY KEY, name VARCHAR(255), price INT)")
    # Query: INSERT
    mysql_db.execute("INSERT INTO cars(name, price) VALUES('Audi', 52642)")
    # Query: INSERT (many)
    new_cars = [
      ('Alfa Romeo', 42123),
      ('Aston Martin', 78324),
      ('Ferrari', 129782),
    ]
    mysql_db.executemany("INSERT INTO cars(name, price) VALUES(%s, %s)", new_cars)
    # Commit changes
    mysql_db.commit()
    # Query: SELECT
    mysql_db.execute('SELECT * FROM cars')
    # View description and other info of last query
    print(mysql_db.description, mysql_db.lastrowid, mysql_db.rowcount)
    # Fetch all data
    print(mysql_db.fetchall())                  # Dataset object
    # Fetch first row
    print(mysql_db.fetchone())                  # Dataset object
    # Fetch select N row
    print(mysql_db.fetchmany(2))                # Dataset object
    print(mysql_db.fetchmany())                 # This is same fetchone() method
    # Query: SHOW
    mysql_db.execute("SHOW TABLES")
    print(mysql_db.fetchall())                  # Dataset object

    # Call store procedure
    mysql_db.callproc('select_cars')
    mysql_db.callproc('select_cars', ['Audi'])  # Call with args
    print(mysql_db.fetchall())                  # Dataset object

.. note::
    Whatever operation is done, the return value of the ``fetch*`` methods return `Dataset objects <https://tablib.readthedocs.io/en/stable/api/#dataset-object>`_.

FileManager
-----------

**FileManager** has two simple methods: *read* and *write*. Let's see how to use this manager.

.. code-block:: python

    import pyreports

    # FileManager object
    csv = pyreports.manager('csv', '/tmp/cars.csv')

    # Read data
    cars = csv.read()       # Dataset object

    # Write data
    cars.append(['Audi', 52642])
    csv.write(cars)

LdapManager
-----------

**LdapManager** is an object that allows you to interface and get data from a directory server via the ldap protocol.

.. code-block:: python

    import pyreports

    # LdapManager object
    ldap = pyreports.manager('ldap', server='ldap.local', username='user', password='password', ssl=False, tls=True)

    # Rebind connection
    ldap.rebind()

    # Query: get data
    # This is Dataset object
    users = ldap.query('DC=test,DC=local', '(&(objectClass=user)(objectCategory=person))', ['name', 'mail', 'phone'])
    if users:
        print(users)

    # Close connection
    ldap.unbind()

.. warning::
    *LdapManager* should only be used for inputs. An ldap manager has no write methods.

NoSQLManager
------------

**NoSQLManager** is an object that allows you to interface and get data from a NoSQL database server.

.. code-block:: python

    import pyreports

    # LdapManager object
    nosql = pyreports.manager('nosql', MongoDBConnection, host='mongo1.local', database='test', user='dba', password='dba0000')

    # Get data
    nosql.get('doc1')                   # Dataset object

    # Find data
    nosql.find('{"name": "Matteo"}')    # Dataset object

.. note::
    *NoSQLManager* object accept connection that must be compliant of `nosqlapi <https://nosqlapi.rtfd.io/>`_.