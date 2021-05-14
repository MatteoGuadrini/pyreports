pyreports example
#################

Example scripts using ``pyreports`` module.

.. toctree::
   :maxdepth: 2
   :caption: Contents:



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
    mydb = pyreports.manager('mysql', host='mysql1.local', database='login_users', username='dba', password='dba0000')

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

    # Return json from GET  request on web server: this is a FileManager object
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
    mydb = pyreports.manager('mysql', host='mysql1.local', database='users', username='dba', password='dba0000')

    # Write to database
    mydb.executemany("INSERT INTO internal_users(name, surname, employeeType) VALUES(%s, %s, %s)", list(user_int))
    mydb.executemany("INSERT INTO external_users(name, surname, employeeType) VALUES(%s, %s, %s)", list(user_ext))
    mydb.commit()

