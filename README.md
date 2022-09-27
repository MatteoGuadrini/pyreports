# pyreports

<img src="https://pyreports.readthedocs.io/en/latest/_static/pyreports.svg" alt="pyreports" title="pyreports" width="300" height="300" />

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/2bad30d308414c83836f22f012c98649)](https://www.codacy.com/gh/MatteoGuadrini/pyreports/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MatteoGuadrini/pyreports&amp;utm_campaign=Badge_Grade)
[![CircleCI](https://circleci.com/gh/MatteoGuadrini/pyreports.svg?style=svg)](https://circleci.com/gh/MatteoGuadrini/pyreports)

_pyreports_ is a python library that allows you to create complex reports from various sources such as databases, 
text files, ldap, etc. and perform processing, filters, counters, etc. 
and then export or write them in various formats or in databases.

## Test package

To test the package, follow these instructions:

```console
$ git clone https://github.com/MatteoGuadrini/pyreports.git
$ cd pyreports
$ python -m unittest discover tests
```

## Install package

To install package, follow these instructions:

```console
$ pip install pyreports #from pypi

$ git clone https://github.com/MatteoGuadrini/pyreports.git #from official repo
$ cd pyreports
$ python setup.py install
```

## Why choose this library?

_pyreports_ wants to be a library that simplifies the collection of data from multiple sources such as databases, 
files and directory servers (through LDAP), the processing of them through built-in and customized functions, 
and the saving in various formats (or, by inserting the data in a database).

## How does it work

_pyreports_ uses the [**tablib**](https://tablib.readthedocs.io/en/stable/) library to organize the data into _Dataset_ object.

### Simple report

I take the data from a database table, filter the data I need and save it in a csv file

```python
import pyreports

# Select source: this is a DatabaseManager object
mydb = pyreports.manager('mysql', host='mysql1.local', database='login_users', user='dba', password='dba0000')

# Get data
mydb.execute('SELECT * FROM site_login')
site_login = mydb.fetchall()

# Filter data
error_login = pyreports.Executor(site_login)
error_login.filter([400, 401, 403, 404, 500])

# Save report: this is a FileManager object
output = pyreports.manager('csv', '/home/report/error_login.csv')
output.write(error_login.get_data())

```

### Combine source

I take the data from a database table, and a log file, and save the report in json format

```python
import pyreports

# Select source: this is a DatabaseManager object
mydb = pyreports.manager('mysql', host='mysql1.local', database='login_users', user='dba', password='dba0000')
# Select another source: this is a FileManager object
mylog = pyreports.manager('file', '/var/log/httpd/error.log')

# Get data
mydb.execute('SELECT * FROM site_login')
site_login = mydb.fetchall()
error_log = mylog.read()

# Filter database
error_login = pyreports.Executor(site_login)
error_login.filter([400, 401, 403, 404, 500])
users_in_error = set(error_login.select_column('users'))

# Prepare log
myreport = dict()
log_user_error = pyreports.Executor(error_log)
log_user_error.filter(list(users_in_error))
for line in log_user_error:
    for user in users_in_error:
        myreport.setdefault(user, [])
        myreport[user].append(line)

# Save report: this is a FileManager object
output = pyreports.manager('json', '/home/report/error_login.json')
output.write(myreport)

```

### Report object

```python
import pyreports

# Select source: this is a DatabaseManager object
mydb = pyreports.manager('mysql', host='mysql1.local', database='login_users', user='dba', password='dba0000')
output = pyreports.manager('xlsx', '/home/report/error_login.xlsx', mode='w')

# Get data
mydb.execute('SELECT * FROM site_login')
site_login = mydb.fetchall()

# Create report data
report = pyreports.Report(site_login, title='Site login failed', filters=[400, 401, 403, 404, 500], output=output)
# Filter data
report.exec()
# Save data on file
report.export()

```

### ReportBook collection object

```python
import pyreports

# Select source: this is a DatabaseManager object
mydb = pyreports.manager('mysql', host='mysql1.local', database='login_users', user='dba', password='dba0000')

# Get data
mydb.execute('SELECT * FROM site_login')
site_login = mydb.fetchall()

# Create report data
report_failed = pyreports.Report(site_login, title='Site login failed', filters=[400, 401, 403, 404, 500])
report_success = pyreports.Report(site_login, title='Site login success', filters=[200, 201, 202, 'OK'])
# Filter data
report_failed.exec()
report_success.exec()
# Create my ReportBook object
my_report = pyreports.ReportBook([report_failed, report_success])
# Save data on Excel file, with two worksheet ('Site login failed' and 'Site login success')
my_report.export(output='/home/report/site_login.xlsx')

```

## Tools for dataset

This library includes many tools for handling data received from databases and files. 
Here are some practical examples of data manipulation.

```python
import pyreports

# Select source: this is a DatabaseManager object
mydb = pyreports.manager('mysql', host='mysql1.local', database='login_users', user='dba', password='dba0000')

# Get data
mydb.execute('SELECT * FROM site_login')
site_login = mydb.fetchall()

# Most common error
most_common_error_code = pyreports.most_common(site_login, 'code')  # args: Dataset, column name
print(most_common_error_code)   # 200

# Percentage of error 404
percentage_error_404 = pyreports.percentage(site_login, 404)    # args: Dataset, filter
print(percentage_error_404)   # 16.088264794 (percent)

# Count every error code
count_error_code = pyreports.counter(site_login, 'code')  # args: Dataset, column name
print(count_error_code)   # Counter({200: 4032, 201: 42, 202: 1, 400: 40, 401: 38, 403: 27, 404: 802, 500: 3})
```

### Command line

```console
$ cat car.yml
reports:
- report:
  title: 'Red ford machine'
  input:
    manager: 'mysql'
    source:
    # Connection parameters of my mysql database
      host: 'mysql1.local'
      database: 'cars'
      user: 'admin'
      password: 'dba0000'
    params:
      query: 'SELECT * FROM cars WHERE brand = %s AND color = %s'
      params: ['ford', 'red']
  # Filter km
  filters: [40000, 45000]
  output:
    manager: 'csv'
    filename: '/tmp/car_csv.csv'

$ report car.yaml
```

## Official docs

In the following links there is the [official documentation](https://pyreports.readthedocs.io/en/latest/), for the use and development of the library.

* Managers: [doc](https://pyreports.readthedocs.io/en/latest/managers.html)
* Executor: [doc](https://pyreports.readthedocs.io/en/latest/executors.html)
* Report: [doc](https://pyreports.readthedocs.io/en/latest/report.html)
* data tools: [doc](https://pyreports.readthedocs.io/en/latest/datatools.html)
* examples: [doc](https://pyreports.readthedocs.io/en/latest/example.html)
* API: [io](https://pyreports.readthedocs.io/en/latest/dev/io.html), [core](https://pyreports.readthedocs.io/en/latest/dev/core.html)
* CLI: [cli](https://pyreports.readthedocs.io/en/latest/dev/cli.html)

## Open source
_pyreports_ is an open source project. Any contribute, It's welcome.

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