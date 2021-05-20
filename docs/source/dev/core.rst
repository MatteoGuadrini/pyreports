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

