pyreports example
#################

Example scripts using ``pyreports`` module.

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Basic features
**************

In this example, we extract the data from a mysql database, filter it by error code and finally export it to a csv.

.. code-block:: python

    import pyreports

    # Select source: this is a DatabaseManager object
    mydb = pyreports.manager('mysql', host='mysql1.local', database='login_users', username='dba', password='dba0000')

    # Get data
    mydb.execute('SELECT * FROM site_login')
    site_login = mydb.fetchall()                    # return Dataset object

    # Filter data
    error_login = pyreports.Executor(site_login)    # accept Dataset object
    error_login.filter([400, 401, 403, 404, 500])

    # Save report: this is a FileManager object
    output = pyreports.manager('csv', '/home/report/error_login.csv')
    output.write(error_login.get_data())


.. note::
    A reflection on this example could be: "Why don't I apply the filter directly in the SQL syntax?"
    The answer is simple. The advantage of using an *Executor* object is that from general data I can filter or modify
    (*map* function or with my custom function) without affecting the original Dataset. So much so that I could do several
    different Executors, process them and then re-merge them into a single Executor, which would be difficult to do with SQL syntax.


Work with managers
------------------

The manager objects are responsible for managing inputs or outputs. We can have three macro types of managers: *database*, *file* and *ldap*.

Each type of manager is managed by micro types; Below is the complete list:

#. Database
    #. sqllite (SQLlite)
    #. mssql (Microsoft SQL)
    #. mysql (MySQL or MariaDB)
    #. postgresql (PostgreSQL or EnterpriseDB)
#. File
    #. file (standard text file or log)
    #. csv (Comma Separated Value file)
    #. json (JSON file)
    #. yaml (YAML file)
    #. xlsx (Microsoft Excel file)
#. LDAP
    #. ldap (Active Directory Server, OpenLDAP, FreeIPA, etc.)

.. warning::
    LDAP manager should only be used for inputs. An ldap manager has no write methods.

. code-block:: python

    import pyreports

    # DatabaseManager object
    sqllite_db = pyreports.manager('sqllite', database='/tmp/mydb.db')
    mssql_db = pyreports.manager('mssql', host='mysql1.local', database='test', username='dba', password='dba0000')
    mysql_db = pyreports.manager('mysql', host='mssql1.local', database='test', username='dba', password='dba0000')
    postgresql_db = pyreports.manager('postgresql', host='postgresql1.local', database='test', username='dba', password='dba0000')