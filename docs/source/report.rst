Reports
#######

The package it is provided with a **Report** object and a **ReportBook** object.

The *Report* object provides an interface for a complete workflow-based report (see :ref:`workflow`).

The *ReportBook* object, on the other hand, is a list of *Report* objects.

This will follow the workflows of each *Report* it contains, except for the output, which can be saved in a single Excel file.


.. toctree::




Report at work
**************

The *Report* object provides an interface to the entire workflow of a report: it accepts an input, processes the data and provides an output.
To instantiate an object, you basically need three things:

- **input**: a *Dataset* object, mandatory.
- **filter**, **map function** or/and **column**: they are the same objects you would use in an *Executor* object, optional.
- **output**: a *Manager* object, optional.

.. code-block:: python

    import pyreports
    import tablib

    # Instantiate a simple Report object
    mydata = tablib.Dataset(*[('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
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
    mydata = tablib.Dataset(*[('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    report_only_55k = pyreports.Report(mydata, filters=[55000], title='Report salary 55k', output=salary55k)

    # View report
    myrep           # <Report object, title=Report salary 55k>

The example above, creates a *Report* object that filters input data only for employees with a salary of 55k.
But we can also edit the data on-demand and then filter it, as follows in the next example.

.. note::
    You can also pass a function to the ``filters`` argument, as for an *Executor* object.

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
    salary55k = pyreports.manager('sqlite', '/tmp/mydb.db')     # DatabaseManager
    mydata = tablib.Dataset(*[('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    report_only_55k = pyreports.Report(mydata,
                                        filters=['$ 55000'],
                                        map_func=stringify_salary,
                                        title='Report salary 55k',
                                        output=salary55k)

    # View report
    myrep           # <Report object, title=Report salary 55k>

.. note::
    It is also possible to declare a counter of the processed lines by setting ``count=True``.
    Moreover, as for an Executor object, you can specify a single return ``column`` using the column argument; ex. ``column='surname'``.

Execute Report
--------------

Once a *Report* object has been instantiated, you can execute the filters and editing functions (map) set during the creation of the object.

.. code-block:: python

    # Apply filters and map function
    report_only_55k.exec()

    # Print result
    print(report_only_55k)

    # Adding count after creation
    report_only_55k.count = True
    report_only_55k.exec()
    print(report_only_55k)

.. warning::
    Once a filter or map function is applied, it will not be possible to go back.
    If you want to change filters after call the ``exec`` method, you need to re-instantiate the object.

Export
------

Once the ``exec`` method is called, and then once the data is processed, we can export the data based on the output set when instantiating the object.

.. note::
    If the output has not been specified, calling the export method will print the data to stdout.

.. code-block:: python

    # Save report on /tmp/salary55k.csv
    report_only_55k.export()

    # Unset output
    report_only_55k.output = None
    report_only_55k.export()            # This print the data on stdout

    # Set output
    report_only_55k.output = salary55k
    report_only_55k.export()            # Save report on /tmp/salary55k.csv


ReportBook at work
******************

The *ReportBook* object is a collection (list) of *Report* objects.
This basically allows you to collect multiple reports in a single container object.
The main advantage is the ability to iterate over each *Report* and access its properties.

.. code-block:: python

    import pyreports
    import tablib

    # Instantiate the Report objects
    mydata = tablib.Dataset(*[('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    report_only_55k = pyreports.Report(mydata, filters=[55000], title='Report salary 55k')
    report_only_65k = pyreports.Report(mydata, filters=[65000], title='Report salary 65k')

    # Create a ReportBook
    salary = pyreports.ReportBook([report_only_55k, report_only_65k])

    # View ReportBook
    salary           # repr(salary)
    print(salary)    # str(salary)

.. note::
    The ReportBook object supports the ``title`` property, as follows: ``pyreports.ReportBook(title='My report book')``

Export reports
--------------

The *ReportBook* object has an ``export`` method.
This method not only saves *Report* objects to its output, but first executes the ``exec`` method of each *Report* object it contains.

.. warning::
    As for *Report* objects, even a *ReportBook* object once the export method has been called,
    it will need to be instantiated again if you want to reset the data to the source, before applying the filters and map functions.

.. code-block:: python

    # Export a ReportBook
    salary.export()         # This run exec() and export() on each Report object

    # Export each Report on one file Excel (xlsx)
    salary.export('/tmp/salary_report.xlsx')

Add and remove report
---------------------

Being a container, the *ReportBook* object can be used to add and remove *Report* object.

.. code-block:: python

    # Create an empty ReportBook
    salary = pyreports.ReportBook(title='Salary report')

    # Add a Report object
    salary.add(report_only_55k)
    salary.add(report_only_65k)

    # Remove last Report object added
    salary.remove()                     # Remove report_only_65k object
    salary.remove(0)                    # Remove report_only_55k object, via index

Count reports
-------------

The *ReportBook* object supports the protocol for the built-in ``len`` function, to count the *Report* objects it contains.

.. code-block:: python

    # Count object
    len(salary)

Iteration
---------

The *ReportBook* object supports the python iteration protocol (return of generator object).
This means that you can use it in a for loop or in a list comprehension.

.. code-block:: python

    # For each report in ReportBook
    for report in salary:
        print(report)

    # List comprehension
    my_list_of_report = [report for report in salary]

Merge
-----

ReportBook objects can be joined together, using the `+` operator.

.. code-block:: python

    # ReportBook
    book1 = pyreports.ReportBook([report1, report2])
    book2 = pyreports.ReportBook([report3, report4])
    # Merge ReportBook
    tot_book = book1 + book2
    tot_book = book1.__add__(book2)

    print(tot_book)

    # ReportBook None
    #   Report1
    #   Report2
    #   Report3
    #   Report4