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
      report:

input section
-------------

The report section must have a data **input**, which can be file, sql database or LDAP.

.. code-block:: yaml
   :caption: FileManager

    reports:
      report:
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
      report:
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
      report:
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

**output** is a *FileManager* object where save your report data.

.. attention::
   If *output* is null or absent, the output of data is *stdout*.

.. code-block:: yaml

    reports:
      report:
        # My input
        input:
          # ...
        output:
          manager: 'csv'
          filename: '/tmp/test_csv.csv'