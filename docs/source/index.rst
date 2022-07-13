.. pyreports documentation master file, created by
   sphinx-quickstart on Mon May  3 12:34:29 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyreports's documentation!
=====================================

*pyreports* is a python library that allows you to create complex reports from various sources such as databases,
text files, ldap, etc. and perform processing, filters, counters, etc. and then export or write them in various formats or in databases.

You can use this library for complex reports, or to simply filter data into datasets divided by topic. Furthermore,
it is possible to export in various formats, such as csv, excel files or write directly to the database (*mysql*, *mssql*, *postgresql* and more).

.. _workflow:

Report workflow
***************

This package provides tools for receiving, processing and exporting data. Mostly, it follows this workflow.

.. code-block::

   +-----------------+      +-----------------+      +-----------------+
   |                 |      |                 |      |                 |
   |                 |      |                 |      |                 |
   |      INPUT      +----->|     PROCESS     +----->|      OUTPUT     |
   |                 |      |                 |      |                 |
   |                 |      |                 |      |                 |
   +-----------------+      +-----------------+      +-----------------+


Features
********

- Capture any type of data
- Export data in many formats
- Data analysis
- Process data with filters and maps
- Some functions will help you to process averages, percentages and much more

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   managers
   executors
   report
   datatools
   example
   package

.. toctree::
   :maxdepth: 2
   :caption: API:

   dev/io
   dev/core

.. toctree::
   :maxdepth: 2
   :caption: CLI:

   dev/cli


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
