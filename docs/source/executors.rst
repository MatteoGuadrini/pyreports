Executors
#########

The **Executor** object is the one who analyzes and processes the data that is instantiated with it.
This type of object is the first core object we will see and the basis for all the others.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Executor at work
****************

To instantiate an *Executor* object, you need two things: the mandatory one, a **Dataset** and the other optional is a **header**,
which represents the data. Let's see how to instantiate an *Executor* object.

.. code-block:: python

    import pyreports

    # Create a data source
    mydb = pyreports.manager('mysql', host='mysql1.local', database='test', username='dba', password='dba0000')

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