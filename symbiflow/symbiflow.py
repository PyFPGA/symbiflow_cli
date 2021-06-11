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

A class which provides an API to solves HDL-to-bitstream based on FOSS.
"""

import subprocess
from pathlib import Path


from symbiflow.oci import OCI
from symbiflow.fpgadb import get_info


class SymbiFlow:
    """Solves HDL-to-bitstream based on FOSS.

    :param project: the basename for generated files
    :param part: name of the target FPGA part
    :param outdir: location for generated files
    """

    def __init__(self, project='symbiflow', part='hx8k-ct256', outdir='.'):
        """Class constructor."""
        self.project = project
        self.part = get_info(part)
        self.outdir = outdir
        self.oci = OCI()
        Path(self.outdir).mkdir(parents=True, exist_ok=True)

    def set_part(self, part):
        """Set the target FPGA part.

        :param part: name of the target FPGA part
        """
        self.part = get_info(part)

    def set_oci(self, engine, volumes, work):
        """Set the OCI engine and its options.

        :param engine: OCI engine
        :param volumes: volumes for the OCI engine
        :type volumes: list
        :param work: working directory for the OCI engine
        """
        self.oci.set_engine(engine)
        self.oci.set_volumes(volumes)
        self.oci.set_work(work)

    # pylint: disable=too-many-arguments
    def synthesis(self, top, vhdl=None, vlog=None, slog=None, scf=None,
                  param=None, arch=None, define=None, include=None):
        """Performs synthesis.

        :param top: name of the top-level entity/module
        :param vhdl: VHDL files (`FILE[,LIBRARY]`)
        :type vhdl: list
        :param vlog: Verilog files
        :type vlog: list
        :param slog: System Verilog files
        :type slog: list
        :param scf: Synthesis Constraint Files
        :type scf: list
        :param param: specify top-level Generics/Parameters (`PARAM:VALUE`)
        :type param: list
        :param arch: specify a VHDL top-level Architecture
        :param define: specify [System] Verilog Defines (`DEFINE:VALUE`)
        :type define: list
        :param include: specify [System] Verilog Include Paths
        :type include: list
        :raises FileNotFoundError: when no HDL files are provided
        """
        if vhdl is None and vlog is None and slog is None:
            raise FileNotFoundError()
        if slog is not None:
            raise NotImplementedError('slog')
        if scf is not None:
            raise NotImplementedError('scf')
        if param is not None:
            raise NotImplementedError('param')
        if arch is not None:
            raise NotImplementedError('arch')
        if define is not None:
            raise NotImplementedError('define')
        if include is not None:
            raise NotImplementedError('include')
        # Prepare and run GHDL analysis
        if vhdl is not None:
            for file in vhdl:
                aux = file.split(',')
                library = '--work={}'.format(aux[1]) if len(aux) > 1 else ''
                cmd = _template('ghdl-analysis').format(
                     command=self.oci.get_command('ghdl'),
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
            files = [_template('ghdl-synth').format(
                 command='ghdl',
                 outdir=self.outdir,
                 unit=top,
                 arch=''
            )]
        cmd = _template('yosys-{}'.format(self.part['family'])).format(
            command=self.oci.get_command('yosys'),
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
        """Performs implementation.

        :param icf: Implementation Constraint Files
        :type icf: list
        """
        family = self.part['family']
        if family == 'ice40':
            ext = 'pcf'
        else:  # family == 'ecp5'
            ext = 'lpf'
        self._create_constraint(icf, ext)
        cmd = _template('nextpnr-{}'.format(family)).format(
            command=self.oci.get_command('nextpnr-{}'.format(family)),
            device=self.part['device'],
            package=self.part['package'],
            outdir=self.outdir,
            project=self.project
        )
        _run(cmd)
        if family == 'ice40':
            cmd = _template('icetime').format(
                command=self.oci.get_command('icetime'),
                device=self.part['device'],
                outdir=self.outdir,
                project=self.project
            )
            _run(cmd)

    def _create_constraint(self, files, ext):
        """Create an unified constraint file."""
        filename = Path('.') / self.outdir / self.project
        filename = '{}.{}'.format(filename, ext)
        with open(filename, 'a') as outfile:
            outfile.truncate(0)
            if files is not None:
                for file in files:
                    with open(file) as infile:
                        print(file)
                        outfile.write(infile.read())

    def bitstream(self):
        """Performs bitstream generation."""
        family = self.part['family']
        if family == 'ice40':
            cmd = _template('icepack').format(
                command=self.oci.get_command('icepack'),
                outdir=self.outdir,
                project=self.project
            )
            _run(cmd)
        else:  # family == 'ecp5'
            cmd = _template('ecppack').format(
                command=self.oci.get_command('ecppack'),
                outdir=self.outdir,
                project=self.project
            )
            _run(cmd)

    def programming(self):
        """Performs programation."""
        family = self.part['family']
        if family == 'ice40':
            cmd = _template('iceprog').format(
                command=self.oci.get_command('iceprog'),
                outdir=self.outdir,
                project=self.project
            )
            _run(cmd)


def _run(command):
    """Run the specified command."""
    subprocess.run(
        command, shell=True, check=True, universal_newlines=True,
    )


def _template(name):
    """Read the specified template file."""
    template = Path(__file__).parent / 'templates' / name
    with open(template, 'r') as file:
        return file.read().strip()
