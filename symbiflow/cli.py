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
import errno
import logging
import sys
from symbiflow import __version__ as version
from symbiflow.symbiflow import SymbiFlow


_ALL_DESC = 'Performs from synthesis to bitstream generation'
_SYN_DESC = 'Performs synthesis'
_PNR_DESC = 'Performs place and route'
_BIT_DESC = 'Performs bitstream generation'
_PGM_DESC = 'Performs programming'

_DEF_PROJECT = 'symbiflow'
_DEF_PART = 'hx8k-ct256'
_DEF_OUTDIR = '.'
_DEF_OCI_VOLUMES = '$HOME:$HOME'
_DEF_OCI_WORK = '$PWD'

_COMMANDS = ['all', 'syn', 'pnr', 'bit', 'pgm']


# pylint: disable=too-many-statements
def main():
    """Parse the CLI arguments"""

    #
    # Groups of arguments
    #

    # Arguments shared by all the sub-commands

    args_shared = argparse.ArgumentParser(add_help=False)

    args_shared.add_argument(
        '--project',
        metavar='PROJECT',
        default=_DEF_PROJECT,
        help='basename for generated files [{}]'.format(_DEF_PROJECT)
    )

    args_shared.add_argument(
        '-p', '--part',
        metavar='FPGA',
        default=_DEF_PART,
        help='name of the target FPGA part [{}]'.format(_DEF_PART)
    )

    args_shared.add_argument(
        '-o', '--outdir',
        metavar='PATH',
        default=_DEF_OUTDIR,
        help='location for generated files [{}]'.format(_DEF_OUTDIR)
    )

    args_shared.add_argument(
        "--oci-engine",
        default=None,
        choices=[None, 'docker', 'podman'],
        help='OCI engine internally employed [None]'
    )

    args_shared.add_argument(
        "--oci-volumes",
        metavar='HOST-DIR:CONT-DIR',
        action='append',
        default=[_DEF_OCI_VOLUMES],
        help='volumes for the OCI engine [{}]'.format(_DEF_OCI_VOLUMES)
    )

    args_shared.add_argument(
        "--oci-work",
        metavar='WORK',
        default=_DEF_OCI_WORK,
        help='working directory for the OCI engine [{}]'.format(_DEF_OCI_WORK)
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
        metavar=('PARAM', 'VALUE'),
        action='append',
        nargs=2,
        help='specify top-level Generics/Parameters'
    )

    args_for_syn.add_argument(
        '--arch',
        metavar='ARCHITECTURE',
        help='specify a VHDL top-level Architecture'
    )

    args_for_syn.add_argument(
        '--define',
        metavar=('DEFINE', 'VALUE'),
        action='append',
        nargs=2,
        help='specify [System] Verilog Defines'
    )

    args_for_syn.add_argument(
        '--include',
        metavar='PATH',
        action='append',
        help='specify a [System] Verilog Include Paths'
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
        action='append',
        help='Synthesis Constraint Files'
    )

    # Arguments for pnr

    args_for_pnr = argparse.ArgumentParser(add_help=False)
    args_for_pnr.add_argument(
        '--pcf',
        metavar='FILE',
        action='append',
        help='Physical Constraint Files'
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
        description=_ALL_DESC,
        help=_ALL_DESC,
        parents=[args_for_syn, args_for_pnr, args_shared]
    )

    subparsers.add_parser(
        'syn',
        description=_SYN_DESC,
        help=_SYN_DESC,
        parents=[args_for_syn, args_shared]
    )

    subparsers.add_parser(
        'pnr',
        description=_PNR_DESC,
        help=_PNR_DESC,
        parents=[args_for_pnr, args_shared]
    )

    subparsers.add_parser(
        'bit',
        description=_BIT_DESC,
        help=_BIT_DESC,
        parents=[args_shared]
    )

    subparsers.add_parser(
        'pgm',
        description=_PGM_DESC,
        help=_PGM_DESC,
        parents=[args_shared]
    )

    args = parser.parse_args()

    #
    # Check arguments
    #

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    if args.command not in _COMMANDS:
        logging.critical('please specify an available command %s', _COMMANDS)
        sys.exit(errno.EPERM)
    if args.command in ['all', 'syn']:
        if args.vhdl == args.vlog == args.slog is None:
            logging.critical('please provide at least one HDL file')
            sys.exit(errno.ENOENT)
        if args.slog is not None:
            logging.critical('System Verilog is not yet supported')
            sys.exit(errno.ENOSYS)
        if args.scf is not None:
            logging.critical('Synthesis Constraints are not yet supported')
            sys.exit(errno.ENOSYS)

    #
    # Invoke the tools
    #

    prj = SymbiFlow(args.project, args.part, args.outdir)
    prj.set_oci(args.oci_engine, args.oci_volumes, args.oci_work)
    if args.command in ['all', 'syn']:
        prj.synthesis(args.top, args.vhdl, args.vlog, args.slog, args.scf,
                      args.param, args.arch, args.define, args.include)
    if args.command in ['all', 'pnr']:
        prj.pnr(args.pcf)
    if args.command in ['all', 'bit']:
        prj.bitstream()
    if args.command == 'pgm':
        prj.programming()


if __name__ == "__main__":
    main()
