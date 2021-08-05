# Release notes

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