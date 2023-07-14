#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# cli -- pyreports
#
#     Copyright (C) 2023 Matteo Guadrini <matteo.guadrini@hotmail.it>
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
__version__ = '1.5.1'


# endregion

# region functions
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='pyreports command line interface (CLI)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='Full docs here: https://pyreports.readthedocs.io/en/latest/dev/cli.html'
    )

    parser.add_argument('config',
                        metavar='CONFIG_FILE',
                        default=sys.stdin,
                        type=argparse.FileType('rt', encoding="utf-8"),
                        help='YAML configuration file')
    parser.add_argument('-e', '--exclude',
                        help='Excluded title report list',
                        nargs=argparse.ZERO_OR_MORE,
                        default=[],
                        metavar='TITLE')
    parser.add_argument('-v', '--verbose', help='Enable verbose mode', action='store_true')
    parser.add_argument('-V', '--version', help='Print version', action='version', version=__version__)

    args = parser.parse_args()
    filename = args.config.name

    # Check if file is a YAML file
    try:
        args.config = load_config(args.config)
    except yaml.YAMLError as err:
        parser.error(f'file {filename} is not a valid YAML file: \n{err}')

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
            raise yaml.YAMLError(
                'one of "report" section does not have "input" section'
            )
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
    elif manager.type == 'sql':
        if params and isinstance(params, (list, tuple)):
            manager.execute(*params)
            data = manager.fetchall()
        elif params and isinstance(params, dict):
            manager.execute(**params)
            data = manager.fetchall()
    # LdapManager
    elif manager.type == 'ldap':
        if params and isinstance(params, (list, tuple)):
            data = manager.query(*params)
        elif params and isinstance(params, dict):
            data = manager.query(**params)
    # NosqlManager
    elif manager.type == 'nosql':
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

    print_verbose(f'found {len(config.get("reports", ()))} report(s)',
                  verbose=args.verbose)

    # Build the data and report
    for report in reports:
        # Check if report isn't in excluded list
        if args.exclude and report.get('report').get('title') in args.exclude:
            print_verbose(f'exclude report "{report.get("report").get("title")}"',
                          verbose=args.verbose)
            continue
        # Make a manager object
        input_ = report.get('report').get('input')
        print_verbose(f'make an input manager of type {input_.get("manager")}',
                      verbose=args.verbose)
        manager = make_manager(input_)
        # Get data
        print_verbose(f'get data from manager {manager}', verbose=args.verbose)
        try:
            # Make a report object
            data = get_data(manager, input_.get('params'))
            if 'map' in report.get('report'):
                exec(report.get('report').get('map'))
            map_func = globals().get('map_func')
            report_ = pyreports.Report(
                input_data=data,
                title=report.get('report').get('title'),
                filters=report.get('report').get('filters'),
                map_func=map_func,
                negation=report.get('report').get('negation', False),
                column=report.get('report').get('column'),
                count=report.get('report').get('count', False),
                output=make_manager(report.get('report').get('output')) if 'output' in report.get('report') else None
            )
            print_verbose(f'created report "{report_.title}"', verbose=args.verbose)
        except Exception as err:
            pyreports.Report(tablib.Dataset())
            exit(f'error: {err}')
        # Check output
        if report_.output:
            # Check if export or send report
            if report.get('report').get('mail'):
                print_verbose(f'send report to {report.get("report").get("mail").get("to")}', verbose=args.verbose)
                mail_settings = report.get('report').get('mail')
                report_.send(
                    server=mail_settings.get('server'),
                    _from=mail_settings.get('from'),
                    to=mail_settings.get('to'),
                    cc=mail_settings.get('cc'),
                    bcc=mail_settings.get('bcc'),
                    subject=mail_settings.get('subject'),
                    body=mail_settings.get('body'),
                    auth=tuple(mail_settings.get('auth')) if 'auth' in mail_settings else None,
                    _ssl=bool(mail_settings.get('ssl')),
                    headers=mail_settings.get('headers')
                )
            else:
                print_verbose(f'export report to {report_.output}',
                              verbose=args.verbose)
                report_.export()
        else:
            # Print report in stdout
            print_verbose('print report to stdout', verbose=args.verbose)
            title = report.get('report').get('title')
            report_.exec()
            print(f"{title}\n{'=' * len(title)}\n")
            print(report_)


# endregion

# region main
if __name__ == '__main__':
    main()

# endregion
