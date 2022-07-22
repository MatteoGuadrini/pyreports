#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# cli -- pyreports
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

"""Command line interface"""

# region imports
import sys
import tablib
import yaml
import argparse
import pyreports

# endregion

# region globals
__version__ = '1.4.0'


# endregion

# region functions
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='pyreports command line interface (CLI)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('config',
                        metavar='CONFIG_FILE',
                        default=sys.stdin,
                        type=argparse.FileType('rt', encoding="utf-8"),
                        help='Config file')
    parser.add_argument('-v', '--verbose', help='Enable verbose mode', action='store_true')
    parser.add_argument('-V', '--version', help='Print version', version=__version__)

    args = parser.parse_args()
    filename = args.config.name

    # Check if file is a YAML file
    try:
        args.config = load_config(args.config)
    except yaml.YAMLError as err:
        parser.error(f'file {args.config} is not a valid YAML file: {err}')

    # Validate config file
    try:
        validate_config(args.config)
    except yaml.YAMLError as err:
        parser.error(str(err))

    print_verbose(f'parsed YAML file {filename}', verbose=args.verbose)

    return args


def load_config(yaml_file):
    """Load configuration file

    :param yaml_file: opened yaml file
    :return: Any
    """
    with yaml_file as file:
        return yaml.safe_load(file)


def validate_config(config):
    """Validate config object

    :param config: YAML config object
    :return: None
    """
    try:
        reports = config['reports']
        if reports is None or not isinstance(reports, list):
            raise yaml.YAMLError('"reports" section have not "report" list sections')
        datas = all([bool(report.get('report').get('input')) for report in reports])
        if not datas:
            raise yaml.YAMLError('one of "report" section does not have "input" section')
    except KeyError as err:
        raise yaml.YAMLError(f'there is no "{err}" section')
    except AttributeError:
        raise yaml.YAMLError('correctly indents the "report" section or "report" section not exists')


def make_manager(input_config):
    """Make Manager object

    :param input_config: file, sql or nosql report configuration
    :return: manager
    """

    type_ = input_config.get('manager')

    if type_ in pyreports.io.FILETYPE:
        manager = pyreports.manager(input_config.get('manager'), input_config.get('filename', ()))
    else:
        manager = pyreports.manager(input_config.get('manager'), **input_config.get('source', {}))

    return manager


def get_data(manager, params=None):
    """Get Dataset from source

    :param manager: Manager object
    :param params: parameter used into call of method in Manager object
    :return: Dataset
    """
    if params is None:
        params = ()
    data = None
    # FileManager
    if manager.type == 'file':
        if params and isinstance(params, (list, tuple)):
            data = manager.read(*params)
        elif params and isinstance(params, dict):
            data = manager.read(**params)
        else:
            data = manager.read()
    # DatabaseManager
    elif manager.type == 'database':
        if params and isinstance(params, (list, tuple)):
            data = manager.execute(*params)
        elif params and isinstance(params, dict):
            data = manager.execute(**params)
    # LdapManager
    elif manager.type == 'ldap':
        if params and isinstance(params, (list, tuple)):
            data = manager.query(*params)
        elif params and isinstance(params, dict):
            data = manager.query(**params)
    # NosqlManager
    else:
        if params and isinstance(params, (list, tuple)):
            data = manager.find(*params)
        elif params and isinstance(params, dict):
            data = manager.find(**params)

    return data


def print_verbose(*messages, verbose=False):
    """Print messages if verbose is True

    :param messages: some string messages
    :param verbose: enable or disable verbosity
    :return: None
    """
    if verbose:
        print('info:', *messages)


def main():
    """Main logic"""

    # Get command line args
    args = get_args()
    # Take reports
    config = args.config
    reports = config.get('reports', ())

    print_verbose(f'found {len(config.get("reports", ()))} report(s)', verbose=args.verbose)

    # Build the data and report
    for report in reports:
        # Make a manager object
        input_ = report.get('report').get('input')
        print_verbose(f'make an input manager of type {input_.get("manager")}', verbose=args.verbose)
        manager = make_manager(input_)
        # Get data
        print_verbose(f'get data from manager {manager}', verbose=args.verbose)
        data = get_data(manager, input_.get('params'))
        try:
            # Make a report object
            exec(report.get('report').get('map'))
            map_func = globals()['map_func']
            report_ = pyreports.Report(
                input_data=data,
                title=report.get('report').get('title'),
                filters=report.get('report').get('filters'),
                map_func=map_func,
                column=report.get('report').get('column'),
                count=report.get('report').get('count', False),
                output=make_manager(report.get('report').get('output'))
            )
            print_verbose(f'created report {report_.title}', verbose=args.verbose)
        except pyreports.exception.ReportException as err:
            exit(f'error: {err}')
        finally:
            report_ = pyreports.Report(tablib.Dataset())
        # Check output
        if report_.output:
            # Check if export or send report
            if report.get('report').get('mail'):
                print_verbose(f'send report to {report.get("report").get("mail").get("to")}', verbose=args.verbose)
                report_.send(
                    server=report.get('report').get('mail').get('server'),
                    _from=report.get('report').get('mail').get('from'),
                    to=report.get('report').get('mail').get('to'),
                    cc=report.get('report').get('mail').get('cc'),
                    bcc=report.get('report').get('mail').get('bcc'),
                    subject=report.get('report').get('mail').get('subject'),
                    body=report.get('report').get('mail').get('body'),
                    auth=tuple(report.get('report').get('mail').get('auth')),
                    _ssl=bool(report.get('report').get('mail').get('ssl')),
                    headers=report.get('report').get('mail').get('headers')
                )
            else:
                print_verbose(f'export report to {report_.output.data.file}', verbose=args.verbose)
                report_.export()
        else:
            # Print report in stdout
            print_verbose(f'print report to stdout', verbose=args.verbose)
            title = report.get('report').get('title')
            print(f"{title}\n{'=' * len(title)}\n")
            print(report_)


# endregion

# region main
if __name__ == '__main__':
    main()

# endregion
