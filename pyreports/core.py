#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# core -- pyreports
#
#     Copyright (C) 2022 Matteo Guadrini <matteo.guadrini@hotmail.it>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Contains all business logic and data processing."""

# region Imports
import os
import ssl
import tablib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from .io import FileManager
from .exception import ReportManagerError, ReportDataError


# endregion

# region Classes

class Executor:

    """Executor receives, processes, transforms and writes data"""

    def __init__(self, data, header=None):
        """Create Executor object

        :param data: everything type of data
        :param header: list header of data
        """
        self.data = tablib.Dataset(*data) if not isinstance(data, tablib.Dataset) else data
        # Set header
        if header or header is None:
            self.headers(header)
        self.origin = tablib.Dataset()
        self.origin.extend(self.data)

    def __len__(self):
        """Count data

        :return: integer
        """
        return self.count_rows()

    def __iter__(self):
        """Iterate over dataset

        :return: next value
        """
        return (row for row in self.data)

    def __str__(self):
        """Pretty representation of Executor object

        :return: string
        """
        return str(self.data)

    def __getitem__(self, item):
        """Get row into Dataset object

        :param item: row (int)
        :return: row
        """
        return self.data[item]

    def __delitem__(self, key):
        """Delete row into Dataset object

        :param key: row (int)
        :return: None
        """
        del self.data[key]

    def get_data(self):
        """Get dataset

        :return: dataset
        """
        return self.data

    def reset(self):
        """Reset data to original data

        :return: None
        """
        self.data = tablib.Dataset()
        self.data.extend(self.origin)

    def headers(self, header):
        """Set header

        :param header: header of data
        :return: None
        """
        self.data.headers = header

    def filter(self, flist=None, key=None, column=None):
        """Filter data through a list of strings (equal operator) and/or function key

        :param flist: list of strings
        :param key: function that takes a single argument and returns data
        :param column: select column name or index number
        :return: None
        """
        if flist is None:
            flist = []
        ret_data = tablib.Dataset(headers=self.data.headers)
        # Filter data through filter list
        for row in self:
            for f in flist:
                if f in row:
                    ret_data.append(row)
                    break
            # Filter data through function
            if key and callable(key):
                for field in row:
                    if bool(key(field)):
                        ret_data.append(row)
                        break
        self.data = ret_data
        # Single column
        if column and self.data.headers:
            self.data = self.select_column(column)

    def map(self, key, column=None):
        """Apply function to data

        :param key: function that takes a single argument
        :param column: select column name or index number
        :return: None
        """
        if callable(key):
            ret_data = tablib.Dataset(headers=self.data.headers)
            for row in self:
                # Apply function to data
                new_row = list()
                for field in row:
                    new_row.append(key(field))
                ret_data.append(new_row)
            self.data = ret_data
        else:
            raise ValueError(f"{key} isn't function object")
        # Return all data or single column
        if column and self.data.headers:
            self.data = self.select_column(column)

    def select_column(self, column):
        """Filter dataset by column

        :param column: name or index of column
        :return: Dataset object
        """
        if isinstance(column, int):
            return self.data.get_col(column)
        else:
            return self.data[column]

    def add_column(self, column, value):
        """Add column to data

        :param column: column name
        :param value: list value for column, or function with no arguments that returns a value
        :return: None
        """
        self.data.append_col(value, header=column)

    def del_column(self, column):
        """Delete column

        :param column: column name
        :return: None
        """
        del self.data[column]

    def count_rows(self):
        """Count all rows

        :return: integer
        """
        return len(self.data)

    def count_columns(self):
        """Count all column

        :return: integer
        """
        return len(self.data.headers)

    def clone(self):
        """Clone Executor object

        :return: executor
        """
        return Executor(self.origin, header=self.origin.headers)


class Report:

    """Report represents the workflow for generating a report"""

    def __init__(self,
                 input_data: tablib.Dataset,
                 title=None,
                 filters=None,
                 map_func=None,
                 column=None,
                 count=False,
                 output: FileManager = None):
        """Create Report object

        :param input_data: Dataset object
        :param title: title of Report object
        :param filters: list or function for filter data
        :param map_func: function for modifying data
        :param column: select column name or index
        :param count: count rows
        :param output: FileManager object
        """
        # Discard all objects that are not Datasets
        if isinstance(input_data, tablib.Dataset):
            self.data = input_data
        else:
            raise ReportDataError('Only Dataset object is allowed for input')
        # Set other arguments
        self.title = title
        self.filter = filters
        self.map = map_func
        self.column = column
        self.count = bool(count)
        if isinstance(output, FileManager) or output is None:
            self.output = output
        else:
            raise ReportManagerError('Only FileManager object is allowed for output')
        # Data for report
        self.report = None

    def __repr__(self):
        """Representation of Report object

        :return: string
        """
        return f"<Report object, title={self.title if self.title else None}>"

    def __str__(self):
        """Pretty representation of Report object

        :return: string
        """
        return str(self._print_data())

    def __bool__(self):
        """Boolean value

        :return: bool
        """
        return True if self.report else False

    def __iter__(self):
        """Return report iterator

        :return: iterable object
        """
        return (row for row in self.report)

    def _print_data(self):
        """Print data and count

        :return: data and count
        """
        if isinstance(self.report, tuple):
            out = f'{self.report[0]}\nrows: {self.report[1]}'
            return out
        else:
            return self.report

    def exec(self):
        """Create Executor object to apply filters and map function to input data

        :return: None
        """
        # Create a temporary Executor object
        ex = Executor(self.data, header=self.data.headers)
        # Apply map function
        if self.map:
            ex.map(self.map)
        # Apply filters
        if self.filter:
            if callable(self.filter):
                ex.filter(key=self.filter)
            else:
                ex.filter(self.filter)
        # Count element
        if bool(self.count):
            self.count = len(ex)
        self.report = ex.get_data()

    def export(self):
        """Process and save data on output

        :return: if count is True, return row count
        """
        # Process data before export
        self.exec()
        # Verify if output is FileManager object
        if isinstance(self.output, FileManager) or self.output is None:
            if self.output:
                self.output.write(self.report)
            else:
                print(self)
        else:
            raise ReportManagerError('the output object must be FileManager or NoneType object')

    def send(self, server, _from, to, cc=None, bcc=None, subject=None, body='', auth=None, _ssl=True, headers=None):
        """Send saved report to email

        :param server: server SMTP
        :param _from: email address 'from:'
        :param to: email address 'to:'
        :param cc: email address 'cc:'
        :param bcc: email address 'bcc:'
        :param subject: email subject. Default is report title
        :param body: email body
        :param auth: authorization tuple "(user, password)"
        :param _ssl: boolean, if True port is 465 else 25
        :param headers: more header value "(header_name, key, value)"
        :return: None
        """
        if not self.output:
            raise ReportDataError('if you want send a mail with a report in attachment, must be specified output')

        # Prepare mail header
        message = MIMEMultipart("alternative")
        message["Subject"] = self.title if not subject else subject
        message["From"] = _from
        message["To"] = to
        if cc:
            message["Cc"] = cc
        if bcc:
            message["Bcc"] = bcc
        if headers:
            message.add_header(*headers)

        # Prepare body
        part = MIMEText(body, "html")
        message.attach(part)

        # Prepare attachment
        self.export()
        attach_file_name = self.output.data.file
        attach_file = open(attach_file_name, 'rb')
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(attach_file.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach_file_name))
        message.attach(payload)

        # Prepare SMTP connection
        if _ssl:
            port = smtplib.SMTP_SSL_PORT
            protocol = smtplib.SMTP_SSL
            kwargs = {'context': ssl.create_default_context()}
        else:
            port = smtplib.SMTP_PORT
            protocol = smtplib.SMTP
            kwargs = {}
        with protocol(server, port, **kwargs) as srv:
            if auth:
                srv.login(*auth)
            srv.sendmail(_from, to, message.as_string())


class ReportBook:

    """ReportBook represent a collection of Report's object"""

    def __init__(self, reports=None, title=None):
        """Create a ReportBook object

        :param reports: Report's object list
        :param title: title of report book
        """

        if reports is None:
            self.reports = list()
        else:
            self.reports = reports
        self.title = title

    def __add__(self, other):
        """Add report object

        :param other: Report object
        :return: ReportBook
        """
        if not isinstance(other, ReportBook):
            raise ReportDataError('you can only add ReportBook object')
        self.reports.extend(other.reports)
        return self

    def __iter__(self):
        """Return report iterator

        :return: iterable object
        """
        return (report for report in self.reports)

    def __len__(self):
        """Number of Report objects

        :return: int
        """
        return len(self.reports)

    def __str__(self):
        """Pretty representation of ReportBook object

        :return: string
        """
        output = f'ReportBook {self.title if self.title else None}\n'
        output += '\n'.join('\t' + str(report.title)
                            for report in self.reports)
        return output

    def __repr__(self):
        """Representation of ReportBook object

        :return: string
        """
        return f"<ReportBook object, title={self.title if self.title else None}>"

    def __bool__(self):
        """Boolean value

        :return: bool
        """
        return True if self.reports else False

    def add(self, report: Report):
        """Add report object

        :param report: Report object
        :return: None
        """
        if not isinstance(report, Report):
            raise ReportDataError('you can only add Report object')
        self.reports.append(report)

    def remove(self, index: int = None):
        """Remove Report object, last added or index specified

        :param index: report number to remove
        :return: None
        """
        if index:
            self.reports.pop(index)
        else:
            self.reports.pop(-1)

    def export(self, output=None):
        """Save data on report output or an Excel workbook

        :param output: output path for report export
        :return: None
        """
        if output:
            # Prepare pyreports
            for report in self:
                report.exec()
            # Prepare book for export
            book = tablib.Databook(tuple([report.report for report in self]))
            # Save Excel WorkBook
            with open(output, 'wb') as f:
                f.write(book.export('xlsx'))
        else:
            for report in self:
                report.export()

    def send(self, server, _from, to, cc=None, bcc=None, subject=None, body='', auth=None, _ssl=True, headers=None):
        """Send saved report to email

        :param server: server SMTP
        :param _from: email address 'from:'
        :param to: email address 'to:'
        :param cc: email address 'cc:'
        :param bcc: email address 'bcc:'
        :param subject: email subject. Default is report title
        :param body: email body
        :param auth: authorization tuple "(user, password)"
        :param _ssl: boolean, if True port is 465 else 25
        :param headers: more header value "(header_name, key, value)"
        :return: None
        """
        for report in self:
            report.send(server, _from, to, cc=cc, bcc=bcc, subject=subject, body=body, auth=auth,
                        _ssl=_ssl, headers=headers)

# endregion
