#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021  Rodrigo A. Melo
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC

"""symbiflow.oci

A Class to configure the underlying containers employed by SymbiFlow CLI.
"""


import argparse
import os
from yaml import safe_load, dump
from symbiflow import __version__ as version


class OCI:
    """Configure the containers employed by SymbiFlow CLI."""

    def __init__(self, filename='oci.yml'):
        """Class constructor."""
        homefile = os.path.join(os.path.expanduser('~'), filename)
        projfile = os.path.join(os.path.dirname(__file__), 'oci.yml')
        if os.path.exists(filename):
            filepath = filename
        elif os.path.exists(homefile):
            filepath = homefile
        else:
            filepath = projfile
        self.oci = {}
        with open(filepath, 'r') as file:
            self.oci = safe_load(file)

    def get_command(self, tool):
        """Get the command-line needed to run a tool."""
        engine = self.oci['engine']['name']
        name = self.oci['tools'][tool]['name']
        if engine is not None:
            oci = [
              engine,
              'run --rm',
              '-v ' + (' -v ').join(self.oci['engine']['volumes']),
              '-w ' + self.oci['engine']['work'],
              self.oci['engine'].get('options', None),
              self.oci['tools'][tool].get('options', None),
              self.oci['tools'][tool]['container'],
              name
            ]
            return ' '.join(list(filter(None, oci)))
        return name

    def get_tools(self):
        """Returns the list of configured tools."""
        return sorted(list(self.oci['tools'].keys()))

    def dump(self):
        """Dumps the configuration in YAML format (debug purpouses)."""
        return dump(self.oci)

    def set_engine(self, engine):
        """Set the OCI engine."""
        self.oci['engine']['name'] = engine

    def unset_engine(self):
        """Unset the OCI engine. """
        self.oci['engine']['name'] = None

    def set_volumes(self, volumes):
        """Set the volumes of the OCI engine."""
        self.oci['engine']['volumes'] = volumes

    def set_work(self, work):
        """Set the working directory inside the container."""
        self.oci['engine']['work'] = work

    def set_global_options(self, options):
        """Set options shared by all the containers."""
        self.oci['engine']['options'] = options

    def set_container(self, tool, container):
        """Set the container of the specified tool."""
        self.oci['tools'][tool]['container'] = container

    def set_name(self, tool, name):
        """Set the name of the specified tool."""
        self.oci['tools'][tool]['name'] = name

    def set_local_options(self, tool, options):
        """Set options for a particular container."""
        self.oci['tools'][tool]['options'] = options


def main():
    """Utility to test the Tool class of SymbiFlow."""

    cfg = OCI()

    # Parsing the command-line.

    parser = argparse.ArgumentParser(
        description=main.__doc__
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='v{}'.format(version)
    )

    parser.add_argument(
        'tool',
        metavar='TOOL',
        choices=cfg.get_tools(),
        help=', '.join(cfg.get_tools())
    )

    args = parser.parse_args()

    # Solving the functionality

    print(cfg.get_command(args.tool))


if __name__ == "__main__":
    main()
