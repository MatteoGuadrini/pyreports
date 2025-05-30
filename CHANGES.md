# Release notes

## 1.8.0
May 31, 2025

- Add **add** special method into _Executor_ class
- Add **type** property on _Manager_ class
- Add **ExecutorDataError** class
- Add **reset** method into _Report_ class
- Add **clone** method into _DataObject_ class
- Add **clone** method into _Report_ class
- Add **column** method on _DataObject_ class
- Add **subset** method on _DataAdapters_ class
- Add **subset** function
- Add _try/except_ into **send** method on _ReportBook_ class
- Add **sort** method into _DataAdapters_ class
- Add **sort** function
- Add **sort**, **subset** and **subset** data tools
- Make _report_ attribute into property on _Report_ class
- Use _remove_duplicates_ method on **deduplicate** functions
- Change behavior of _column_ parameter into **filter** function on _Executor_ class

## 1.7.0
Apr 19, 2024

- Remove **pymssql** support
- Add **DataObject** class
- Add **DataAdapters** class
- Add **DataPrinters** class
- Add **aggregate** into _DataAdapters_ class
- Add **merge** method into _DataAdapters_ class
- Add **counter** method into _DataAdapters_ class
- Add **chunks** method into _DataAdapters_ class
- Add **deduplicate** method into _DataAdapters_ class
- Add **iter** method into _DataAdapters_ class
- Add **getitem** method into _DataAdapters_ class
- Add **repr** and **str** function into _DataPrinters_ class
- Add **average** method into _DataPrinters_ class
- Add **most_common** method into _DataPrinters_ class
- Add **percentage** method into _DataPrinters_ class
- Add **len** method into _DataPrinters_ class
- Add **DataAdapters** and **DataPrinters** classes into _Report_ class
- Add **DataObjectError** exception class

## 1.6.0
Jul 14, 2023

- Add **deduplicate** function on datatools
- Add **Manager** abstract class
- Add **READABLE_MANAGER** and **WRITABLE_MANAGER** tuple
- Add _pyproject.toml_ file
- Add **negation** to filter method on _Executor_ class
- Fix _max_len_ into **aggregate** function, refs #2
- Fix _sendmail_ method addresses, refs #3
- Rename **SQLiteConnection** class
- Reformat code with ruff code analysis

## 1.5.0
Aug 4, 2022

- Added **cli** module
- Added **reports** cli
- Added **\__getitem\__** method on _Report_ class
- Added **\__delitem\__** method on _Report_ class
- Added **\__getitem\__** method on _ReportBook_ class
- Added **\__delitem\__** method on _ReportBook_ class
- Added **\__contains\__** on _Executor_ class
- Fix **NoSQLManager** creation into _manager_ function
- Fix **print_data** on _Report_ class

## 1.4.0
Jun 27, 2022

- Added **\__bool\__** method on _Report_ class
- Added **\__iter\__** method on _Report_ class
- Added **\__bool\__** method on _ReportBook_ class
- Added **\__iter\__** method on _Connection_ and _File_ classes
- Added **\__iter\__** method on _FileManager_ class
- Added **\__iter\__** method on _DatabaseManager_ class
- Added **\__getitem\__** on _Executor_ class
- Added **\__delitem\__** on _Executor_ class
- Fix name of attachment on **send** method of _Report_ class
- Fix **write** method on _LogFile_ class

## 1.3.0
Apr 15, 2022

- Added **NoSQLManager** class; this class extend _Manager_ class on the [nosqlapi](https://github.com/MatteoGuadrini/nosqlapi) package
- Added **LogFile** class; this class load a log file and _read_ method accept regular expression
- Added **\__bool\__** and **\__repr\__** method on _File_ and _Connection_ abstract classes
- Fix documentation API section
- Fix tests package
- Fix CircleCi docker image

## 1.2.0
Aug 5, 2021

- Added _fill_value_ argument on **aggregate** function; this value also is callable without arguments
- Added _send_ method on **Report** class; with this method you send report via email
- Added _send_ method on **ReportBook** class; with this method you send report via email
- Fix \*__str__* method on **Report** class

## 1.1.0
Jun 5, 2021

- Created abstract **File** class
- Created **TextFile** class
- Added *\__str__* method for pretty representation of **Executor** class
- Added *\__repr__* method for representation of **DatabaseManager** class
- Added *\__repr__* method for representation of **FileManager** class
- Added *\__repr__* method for representation of **LdapManager** class
- Fix documentation for new abstract **File** class

## 1.0.0
May 26, 2021

- Created abstract **Connection** class
- Created **\*Connection** classes
- Created **\*File** classes
- Created **FileManager**, **DatabaseManager** and **LdapManager** classes
- Created **Executor** class
- Created **Report** class
- Created **ReportBook** class
- Created **average**, **most_common**, **percentage**, **counter**, **aggregate**, **merge**, **chunks**, functions