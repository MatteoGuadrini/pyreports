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
import yaml
import argparse
from pyreports import manager


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

    args = parser.parse_args()

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


def main():
    """Main logic"""

    # Get command line args
    args = get_args()
    config = args.config

    # Build the data and report
    for report in config.get('reports', ()):
        # Get data
        input_ = report.get('report').get('input')
        manager_ = manager(input_.get('manager'), input_.get('filename', ()))
        if manager_.type == 'file':
            data = manager_.read(*input_.get('params', ()))
        elif manager_.type == 'database':
            data = manager_.execute(*input_.get('params', ()))
        else:
            data = manager_.find(*input_.get('params', ()))


# endregion

# region main
if __name__ == '__main__':
    main()

# endregion
