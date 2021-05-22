.. toctree::

core
####

In this section, we will see how to expand and modify *pyreports core* objects.

Expand Executor
***************

It is possible that in some particular case, it is necessary to have custom methods not included in the objects at our disposal.
This concept extends to python in general, but we will focus on this library.

Custom map method
-----------------

The ``map`` method of the ``Executor`` class accepts a function as an argument that it will call for each element of each row of the ``Dataset`` included in the ``Executor`` object.

.. literalinclude:: ../../../pyreports/core.py
    :language: python
    :pyobject: Executor.map

There may be a need to apply the function on the entire row. Personalization could be done like this:

.. code-block:: python

    import pyreports
    import tablib

    # Define my Executor class
    class MyExecutor(pyreports.Executor):

        # My custom map method
        def map(self, key, column=None):
            if callable(key):
                ret_data = tablib.Dataset(headers=self.data.headers)
                for row in self:
                    # Apply function to data
                    ret_data.append(key(row))
                self.data = ret_data
            else:
                raise ValueError(f"{key} isn't function object")
            # Return all data or single column
            if column and self.data.headers:
                self.data = self.select_column(column)

    # Test my map
    exec = MyExecutor([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], header=['name', 'surname', 'salary'])

    # Function than accept row (iterable)
    def stringify(row):
        return [str(item) for item in row]

    exec.map(stringify)

Add method
----------

You can also add new functionality to the ``Executor`` object. We are going to add a method to view the data content of an ``Executor``.


.. code-block:: python

    import pyreports

    # Define my Executor class
    class MyExecutor(pyreports.Executor):

        def __str__(self):
            return self.data


    # Print data
    exec = MyExecutor([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], header=['name', 'surname', 'salary'])
    print(exec)

Expand Report
*************

The ``Report`` object is really versatile. It is a representation of the report's workflow in full. However, there may be greater needs.
For example, before saving the output, make a certain request or save the output before and after processing.

To "break" the working process of the *Report* object, you need to expand it and re-implement its methods.

Save the origin
---------------

As anticipated, sometimes we need to save the data before it is processed.
To do this, we need to implement a new method to augment or modify the workflow.
In this way, we are going to run this worklow:
``[INPUT] -> [SAVE ORIGIN] -> [PROCESS] -> [OUTPUT]``

.. code-block:: python

    import pyreports
    import tablib
    import os

    # Define my Executor class
    class MyReport(pyreports.Report):

        def save_origin(self):
            # Save origin in origin file
            if self.output:
                self.output.write(self.data)
                os.rename(self.output.file, 'origin_' + self.output.file)
            # Process report
            self.export()

    # Test MyReport
    salary55k = pyreports.manager('csv', '/tmp/salary55k.csv')
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    report_only_55k = MyReport(mydata, filters=[55000], title='Report salary 55k', output=salary55k)

    # My workflow report: [INPUT] -> [SAVE ORIGIN] -> [PROCESS] -> [OUTPUT]
    report_only_55k.save_origin()


Always print
------------

Another highly requested feature is to save and print at the same time. Much like the Unix ``tee`` shell command,
we will implement the new functionality in our custom *Report* object.

.. code-block:: python

    import pyreports
    import tablib

    # Define my Executor class
    class MyReport(pyreports.Report):

        def tee(self):
            # Print data...
            print(self)
            # ...and save!
            self.export()

    # Test MyReport
    salary55k = pyreports.manager('csv', '/tmp/salary55k.csv')
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    report_only_55k = MyReport(mydata, filters=[55000], title='Report salary 55k', output=salary55k)

    # Print and export
    report_only_55k.tee()

Extend ReportBook
*****************

The ``ReportBook`` object is a collection of ``Report`` type objects.
When you iterate over an object of this type, you get a generator that returns the *Report* objects it contains one at a time.

.. note::
    Nothing prevents that you can also insert the ``MyReport`` classes created previously. They are also subclasses of ``Reports``.

Book to dict
------------

One of the features that might interest you is to export a *ReportBook* as if it were a dictionary.

.. code-block:: python

    import pyreports
    import tablib


    # Instantiate the Report objects
    mydata = tablib.Dataset([('Arthur', 'Dent', 55000), ('Ford', 'Prefect', 65000)], headers=['name', 'surname', 'salary'])
    report_only_55k = pyreports.Report(mydata, filters=[55000], title='Report salary 55k')
    report_only_65k = pyreports.Report(mydata, filters=[65000], title='Report salary 65k')

    class MyReportBook(pyreports.ReportBook):

        def to_dict(self):
            return {report.title: report for report in self if report.title}

    # Test my book
    salary = MyReportBook([report_only_55k, report_only_65k])
    salary.to_dict()            # {'Report salary 55k': <Report object, title=Report salary 55k>, 'Report salary 65k': <Report object, title=Report salary 65k>}

