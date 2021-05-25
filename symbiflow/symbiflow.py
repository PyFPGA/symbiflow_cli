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

"""symbiflow.symbiflow

A Python Package which solves HDL-to-bitstream based on FOSS.
"""

import subprocess
from pathlib import Path


class SymbiFlow:
    """Class which solves HDL-to-bitstream based on FOSS."""

    def __init__(self, project='symbiflow', part='hx8k-ct256', outdir='.'):
        """Class constructor."""
        self.project = project
        self.part = get_info(part)
        self.outdir = outdir
        self.engine = 'none'
        self.options = None
        Path(self.outdir).mkdir(parents=True, exist_ok=True)

    def set_oci(self, engine, options):
        """Set the OCI engine and its options."""
        self.engine = engine
        self.options = options

    # pylint: disable=too-many-arguments
    # pylint: disable=unused-argument
    # pylint: disable=too-many-locals
    def synthesis(self, top, vhdl=None, vlog=None, slog=None, scf=None,
                  param=None, arch=None, define=None, include=None):
        """Performs synthesis."""
        if vhdl is None and vlog is None and slog is None:
            raise FileNotFoundError()
        # print(slog)
        # print(scf)
        # print(arch)
        # print(define)
        # print(param)
        # print(include)
        # Prepare OCI
        oci = read_template('oci').format(
            engine=self.engine,
            options=self.options,
            container='hdlc/ghdl:yosys'
        ) + ' ' if self.engine is not None else ''
        # Prepare and run GHDL analysis
        if vhdl is not None:
            for file in vhdl:
                aux = file.split(',')
                library = '--work={}'.format(aux[1]) if len(aux) > 1 else ''
                cmd = oci + read_template('ghdl-a').format(
                     outdir=self.outdir,
                     library=library,
                     file=aux[0]
                )
                _run(cmd)
        # Prepare and run Yosys synthesis
        files = []
        if vlog is not None:
            for file in vlog:
                files.append('read_verilog {}'.format(file))
        if vhdl is not None:
            files = [read_template('ghdl-synth').format(
                 outdir=self.outdir,
                 unit=top,
                 arch=''
            )]
        family = self.part['family']
        cmd = oci
        cmd += read_template('yosys-{}'.format(family)).format(
            module='-m ghdl' if vhdl is not None else '',
            includes='',
            files='; '.join(files),
            params='',
            top=top,
            outdir=self.outdir,
            project=self.project
        )
        _run(cmd)

    def implementation(self, icf=None):
        """Performs implementation."""
        # print(icf)
        family = self.part['family']
        if family == 'ice40':
            ext = 'pcf'
        else:  # family == 'ecp5'
            ext = 'lpf'
        constraint = Path('.') / self.outdir / self.project
        constraint = '{}.{}'.format(constraint, ext)
        with open(constraint, 'w') as file:
            file.write('#')
        cmd = read_template('oci').format(
            engine=self.engine,
            options=self.options,
            container='hdlc/nextpnr:{}'.format(family)
        ) + ' ' if self.engine is not None else ''
        cmd += read_template('nextpnr-{}'.format(family)).format(
            device=self.part['device'],
            package=self.part['package'],
            outdir=self.outdir,
            project=self.project
        )
        _run(cmd)
        if family == 'ice40':
            cmd = read_template('oci').format(
                engine=self.engine,
                options=self.options,
                container='hdlc/icestorm'
            ) + ' ' if self.engine is not None else ''
            cmd += read_template('icetime').format(
                device=self.part['device'],
                outdir=self.outdir,
                project=self.project
            )
            _run(cmd)

    def bitstream(self):
        """Performs bitstream generation."""
        print(self.project)
        print(self.part)


def _run(command):
    """Run the specified command."""
    subprocess.run(
        command, shell=True, check=True, universal_newlines=True,
    )


def get_info(part):
    """Get info about the FPGA part.

    :param part: the FPGA part as specified by the tool
    :returns: a dictionary with the keys name, family, device and package
    """
    name = part.lower()
    # Looking for the family
    family = None
    families = [
        # From <YOSYS>/techlibs/xilinx/synth_xilinx.cc
        'xcup', 'xcu', 'xc7', 'xc6s', 'xc6v', 'xc5v', 'xc4v', 'xc3sda',
        'xc3sa', 'xc3se', 'xc3s', 'xc2vp', 'xc2v', 'xcve', 'xcv'
    ]
    for item in families:
        if name.startswith(item):
            family = item
    families = [
        # From <nextpnr>/ice40/main.cc
        'lp384', 'lp1k', 'lp4k', 'lp8k', 'hx1k', 'hx4k', 'hx8k',
        'up3k', 'up5k', 'u1k', 'u2k', 'u4k'
    ]
    if name.startswith(tuple(families)):
        family = 'ice40'
    families = [
        # From <nextpnr>/ecp5/main.cc
        '12k', '25k', '45k', '85k', 'um-25k', 'um-45k', 'um-85k',
        'um5g-25k', 'um5g-45k', 'um5g-85k'
    ]
    if name.startswith(tuple(families)):
        family = 'ecp5'
    # Looking for the device and package
    device = None
    package = None
    aux = name.split('-')
    if len(aux) == 2:
        device = aux[0]
        package = aux[1]
    elif len(aux) == 3:
        device = '{}-{}'.format(aux[0], aux[1])
        package = aux[2]
    else:
        raise ValueError('Part must be DEVICE-PACKAGE')
    if family == 'ice40' and device.endswith('4k'):
        # See http://www.clifford.at/icestorm/
        device = device.replace('4', '8')
        package += ":4k"
    if family == 'ecp5':
        package = package.upper()
    # Finish
    return {
        'family': family, 'device': device, 'package': package
    }


def read_template(name):
    """Read the specified template file."""
    template = Path(__file__).parent / 'templates' / name
    with open(template, 'r') as file:
        return file.read().strip()
