#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# __init__ -- pyreports
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

"""Build complex pyreports from/to various formats."""

from .io import manager, READABLE_MANAGER, WRITABLE_MANAGER
from .core import Executor, Report, ReportBook
from .exception import ReportDataError, ReportManagerError
from .datatools import average, most_common, percentage, counter, aggregate, chunks, merge, deduplicate
from .cli import make_manager, get_data, load_config, validate_config
