.. toctree::
   :maxdepth: 2
   :caption: Contents:

Command Line Interface
######################

*pyreports* has a command line interface which takes a configuration file in `YAML <https://yaml.org/>`_ format as an argument.


Command arguments
*****************

The only mandatory argument is the `YAML <https://yaml.org/>`_ language configuration file.

Optional arguments
------------------

Here are all the optional flags that the command line interface has.

+---------------+----------------------+
| flags         | description          |
+===============+======================+
| -v/--verbose  | Enable verbose mode  |
+---------------+----------------------+
| -e/--exclude  | Exclude reports      |
+---------------+----------------------+
| -V/--version  | Print version        |
+---------------+----------------------+
| -h/--help     | Print help           |
+---------------+----------------------+

Report configuration
********************

The *YAML* file representing your reports begins with a **reports** key.

.. code-block:: yaml

    reports:
        # ...


Each report you want to define is a **report** key inside *reports*.

.. code-block:: yaml

    # My reports collection
    reports:
    # My single report
    - report:

input section
-------------

The report section must have a data **input**, which can be file, sql database or LDAP.

.. code-block:: yaml
   :caption: FileManager

    reports:
    - report:
        # My input
        input:
          manager: 'log'
          filename: '/tmp/test_log.log'
          # Apache http log format
          params:
            pattern: '([(\d\.)]+) (.*) \[(.*?)\] (.*?) (\d+) (\d+) (.*?) (.*?) (\(.*?\))'
            headers: ['ip', 'user', 'date', 'req', 'ret', 'size', 'url', 'browser', 'host']

.. note::
   Only *log* type has a ``pattern`` params.


.. code-block:: yaml
   :caption: DatabaseManager

    reports:
    - report:
        # My input
        input:
          manager: 'mysql'
          source:
          # Connection parameters of my mysql database
            host: 'mysql1.local'
            database: 'cars'
            user: 'admin'
            password: 'dba0000'
          params:
            query: 'SELECT * FROM cars WHERE brand = %s AND color = %s'
            params: ['ford', 'red']

.. attention::
   For complete list of *source* parameters see the various python package for the providers databases.

.. code-block:: yaml
   :caption: LdapManager

    reports:
    - report:
        # My input
        input:
          manager: 'ldap'
          source:
          # Connection parameters of my ldap server
            server: 'ldap.local'
            username: 'user'
            password: 'password'
            ssl: False
            tls: True
          params:
            base_search: 'DC=test,DC=local'
            search_filter: '(&(objectClass=user)(objectCategory=person))'
            attributes: ['name', 'mail', 'phone']

output section
--------------

**output** is a *Manager* object where save your report data, is same of input data.

.. attention::
   If *output* is null or absent, the output of data is *stdout*.

.. code-block:: yaml
   :caption: FileManager

    reports:
    - report:
        # My input
        input:
          # ...
        output:
          manager: 'csv'
          filename: '/tmp/test_csv.csv'


.. code-block:: yaml
   :caption: DatabaseManager

    reports:
    - report:
        # My input
        input:
          # ...
        output:
          manager: 'mysql'
          source:
          # Connection parameters of my mysql database
            host: 'mysql1.local'
            database: 'cars'
            user: 'admin'
            password: 'dba0000'

other section
-------------

*report* section has multiple key/value.

.. code-block:: yaml

    reports:
    - report:
        # My input
        input:
          # ...
        output:
          # ...
        title: "One report"
        filters: ['string_filter', 42]
        map: |
          def map_func(integer):
              if isinstance(integer, int):
                  return str(integer)
        negation: true
        column: "column_name"
        count: True

.. warning::
   **map** section accept any python code. Specify only a function that accept only one argument and with name ``map_func``.

.. note::
   **filters** could accept also a function that accept only one argument and return a ``bool`` value.

mail settings
-------------

Reports can also be sent by email. Just specify the **mail** section.

.. code-block:: yaml

    reports:
    - report:
        # My input
        input:
          # ...
        output:
          # ...
        # Other sections
        mail:
          server: 'smtp.local'
          from: 'ARTHUR DENT <arthur.dent@hitchhikers.com>'
          to: 'ford.prefect@hitchhikers.com'
          cc: 'startiblast@hitchhikers.com'
          bcc: 'allmouse@hitchhikers.com'
          subject: 'New report mail'
          body: 'Report in attachment'
          auth: ['user', 'password']
          ssl: true
          headers: ['key', 'value']

.. warning::
   **mail** settings required **output** settings.

Report examples
***************

Here are some report configurations ranging from the case of reading from a database and writing to a file up to an LDAP server.

Database example
----------------

Below is an example of a report with data taken from a *mysql* database and save it into *csv* file.

.. code-block:: yaml

    reports:
    - report:
        title: 'Red ford machine'
        input:
          manager: 'mysql'
          source:
          # Connection parameters of my mysql database
            host: 'mysql1.local'
            database: 'cars'
            user: 'admin'
            password: 'dba0000'
          params:
            query: 'SELECT * FROM cars WHERE brand = %s AND color = %s'
            params: ['ford', 'red']
        # Filter km
        filters: [40000, 45000]
        output:
          manager: 'csv'
          filename: '/tmp/car_csv.csv'

LDAP example
------------

Reports of users who have passwords without expiration by saving it in an *excel* file and sending it by email.

.. code-block:: yaml

    reports:
    - report:
        title: 'Users who have passwords without expiration'
        input:
          manager: 'ldap'
          source:
           # Connection parameters of my ldap server
           server: 'ldap.local'
            username: 'user'
            password: 'password'
            ssl: False
            tls: True
          params:
            base_search: 'DC=test,DC=local'
            search_filter: '(&(objectCategory=person)(objectClass=user)(!userAccountControl:1.2.840.113556.1.4.803:=65536))'
            attributes: ['cn', 'mail', 'phone']
        # Append prefix number on phone number
        map: |
            def map_func(phone):
               if phone.startswith('33'):
                  return '+39' + phone
        output:
          manager: 'xlsx'
          filename: '/tmp/users.xlsx'
        mail:
          server: 'smtp.local'
          from: 'ARTHUR DENT <arthur.dent@hitchhikers.com'
          to: 'ford.prefect@hitchhikers.com'

Two report examples
-------------------

Combine latest report examples into one configuration file.

.. code-block:: yaml

    reports:
    - report:
        title: 'Red ford machine'
        input:
          manager: 'mysql'
          source:
          # Connection parameters of my mysql database
            host: 'mysql1.local'
            database: 'cars'
            user: 'admin'
            password: 'dba0000'
          params:
            query: 'SELECT * FROM cars WHERE brand = %s AND color = %s'
            params: ['ford', 'red']
        # Filter km
        filters: [40000, 45000]
        output:
          manager: 'csv'
          filename: '/tmp/car_csv.csv'
    - report:
        title: 'Users who have passwords without expiration'
        input:
          manager: 'ldap'
          source:
          # Connection parameters of my ldap server
            server: 'ldap.local'
            username: 'user'
            password: 'password'
            ssl: False
            tls: True
          params:
            base_search: 'DC=test,DC=local'
            search_filter: '(&(objectCategory=person)(objectClass=user)(!userAccountControl:1.2.840.113556.1.4.803:=65536))'
            attributes: ['cn', 'mail', 'phone']
        # Append prefix number on phone number
        map: |
            def map_func(phone):
               if phone.startswith('33'):
                  return '+39' + phone
        output:
          manager: 'xlsx'
          filename: '/tmp/users.xlsx'
        mail:
          server: 'smtp.local'
          from: 'ARTHUR DENT <arthur.dent@hitchhikers.com'
          to: 'ford.prefect@hitchhikers.com'
