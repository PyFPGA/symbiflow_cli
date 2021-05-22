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

"""SymbiFlow CLI"""

import argparse
from fpga import __version__ as version

ALL_DESC = 'Performs from synthesis to bitstream generation'
SYN_DESC = 'Performs synthesis'
IMP_DESC = 'Performs implementation'
BIT_DESC = 'Performs bitstream generation'


def cli():
    """Parse the CLI arguments"""

    #
    # Groups of arguments
    #

    # Arguments shared by all the sub-commands

    args_shared = argparse.ArgumentParser(add_help=False)

    args_shared.add_argument(
        'name',
        help='basename for generated files (project name)'
    )

    args_shared.add_argument(
        '-p', '--part',
        default='TODO',
        help='target FPGA part'
    )

    args_shared.add_argument(
        '-o', '--outdir',
        default='.',
        help='location for generated files'
    )

    args_shared.add_argument(
        "--oci-engine",
        choices=['none', 'docker', 'podman'],
        help='OCI engine internally employed'
    )

    args_shared.add_argument(
        "--oci-options",
        default='-v $HOME:$HOME -w $PWD',
        help='options for the OCI engine (a string between quotation marks)'
    )

    # Arguments for synthesis

    args_for_syn = argparse.ArgumentParser(add_help=False)

    args_for_syn.add_argument(
        '-t', '--top',
        help='specify a top-level name'
    )

    args_for_syn.add_argument(
        '--param',
        metavar='PARAM:VALUE',
        nargs='*',
        help='specify top-level Generics/Parameters'
    )

    args_for_syn.add_argument(
        '--arch',
        metavar='ARCHITECTURE',
        help='specify a VHDL top-level Architecture'
    )

    args_for_syn.add_argument(
        '--define',
        metavar='DEFINE:VALUE',
        nargs='*',
        help='specify [System] Verilog Defines'
    )

    args_for_syn.add_argument(
        '--include',
        metavar='PATH',
        nargs='*',
        help='specify [System] Verilog Include Paths'
    )

    args_for_syn.add_argument(
        '--vhdl',
        metavar='FILE[,LIBRARY]',
        nargs='+',
        help='VHDL files'
    )

    args_for_syn.add_argument(
        '--vlog',
        nargs='+',
        help='Verilog files'
    )

    args_for_syn.add_argument(
        '--slog',
        nargs='+',
        help='System Verilog files'
    )

    args_for_syn.add_argument(
        '--scf',
        nargs='+',
        help='Synthesis Constraint Files'
    )

    # Arguments for implementation

    args_for_imp = argparse.ArgumentParser(add_help=False)
    args_for_imp.add_argument(
        '--icf',
        nargs='+',
        help='Implementation Constraint Files'
    )

    #
    # Parse
    #

    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='v{}'.format(version)
    )

    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(
        'all',
        description=ALL_DESC,
        help=ALL_DESC,
        parents=[args_for_syn, args_for_imp, args_shared]
    )

    subparsers.add_parser(
        'syn',
        description=SYN_DESC,
        help=SYN_DESC,
        parents=[args_for_syn, args_shared]
    )

    subparsers.add_parser(
        'imp',
        description=IMP_DESC,
        help=IMP_DESC,
        parents=[args_for_imp, args_shared]
    )

    subparsers.add_parser(
        'bit',
        description=BIT_DESC,
        help=BIT_DESC,
        parents=[args_shared]
    )

    return parser.parse_args()


if __name__ == "__main__":
    print(cli())
