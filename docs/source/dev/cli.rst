.. toctree::
   :maxdepth: 2
   :caption: Contents:

Command Line Interface
######################

*pyreports* has a command line interface which takes a configuration file in `YAML <https://yaml.org/>`_ format as an argument.


Command arguments
*****************

The only mandatory argument is the `YAML <https://yaml.org/>`_ language configuration file.

Optional arguments
------------------

Here are all the optional flags that the command line interface has.

+---------------+----------------------+
| flags         | description          |
+===============+======================+
| -v/--verbose  | Enable verbose mode  |
+---------------+----------------------+
| -V/--version  | Print version        |
+---------------+----------------------+
| -h/--help     | Print help           |
+---------------+----------------------+

Report configuration
********************

The *YAML* file representing your reports begins with a **reports** key.

.. code-block:: yaml

    reports:
        # ...


Each report you want to define is a **report** key inside *reports*.

.. code-block:: yaml

    # My reports collection
    reports:
        # My single report
        report:

