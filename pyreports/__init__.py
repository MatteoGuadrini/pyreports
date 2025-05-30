#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# __init__ -- pyreports
#
#     Copyright (C) 2025 Matteo Guadrini <matteo.guadrini@hotmail.it>
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

"""Build complex reports from/to various formats."""

__version__ = "1.8.0"

from .io import manager, READABLE_MANAGER, WRITABLE_MANAGER  # noqa: F401
from .core import Executor, Report, ReportBook  # noqa: F401
from .exception import ReportDataError, ReportManagerError, DataObjectError  # noqa: F401
from .datatools import (
    average,  # noqa: F401
    most_common,  # noqa: F401
    percentage,  # noqa: F401
    counter,  # noqa: F401
    aggregate,  # noqa: F401
    chunks,  # noqa: F401
    merge,  # noqa: F401
    deduplicate,  # noqa: F401
    subset,  # noqa: F401
    sort,  # noqa: F401
    DataObject,  # noqa: F401
    DataAdapters,  # noqa: F401
    DataPrinters,  # noqa: F401
)
from .cli import make_manager, get_data, load_config, validate_config  # noqa: F401
