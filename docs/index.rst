.. program:: symbiflow_cli

Introduction
============

.. warning::
   This project is a proposal for a `SymbiFlow <https://symbiflow.github.io/>`__ command-line Interface, but is not directly related, neither endorsed, by it.

The `SymbiFlow CLI <https://github.com/PyFPGA/symbiflow_cli>`__ proyect aims to provide a CLI utility to solves **HDL-to-bitstream** for FPGAs, based on :wikipedia:`FLOSS <Free_and_open-source_software>`:

* :github:`Yosys <YosysHQ/yosys>` is employed for the *Synthesis* of **Verilog** code, while :github:`NextPnR <YosysHQ/nextpnr>` to perform *Place and Route*.
* :github:`GHDL <ghdl/ghdl>` and the :github:`ghdl-yosys-plugin <ghdl/ghdl-yosys-plugin>` provide the **VHDL** support.
* Tools from the :github:`IceStorm <YosysHQ/icestorm>` and :github:`Trellis <YosysHQ/prjtrellis>` projects provide support for **iCE40** and **ECP5** devices.
* Ideally, it will also support **System Verilog** (through :github:`Surelog <chipsalliance/Surelog>` and :github:`UHDM <chipsalliance/UHDM>`), other *P&R* tools (such as :github:`VPR <verilog-to-routing/vtr-verilog-to-routing>`), and more devices (employing projects such as :github:`Apicula <YosysHQ/apicula>`, :github:`Mistral <Ravenslofty/mistral>`, :github:`Oxide <gatecat/prjoxide>`, :github:`XRay <SymbiFlow/prjxray>`, :github:`URay <SymbiFlow/prjuray>`, and more!).

.. note::
    By default, it assumes that the tools employed under the hood are installed and ready to be used. Alternatively, an :wikipedia:`OCI <Open_Container_Initiative>` engine such as Docker or Podman could be used, based on containers from the `hdl/containers <https://hdl.github.io/containers>`__ Project.

.. toctree::
   cli.rst
   api.rst
   devices.rst
