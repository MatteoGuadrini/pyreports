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



