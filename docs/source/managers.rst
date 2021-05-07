Managers
########

The manager objects are responsible for managing inputs or outputs. We can have three macro types of managers: *database*, *file* and *ldap*.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Work with managers
******************

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

.. code-block:: python

    import pyreports

    # DatabaseManager object
    sqllite_db = pyreports.manager('sqllite', database='/tmp/mydb.db')
    mssql_db = pyreports.manager('mssql', host='mysql1.local', database='test', username='dba', password='dba0000')
    mysql_db = pyreports.manager('mysql', host='mssql1.local', database='test', username='dba', password='dba0000')
    postgresql_db = pyreports.manager('postgresql', host='postgresql1.local', database='test', username='dba', password='dba0000')

    # FileManager object
    file = pyreports.manager('file', '/tmp/log.log')
    csv = pyreports.manager('csv', '/tmp/csv.csv')
    json = pyreports.manager('json', '/tmp/json.json')
    yaml = pyreports.manager('yaml', '/tmp/yaml.yaml')
    xlsx = pyreports.manager('xlsx', '/tmp/xlsx.xlsx')

    # LDAPManager object
    ldap = pyreports.manager('ldap', server='ldap.local', username='user', password='password', ssl=False, tls=True)
