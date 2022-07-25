Data tools
##########

The package comes with utility functions to work directly with *Datasets*.
In this section we will see all these functions contained in the **datatools** module.


.. toctree::




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

Aggregate
---------

The **aggregate** function aggregates multiple columns of some *Dataset* into a single *Dataset*.

.. warning::
    The number of elements in the columns must be the same. If you want to aggregate columns with a different number of elements,
    you need to specify the argument ``fill_empty=True``. Otherwise, an ``InvalidDimension`` exception will be raised.

.. code-block:: python

    import pyreports

    # Build a datasets
    employee = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    places = tablib.Dataset([('London', 'Green palace', 1), ('Helsinky', 'Red palace', 2)], headers=['city', 'place', 'floor'])

    # Aggregate column for create a new Dataset
    new_data = pyreports.aggregate(employee['name'], employee['surname'], employee['salary'], places['city'], places['place']))
    new_data.headers = ['name', 'surname', 'salary', 'city', 'place']
    print(new_data)     # ['name', 'surname', 'salary', 'city', 'place']

Merge
-----

The **merge** function combines multiple *Dataset* objects into one.

.. warning::
    The datasets must have the same number of columns otherwise an ``InvalidDimension`` exception will be raised.

.. code-block:: python

    import pyreports

    # Build a datasets
    employee1 = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    employee2 = tablib.Dataset([('Tricia', 'McMillian', 55000), ('Zaphod', 'Beeblebrox', 65000)], headers=['name', 'surname', 'salary'])

    # Merge two Dataset object into only one
    employee = pyreports.merge(employee1, employee2)
    print(len(employee))     # 4

Chunks
------

The **chunks** function divides a *Dataset* into pieces from *N* (``int``). This function returns a generator object.

.. code-block:: python

    import pyreports

    # Build a datasets
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    mydata.append(*[('Tricia', 'McMillian', 55000), ('Zaphod', 'Beeblebrox', 65000)])

    # Divide data into 2 chunks
    new_data = pyreports.chunks(mydata, 2)      # Generator object
    print(list(new_data))     # [[('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], [('Tricia', 'McMillian', 55000), ('Zaphod', 'Beeblebrox', 65000)]]

.. note::
    If the division does not result zero, the last tuple of elements will be a smaller number.