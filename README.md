# reports

_reports_ is a python library that allows you to create complex reports from various sources such as databases, 
text files, ldap, etc. and perform processing, filters, counters, etc. 
and then export or write them in various formats or in databases.

> Project status: **beta released**

## Test package

To test the package, follow these instructions:

```console
$ git clone https://github.com/MatteoGuadrini/reports.git
$ cd reports
$ python -m unittest discover tests
```

## How does it work

_reports_ wants to be a library that simplifies the collection of data from multiple sources such as databases, 
files and directory servers (through LDAP), the processing of them through built-in and customized functions, 
and the saving in various formats (or, by inserting the data in a database).

_reports_ uses the [**tablib**](https://tablib.readthedocs.io/en/stable/) library to organize the data into _Dataset_ object.

### Simple report

I take the data from a database table, filter the data I need and save it in a csv file

```python
import reports

# Select source: this is a DatabaseManager object
mydb = reports.manager('mysql', host='mysql1.local', database='login_users', username='dba', password='dba0000')

# Get data
mydb.execute('SELECT * FROM site_login')
site_login = mydb.fetchall()

# Filter data
error_login = reports.Executor(site_login)
error_login.filter([400, 401, 403, 404, 500])

# Save report: this is a FileManager object
output = reports.manager('csv', '/home/report/error_login.csv')
output.write(error_login.get_data())

```

### Combine source

I take the data from a database table and a log file and save the report in json format

```python
import reports

# Select source: this is a DatabaseManager object
mydb = reports.manager('mysql', host='mysql1.local', database='login_users', username='dba', password='dba0000')
# Select another source: this is a FileManager object
mylog = reports.manager('file', '/var/log/httpd/error.log')

# Get data
mydb.execute('SELECT * FROM site_login')
site_login = mydb.fetchall()
error_log = mylog.read()

# Filter database
error_login = reports.Executor(site_login)
error_login.filter([400, 401, 403, 404, 500])
users_in_error = set(error_login.select_column('users'))

# Prepare log
myreport = dict()
log_user_error = reports.Executor(error_log)
log_user_error.filter(list(users_in_error))
for line in log_user_error:
    for user in users_in_error:
        myreport.setdefault(user, [])
        myreport[user].append(line)

# Save report: this is a FileManager object
output = reports.manager('json', '/home/report/error_login.json')
output.write(myreport)

```

### Report object

```python
import reports

# Select source: this is a DatabaseManager object
mydb = reports.manager('mysql', host='mysql1.local', database='login_users', username='dba', password='dba0000')
output = reports.manager('xlsx', '/home/report/error_login.xlsx', mode='w')

# Get data
mydb.execute('SELECT * FROM site_login')
site_login = mydb.fetchall()

# Create report data
report = reports.Report(site_login, title='Site login failed', filters=[400, 401, 403, 404, 500], output=output)
# Filter data
report.exec()
# Save data on file
report.export()

```

## Open source
_reports_ is an open source project. Any contribute, It's welcome.

**A great thanks**.

For donations, press this

For me

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.me/guos)

For [Telethon](http://www.telethon.it/)

The Telethon Foundation is a non-profit organization recognized by the Ministry of University and Scientific and Technological Research.
They were born in 1990 to respond to the appeal of patients suffering from rare diseases.
Come today, we are organized to dare to listen to them and answers, every day of the year.

<a href="https://www.telethon.it/sostienici/dona-ora"> <img src="https://www.telethon.it/dev/_nuxt/img/c6d474e.svg" alt="Telethon" title="Telethon" width="200" height="104" /> </a>

[Adopt the future](https://www.ioadottoilfuturo.it/)


## Acknowledgments

Thanks to Mark Lutz for writing the _Learning Python_ and _Programming Python_ books that make up my python foundation.

Thanks to Kenneth Reitz and Tanya Schlusser for writing the _The Hitchhiker’s Guide to Python_ books.

Thanks to Dane Hillard for writing the _Practices of the Python Pro_ books.

Special thanks go to my wife, who understood the hours of absence for this development. 
Thanks to my children, for the daily inspiration they give me and to make me realize, that life must be simple.

Thanks Python!