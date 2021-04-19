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

"""A CLI utility to perform bitstream generation based on FOSS."""

import argparse

from openflow import __version__ as version


def main():
    """Solves the main functionality of this utility."""

    # Parsing the command-line.

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='v{}'.format(version)
    )

    # project
    # outdir

    # part

    # enable
    # engine
    # container
    # options
    # tool

    args = parser.parse_args()


if __name__ == "__main__":
    main()
