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


class SymbiFlow:
    """Class which solves HDL-to-bitstream based on FOSS."""

    def __init__(self, name='symbiflow', part='hx8k-ct256', outdir='.'):
        """Class constructor."""
        self.name = name
        self.part = get_info(part)
        self.outdir = outdir
        self.engine = 'none'
        self.options = None

    def set_oci(self, engine, options):
        """Set the OCI engine and its options."""
        self.engine = engine
        self.options = options

    # pylint: disable=too-many-arguments
    def synthesis(self, top, vhdl=None, vlog=None, slog=None, scf=None,
                  param=None, arch=None, define=None, include=None):
        """Performs synthesis."""
        print(self.name)
        print(self.part)
        print(top)
        print(vhdl)
        print(vlog)
        print(slog)
        print(scf)
        print(arch)
        print(define)
        print(param)
        print(include)

    def implementation(self, icf=None):
        """Performs implementation."""
        print(self.name)
        print(self.part)
        print(icf)

    def bitstream(self):
        """Performs bitstream generation."""
        print(self.name)
        print(self.part)


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
    # Finish
    return {
        'family': family, 'device': device, 'package': package
    }
