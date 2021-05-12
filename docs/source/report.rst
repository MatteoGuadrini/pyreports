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
