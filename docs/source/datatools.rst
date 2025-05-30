Data tools
##########

The package comes with utility functions to work directly with *Datasets*.
In this section we will see all these functions contained in the **datatools** module.


.. toctree::


DataObject
----------

**DataObject** class represents a pure *Dataset*.

.. autoclass:: pyreports.DataObject
   :members:

.. code-block:: python

    import pyreports, tablib

    data = pyreports.DataObject(tablib.Dataset(*[("Arthur", "Dent", 42)]))
    assert isinstance(data.data, tablib.Dataset) == True

    # Clone data
    new_data = data.clone()
    assert isinstance(new_data.data, tablib.Dataset) == True

    # Select column
    new_data.column("name")
    new_data.column(0)



DataAdapters
------------

**DataAdapters** class is an object that contains methods that modifying *Dataset*.

.. code-block:: python

    import pyreports, tablib

    data = pyreports.DataAdapters(tablib.Dataset(*[("Arthur", "Dent", 42)]))
    assert isinstance(data.data, tablib.Dataset) == True


    # Aggregate
    planets = tablib.Dataset(*[("Heart",)])
    data.aggregate(planets)

    # Merge
    others = tablib.Dataset(*[("Betelgeuse", "Ford", "Prefect", 42)])
    data.merge(others)

    # Counter
    data = pyreports.DataAdapters(Dataset(*[("Heart", "Arthur", "Dent", 42)]))
    data.merge(self.data)
    counter = data.counter()
    assert counter["Arthur"] == 2

    # Chunks
    data.data.headers = ["planet", "name", "surname", "age"]
    assert list(data.chunks(4))[0][0] == ("Heart", "Arthur", "Dent", 42)

    # Deduplicate
    data.deduplicate()
    assert len(data.data) == 2

    # Subsets
    new_data = data.subset("planet", "age")
    assert len(data.data[0]) == 2

    # Sort
    new_data = data.sort("age")
    reverse_data = data.sort("age", reverse=True)

    # Get items
    assert data[1] == ("Betelgeuse", "Ford", "Prefect", 42)

    # Iter items
    for item in data:
        print(item)


.. autoclass:: pyreports.DataAdapters
   :members:

DataPrinters
------------

**DataPrinters** class is an object that contains methods that printing *Dataset*'s information.

.. code-block:: python

    import pyreports, tablib

    data = pyreports.DataPrinters(tablib.Dataset(*[("Arthur", "Dent", 42), ("Ford", "Prefect", 42)], headers=["name", "surname", "age"]))
    assert isinstance(data.data, tablib.Dataset) == True

    # Print
    data.print()

    # Average
    assert data.average(2) == 42
    assert data.average("age") == 42

    # Most common
    data.data.append(("Ford", "Prefect", 42))
    assert data.most_common(0) == "Ford"
    assert data.most_common("name") == "Ford"

    # Percentage
    assert data.percentage("Ford") == 66.66666666666666

    # Representation
    assert repr(data) == "<DataObject, headers=['name', 'surname', 'age'], rows=3>"

    # String
    assert str(data) == 'name  |surname|age\n------|-------|---\nArthur|Dent   |42 \nFord  |Prefect|42 \nFord  |Prefect|42 '

    # Length
    assert len(data) == 3

.. autoclass:: pyreports.DataPrinters
   :members:


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

Deduplicate
-----------

The **deduplicate** function remove duplicated rows into *Dataset* objects.

.. code-block:: python

    import pyreports

    # Build a datasets
    employee1 = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])

    # Remove duplicated rows (removed the last ('Ford', 'Prefect', 65000))
    print(len(pyreports.deduplicate(employee1)))     # 2

Subset
------

The **subset** function make a new *Dataset* with only selected columns.

.. code-block:: python

    import pyreports

    # Build a datasets
    employee1 = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])

    # Select only a two columns
    print(len(pyreports.subset(employee1, 'name', 'surname')[0]))     # 2

Sort
----

The **sort** function sort the *Dataset* by column, also in reversed mode.

.. code-block:: python

    import pyreports

    # Build a datasets
    employee1 = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])

    # Sort and sort reversed
    print(pyreports.sort(employee1, 'salary'))
    print(pyreports.sort(employee1, 'salary', reverse=True))