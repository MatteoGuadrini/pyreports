Executors
#########

The **Executor** object is the one who analyzes and processes the data that is instantiated with it.
This type of object is the first core object we will see and the basis for all the others.


.. toctree::




Executor at work
****************

To instantiate an *Executor* object, you need two things: the mandatory one, a **Dataset** and the other optional is a **header**,
which represents the data. Let's see how to instantiate an *Executor* object.

.. code-block:: python

    import pyreports

    # Create a data source
    mydb = pyreports.manager('mysql', host='mysql1.local', database='test', user='dba', password='dba0000')

    # Get data
    mydb.execute('SELECT * FROM salary')
    employees = mydb.fetchall()                 # return Dataset object

    # Create Executor object
    myex = pyreports.Executor(employees)        # The employees object already has a header, as it was created by a database manager

.. note::
    If I wanted to apply a header different from the name of the table columns, perhaps because they are not very speaking or full of underscores, I would have to instantiate the object as follows:
    ``myex = pyreports.Executor(employees, header=['name', 'surname', 'salary'])``.
    If you wanted to remove the header instead, just set it as ``None``: ``myex = pyreports.Executor(employees, header=None)``

The *Executor* is a flexible object. It is not related to the *pyreports* library. An *Executor* can also be instantiated via
its own Dataset or from a list of tuples (Python primitives used to instantiate a Dataset object. It is also equal to
the return value of a database object)

.. code-block:: python

    import pyreports
    import tablib

    # Create my Dataset object
    mydata = tablib.Dataset()
    mydata.append(['Arthur', 'Dent', 55000])
    mydata.append(['Ford', 'Prefect', 65000])

    # Create Executor object: same result for both
    myex = pyreports.Executor(mydata, header=['name', 'surname', 'salary'])
    myex = pyreports.Executor([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], header=['name', 'surname', 'salary'])

    # Set header after creation
    myex.headers(['name', 'surname', 'salary'])

Filter data
-----------

One of the main functions of working with data is to filter it. The *Executor* object has a filter method for doing this.
This method accepts a list of values that must correspond to one of the values of a row in the Executor's Dataset.

Another way to filter the data of an *Executor* object is to pass a callable that takes a single argument and returns something.
The return value will be called by the ``bool`` class to see if it is ``True`` or ``False``.
This callable will be called to every single value of the row of the Executor's Dataset.

Finally, it is possible to declare the name of a single return column, if not all columns are needed.

.. note::
    You can pass both a list of values and a function to filter the data.

.. code-block:: python

    # Filter data by list
    myex.filter([55000, 65000, 75000])                          # Filter data only for specified salaries

    # Filter data by callable
    myex.filter(key=str.istitle)                                # Filter data only for string contains Title case

    def big_salary(salary):
        if not isinstance(salary, int):
            return False
        return True if salary >= 65000 else False               # My custom function

    myex.filter(key=big_salary)                                 # Filter data with a salary greater than or equal to 65000

    # Filter data by column
    myex.filter(column='salary')                                # Filter by column: name
    myex.filter(column=2)                                       # Filter by column: index

    # Filter data by list, callable and column
    myex.filter([55000, 65000, 75000], str.istitle, 'salary')   # Filter for all three methods

.. warning::
    If the filters are not applied, the result will be an empty Executor object.
    If you want to reapply a filter, you will have to reset the object, using the ``reset()`` method. See below.

Map (modify) data
-----------------

The *Executor* object is provided with a method to modify the data in real time.
The ``map`` method accepts a mandatory argument, i.e. a callable that accepts a single argument and an optional one
that accepts the name of the column or the number of its index.

.. code-block:: python

    # Define my function for increase salary; isn't that amazing!
    def salary_increase(salary):
        if isinstance(salary, int):
            if salary <= 65000:
                return salary + 10000
        return salary

    # Let's go! Increase salary today!
    myex.map(salary_increase)

    # Now, return only salary columns
    myex.map(salary_increase, column='salary')

.. warning::
    If the function you are passing to the *map* method returns nothing, ``None`` will be substituted for the original value.
    If you are using special conditions make sure your function always returns to its original value.

Get data
--------

An *Executor* is not a data object. It is an object that contains data for processing, filters and etc.
Once an instance of an *Executor* object is created, the original data is saved so that it can be retrieved.

So there is a way to retrieve and print the current and original data.

.. code-block:: python

    # Get data
    myex.get_data()                                 # Return current Dataset object
    myex.origin                                     # Return original Dataset object
    print(myex.get_data())                          # Print Dataset with current data

    # Assign result to variable
    my_dataset = myex.get_data()                    # Return Dataset object

    # Create a new executor
    new_ex = pyreports.Executor(myex.get_data())    # New Executor object with current data
    new_ex = myex.clone()                           # New Executor object with original data

.. note::
    If you want to clone the original data contained in an Executor object, use the ``clone`` method.

It is possible through this object, to restore the data source after the modification or the applied filter.

.. code-block:: python

    # Restore data
    myex.reset()                                 # Reset data to origin
    print(myex.get_data())

.. attention::
    Once the object is reset, any changes made will be lost, unless the object has been cloned.

Work with columns
-----------------

Since the *Executor* object is based on a Dataset object, it is possible to work not only with rows but also with columns.
Let's see how to select a single column.

.. code-block:: python

    # Select column
    myex.select_column(1)               # Select column by index number (surname)
    myex.select_column('surname')       # Select column by name (surname)

We can also add columns as long as they are the same length as the others, otherwise, we will receive an ``InvalidDimension`` exception.

.. code-block:: python

    # Add column with values
    myex.add_column('floor', [1, 2])

    # Add column with function values
    def stringify_salary(row):
        return f'$ {row[2]}'

    myex.add_column('str_salary', stringify_salary)

.. note::
    The function passed to the ``add_column`` method must have a single argument representing the row (the name *"row"* is a convention).
    You can use this argument to access data from other columns.

It is also possible to delete a column.

.. code-block:: python

    # Delete column
    myex.del_column('floor')

Count
-----

The *Executor* object contains data. You may need to count rows and columns.
The object supports the protocol for counting through the built-in ``len`` function, which will return the current number of rows.

.. code-block:: python

    # Count columns
    myex.count_columns()        # Return number of columns

    # Count rows
    myex.count_rows()           # Return number of rows
    len(myex)                   # Return number of rows

Iteration
---------

The *Executor* object supports the python iteration protocol (return of generator object).
This means that you can use it in a for loop or in a list comprehension.

.. code-block:: python

    # For each row in Executor
    for row in myex:
        print(row)

    # List comprehension
    my_list_of_rows = [row for row in myex]