Data Tools
##########

The package comes with utility functions to work directly with *Datasets*.
In this section we will see all these functions contained in the **datatools** module.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Average
-------

**average** function calculates the average of the numbers within a column.

.. code-block:: python

    import pyreports

    # Build a dataset
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])

    # Calculate average
    print(pyreports.average(mydata, 'salary'))  # Column by name
    print(pyreports.average(mydata, 2))         # Column by index

.. attention::
    All values in the column must be ``float`` or ``int``, otherwise a ``ReportDataError`` exception will be raised.

Most common
-----------

The **most_common** function will return the value of a specific column that is most recurring.

.. code-block:: python

    import pyreports

    # Build a dataset
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    mydata.append(('Ford', 'Prefect', 65000))

    # Get most common
    print(pyreports.most_common(mydata, 'name'))  # Ford

Percentage
----------

The **percentage** function will calculate the percentage based on a filter (Any) on the whole *Dataset*.

.. code-block:: python

    import pyreports

    # Build a dataset
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    mydata.append(('Ford', 'Prefect', 65000))

    # Calculate percentage
    print(pyreports.percentage(mydata, 65000))  # 66.66666666666666 (percent)

Counter
-------

The **counter** function will return a `Counter <https://docs.python.org/3/library/collections.html#collections.Counter>`_ object, with inside it the count of each element of a specific column.

.. code-block:: python

    import pyreports

    # Build a dataset
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    mydata.append(('Ford', 'Prefect', 65000))

    # Create Counter object
    print(pyreports.counter(mydata, 'name'))  # Counter({'Arthur': 1, 'Ford': 2})

