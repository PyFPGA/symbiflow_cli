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
import logging
import sys
from symbiflow import __version__ as version
from symbiflow.symbiflow import SymbiFlow


ALL_DESC = 'Performs from synthesis to bitstream generation'
SYN_DESC = 'Performs synthesis'
IMP_DESC = 'Performs implementation'
BIT_DESC = 'Performs bitstream generation'

DEF_PART = 'hx8k-ct256'
DEF_OUTDIR = '.'
DEF_OCI_OPTIONS = '-v $HOME:$HOME -w $PWD'

COMMANDS = ['all', 'syn', 'imp', 'bit']


def cli():
    """Parse the CLI arguments"""

    #
    # Groups of arguments
    #

    # Arguments shared by all the sub-commands

    args_shared = argparse.ArgumentParser(add_help=False)

    args_shared.add_argument(
        'project',
        help='basename for generated files'
    )

    args_shared.add_argument(
        '-p', '--part',
        metavar='FPGA',
        default=DEF_PART,
        help='name of the target FPGA part [{}]'.format(DEF_PART)
    )

    args_shared.add_argument(
        '-o', '--outdir',
        metavar='PATH',
        default=DEF_OUTDIR,
        help='location for generated files [{}]'.format(DEF_OUTDIR)
    )

    args_shared.add_argument(
        "--oci-engine",
        choices=['none', 'docker', 'podman'],
        help='OCI engine internally employed'
    )

    args_shared.add_argument(
        "--oci-options",
        metavar='OPTIONS_BETWEEN_QUOTATION_MARKS',
        default=DEF_OCI_OPTIONS,
        help='options for the OCI engine [{}]'.format(DEF_OCI_OPTIONS)
    )

    # Arguments for synthesis

    args_for_syn = argparse.ArgumentParser(add_help=False)

    args_for_syn.add_argument(
        '-t', '--top',
        metavar='NAME',
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
        metavar='FILE',
        nargs='+',
        help='Verilog files'
    )

    args_for_syn.add_argument(
        '--slog',
        metavar='FILE',
        nargs='+',
        help='System Verilog files'
    )

    args_for_syn.add_argument(
        '--scf',
        metavar='FILE',
        nargs='+',
        help='Synthesis Constraint Files'
    )

    # Arguments for implementation

    args_for_imp = argparse.ArgumentParser(add_help=False)
    args_for_imp.add_argument(
        '--icf',
        metavar='FILE',
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

    subparsers = parser.add_subparsers(
        dest='command',
        # required=True, # added in Python 3.7
        help='Available commands'
    )

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

    args = parser.parse_args()

    #
    # Check arguments
    #

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    if args.command not in COMMANDS:
        logging.critical('specify an available command %s', COMMANDS)
        sys.exit()

    #
    # Invoke the tools
    #

    prj = SymbiFlow(args.project, args.part, args.outdir)
    prj.set_oci(args.oci_engine, args.oci_options)
    if args.command == 'all':
        prj.synthesis(args.top, args.vhdl, args.vlog, args.slog, args.scf,
                      args.param, args.arch, args.define, args.include)
        prj.implementation(args.icf)
        prj.bitstream()
    elif args.command == 'syn':
        prj.synthesis(args.top, args.vhdl, args.vlog, args.slog, args.scf,
                      args.param, args.arch, args.define, args.include)
    elif args.command == 'imp':
        prj.implementation(args.icf)
    else:  # 'bit':
        prj.bitstream()


if __name__ == "__main__":
    cli()
