Reports
#######

The package it is provided with a **Report** object and a **ReportBook** object.

The *Report* object provides an interface for a complete workflow-based report (see :ref:`workflow`).

The *ReportBook* object, on the other hand, is a list of *Report* objects.

This will follow the workflows of each *Report* it contains, except for the output, which can be saved in a single Excel file.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Report at work
**************

The *Report* object provides an interface to the entire workflow of a report: it accepts an input, processes the data and provides an output.
To instantiate an object, you basically need three things:

- **input**: a *Dataset* object, mandatory.
- **filter**, **map function** or/and **column**: they are the same objects you would use in an *Executor* object, optional.
- **output**: a *FileManager* object, optional.

.. code-block:: python

    import pyreports
    import tablib

    # Instantiate a simple Report object
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    myrep = pyreports.Report(mydata)

    # View report
    myrep           # repr(myrep)
    print(myrep)    # str(myrep)

Advanced Report instance
------------------------

The *Report* object is very complex. Instantiating it as above makes little sense, because the result will be identical to the input dataset.
This object enables a series of features for data processing.

.. code-block:: python

    import pyreports
    import tablib

    # Instantiate a Report object
    salary55k = pyreports.manager('csv', '/tmp/salary55k.csv')
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    report_only_55k = pyreports.Report(mydata, filters=[55000], title='Report salary 55k', output=salary55k)

    # View report
    myrep           # <Report object, title=Report salary 55k>

The example above, creates a *Report* object that filters input data only for employees with a salary of 55k.
But we can also edit the data on-demand and then filter it, as follows in the next example.

.. code-block:: python

    import pyreports
    import tablib

    # My custom function for modifying salary data
    def stringify_salary(salary):
        if isinstance(salary, int):
            return f'$ {salary}'
        else:
            return salary

    # Instantiate a Report object
    salary55k = pyreports.manager('csv', '/tmp/salary55k.csv')
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    report_only_55k = pyreports.Report(mydata,
                                        filters=['$ 55000'],
                                        map_func=stringify_salary,
                                        title='Report salary 55k',
                                        output=salary55k)

    # View report
    myrep           # <Report object, title=Report salary 55k>

.. note::
    It is also possible to declare a counter of the processed lines by setting ``count=True``.
    Moreover, as for an Executor object, you can specify a single return column using the column argument; former. ``column='surname'``.