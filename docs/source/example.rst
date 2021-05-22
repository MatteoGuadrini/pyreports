pyreports example
#################

Example scripts using ``pyreports`` module.

.. toctree::




Basic usage
***********

In this section you will find examples that represent the entire reporting workflow, relying on the *\*Manager* objects as input and output, and the *Executor* object for the process part.

Database to file
----------------

In this example, we extract the data from a mysql database, filter it by error code and finally export it to a csv.

.. code-block:: python

    import pyreports

    # INPUT

    # Select source: this is a DatabaseManager object
    mydb = pyreports.manager('mysql', host='mysql1.local', database='login_users', user='dba', password='dba0000')

    # Get data
    mydb.execute('SELECT * FROM site_login')
    site_login = mydb.fetchall()                    # return Dataset object

    # PROCESS

    # Filter data
    error_login = pyreports.Executor(site_login)    # accept Dataset object
    error_login.filter([400, 401, 403, 404, 500])

    # OUTPUT

    # Save report: this is a FileManager object
    output = pyreports.manager('csv', '/home/report/error_login.csv')
    output.write(error_login.get_data())


.. note::
    A reflection on this example could be: "Why don't I apply the filter directly in the SQL syntax?"
    The answer is simple. The advantage of using an *Executor* object is that from general data I can filter or modify
    (*map* function or with my custom function) without affecting the original Dataset. So much so that I could do several
    different Executors, process them and then re-merge them into a single Executor, which would be difficult to do with SQL syntax.

File to Database
----------------

In this example I have a json file as input, received from a web server, I process it and write to the database.

.. code-block:: python

    import pyreports

    # INPUT

    # Return json from GET request on web server: this is a FileManager object
    web_server_result = pyreports.manager('json', '/home/report/users.json')
    # Get data
    users = web_server_result.read()                            # return Dataset object

    # PROCESS

    # Filter data
    user_int = pyreports.Executor(users)                        # accept Dataset object
    user_int.filter(key=lambda record: if record == 'INTERNAL') # My filter is a function
    user_ext = pyreports.Executor(users)
    user_ext.filter(key=lambda record: if record == 'EXTERNAL')

    # OUTPUT

    # Save report: this is a DatabaseManager object
    mydb = pyreports.manager('mysql', host='mysql1.local', database='users', user='dba', password='dba0000')

    # Write to database
    mydb.executemany("INSERT INTO internal_users(name, surname, employeeType) VALUES(%s, %s, %s)", list(user_int))
    mydb.executemany("INSERT INTO external_users(name, surname, employeeType) VALUES(%s, %s, %s)", list(user_ext))
    mydb.commit()


Combine inputs
--------------

In this example, we will take two different inputs, and combine them to export an excel file containing the data processing of the two sources.

.. code-block:: python

    import pyreports

    # INPUT

    # Config Unix application file: this is a FileManager object
    config_file = pyreports.manager('yaml', '/home/myapp.yml')
    # Console admin: this is a DatabaseManager object
    mydb = pyreports.manager('mssql', server='mssql1.local', database='admins', user='sa', password='sa0000')
    # Get data
    admin_app = config_file.read()                  # return Dataset object: three column (name, shell, login)
    mydb.execute('SELECT * FROM console_admins')
    admins = mydb.fetchall()                        # return Dataset object: three column (name, shell, login)

    # PROCESS

    # Filter data
    all_console_admins = pyreports.Executor(admins) # accept Dataset object
    all_console_admins.filter(config_file['shell']) # filter by shells

    # OUTPUT

    # Save report: this is a FileManager object
    output = pyreports.manager('xlsx', '/home/report/all_admins.xlsx')
    output.write(all_console_admins.get_data())

Simple report
-------------

In this example, we use a Report type object to create and filter the data through a function and save it in a csv file, printing the number of lines in total.

.. code-block:: python

    import pyreports

    OFFICE_FILTER = 'Customer'

    # Function: filter by office
    def filter_by_office(value):
        if value == OFFICE_FILTER:
            return True

    # Connect to database
    mydb = pyreports.manager('postgresql', host='pssql1.local', database='users', user='admin', password='pwd0000')
    mydb.execute('SELECT * FROM employees')
    all_employees = mydb.fetchall()
    # Output to csv
    output = pyreports.manager('csv', f'/home/report/office_{OFFICE_FILTER}.csv')
    # All customer employees: Report object
    one_office = pyreports.Report(all_employees,
                                 filters=filter_by_office,
                                 title=f'All employees in {OFFICE_FILTER}',
                                 count=True,
                                 output=output)
    # Run and save report
    one_office.export()
    print(one_office.count)     # Row count


Advanced usage
**************

From here on, the examples will be a bit more complex; we will process the data in order to modify it, filter it,
combine it and merge it before exporting or parsing it in another object.

Report apache log
-----------------

In this example we will analyze and capture parts of a web server log. For each error code present in the log, we will
create a report that will be inserted in a book, where each sheet will contain the details of the error code.
In the last sheet, there will be an element counter for every single error present in the report.

.. code-block:: python

    import pyreports
    import tablib
    import re

    # Get apache log data: this is a FileManager object
    apache_log = pyreports.manager('file', '/var/log/httpd/error.log').read()
    # apache log format: regex
    regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) - "(.*?)" "(.*?)"'

    # Function than receive Dataset and return a new Dataset
    def format_dataset_log(data_input):
        data = tablib.Dataset(headers=['ip', 'date', 'operation', 'code', 'client'])
        for row in data_input:
            log_parts = re.match(regex, row[0]).groups()
            new_row = list(log_parts[:4])
            new_row.append(log_parts[5])
            data.append(new_row)
        return data

    # Create a collection of Report objects
    all_apache_error = pyreports.ReportBook(title='Apache error on my site')

    # Create a Report object based on error code
    apache_error_log = format_dataset_log(apache_log)
    all_error = set(apache_error_log['code'])
    for code in all_error:
        all_apache_error.add(pyreports.Report(apache_error_log, filters=[code], title=f'Error {code}'))

    # Count all error code
    counter = pyreports.counter(apache_error_log, 'code')
    # Append new Report on ReportBook with error code counters
    error_counter = tablib.Dataset(counter.values(), headers=counter)
    all_apache_error.add(pyreports.Report(error_counter))

    # Save ReportBook on Excel
    all_apache_error.export('/home/report/apache_log_error_code.xlsx')

We now have a script that parses and breaks an apache httpd log file by error code.

Report e-commerce data
----------------------

In this example, we combine data from different e-commerce databases.
In addition, we will create two reports: one for the sales, the other for the warehouse.
Then once saved, we will create an additional report that combines both of the previous ones.

.. code-block:: python

    import pyreports

    # Get data from database: a DatabaseManager object
    mydb = pyreports.manager('postgresql', host='pssql1.local', database='ecommerce', user='reader', password='pwd0000')
    mydb.execute('SELECT * FROM sales')
    sales = mydb.fetchall()
    mydb.execute('SELECT * FROM warehouse')
    warehouse = mydb.fetchall()

    # filters
    household = ['plates', 'glass', 'fork']
    clothes = ['shorts', 'tshirt', 'socks']

    # Create sales Report objects
    sales_by_household= pyreports.Report(sales, filter=household, title='household sold items')
    sales_by_clothes = pyreports.Report(sales, filter=clothes, title='clothes sold items')

    # Create warehouse Report objects
    warehouse_by_household= pyreports.Report(warehouse, filter=household, title='household items in warehouse')
    warehouse_by_clothes = pyreports.Report(warehouse, filter=clothes, title='clothes items in warehouse')

    # Create a ReportBook objects
    sales_book = pyreports.ReportBook([sales_by_household, sales_by_clothes], filter='Total sold')
    warehouse_book = pyreports.ReportBook([warehouse_by_household, warehouse_by_clothes], filter='Total remained')

    # Save reports
    sales_book.export('/home/report/sales.xlsx')
    warehouse_book.export('/home/report/warehouse.xlsx')

    # Other report: combine two book
    all = sales_book + warehouse_book
    all.export('/home/report/all.xlsx')

    # Now print to stdout all data
    all.export()

Command line report
-------------------

In this example, we're going to create a script that doesn't save any files. We will read from a database, modify the data
so that it is more readable and print it in standard output. We will also see how to use our script with other command line tools.

.. code-block:: python

    import pyreports

    # Get data from database: a DatabaseManager object
    mydb = pyreports.manager('sqllite', database='/var/myapp/myapp.db')
    mydb.execute('SELECT * FROM performance')
    performance = mydb.fetchall()

    # Transform data for command line reader
    cmd = pyreports.Executor(performance)

    def number_to_second(seconds):
        if isinstance(seconds, int):
            ret = float(int)
            return f'{ret:.2f} s'
        else:
            return seconds

    cmd.map(number_to_second)

    # Print data
    print(cmd.get_data())

Now we can read the db directly from the command line.

.. code-block:: console

    $ python performance.py
    $ python performance.py | grep -G "12.*"

.. note::
    The examples we can give are almost endless. This library has such flexible python objects that we can adapt them to any use case.
    You can also use it as a simple database data reader.

Use cases
*********

As you may have noticed, there are many use cases for this library. The ``manager`` objects are so flexible that you
can read and write data from any source.
Furthermore, thanks to the ``Executor`` objects you can filter and modify the data on-demand when you want and restore
it at a later time, and then channel it into the ``Report`` objects and then into the ``ReportBook`` collection objects.

Below, I'll list other use cases common to both package users and developers:

- Export LDAP users and insert them into a database
- Read a log file and write it into a database
- Find out which LDAP users are present in a web server log file
- Backup configuration files by exporting them in yaml format (passwd, httpd.conf, etc)
- Calculate access rates of a database
- Count how many times an ip address is present in a log file

I could go on indefinitely; anything you can think of about a file, a database and an LDAP server and you need to
manipulate or verify the data, this is the library for you.