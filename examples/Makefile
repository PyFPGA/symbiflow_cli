ENGINE  = docker

ICE40   = hx1k-tq144
ECP5    = 25k-CSFBGA285

BOARD   = icestick

VHDLDIR = ../resources/vhdl
VLOGDIR = ../resources/verilog
CONSDIR = ../resources/constraints/$(BOARD)


test: all syn pnr bit

#
# Complete flow examples
#

all: all-ice40

all-ice40:
	symbiflow all --oci-engine $(ENGINE) --part $(ICE40) \
		--vlog $(VLOGDIR)/blink.v \
		--pcf $(CONSDIR)/clk.pcf $(CONSDIR)/led.pcf \
		--top Blink -o build-ice40 --project ice40

#
# Synthesis examples
#

syn: \
  vhdl-simple vhdl-complex vhdl-param vhdl-arch \
  vlog-simple vlog-complex vlog-define vlog-include vlog-param \
  syn-ice40 syn-ecp5

vhdl-simple:
	symbiflow syn --oci-engine $(ENGINE) \
		--vhdl $(VHDLDIR)/blink.vhdl \
		--top Blink -o build-$@ --project $@

vhdl-complex:
	symbiflow syn --oci-engine $(ENGINE) \
		--vhdl \
			$(VHDLDIR)/blink.vhdl,blink_lib \
			$(VHDLDIR)/blink_pkg.vhdl,blink_lib \
			$(VHDLDIR)/top.vhdl \
		--top Top -o build-$@ --project $@

vhdl-param:
	symbiflow syn --oci-engine $(ENGINE) \
		--vhdl $(VHDLDIR)/generics.vhdl \
		--param BOO:True INT:255 \
		--top Params -o build-$@ --project $@

vhdl-arch:
	symbiflow syn --oci-engine $(ENGINE) \
		--vhdl $(VHDLDIR)/arch.vhdl \
		--arch Second \
		--top Arch -o build-$@ --project $@

vlog-simple:
	symbiflow syn --oci-engine $(ENGINE) \
		--vlog $(VLOGDIR)/blink.v \
		--top Blink -o build-$@ --project $@

vlog-complex:
	symbiflow syn --oci-engine $(ENGINE) \
		--vlog \
			$(VLOGDIR)/blink.v \
			$(VLOGDIR)/top.v \
		--top Top -o build-$@ --project $@

vlog-define:
	symbiflow syn --oci-engine $(ENGINE) \
		--vlog $(VLOGDIR)/defines.v \
		--define DEFAULT_FREQ:10000000 DEFAULT_SECS:2 \
		--top Defines -o build-$@ --project $@

vlog-include:
	symbiflow syn --oci-engine $(ENGINE) \
		--vlog $(VLOGDIR)/paths.v \
		--include $(VLOGDIR)/path1 $(VLOGDIR)/path2 \
		--top Paths -o build-$@ --project $@

vlog-param:
	symbiflow syn --oci-engine $(ENGINE) \
		--vlog $(VLOGDIR)/parameters.v \
		--param BOO:1 INT:255 LOG:1 \
		--top Params -o build-$@ --project $@

syn-ice40:
	symbiflow syn --oci-engine $(ENGINE) --part $(ICE40) \
		--vlog $(VLOGDIR)/blink.v \
		--top Blink -o build-ice40 --project ice40

syn-ecp5:
	symbiflow syn --oci-engine $(ENGINE) --part $(ECP5) \
		--vlog $(VLOGDIR)/blink.v \
		--top Blink -o build-ecp5 --project ecp5

#
# Place and Route examples
#

pnr: pnr-ice40 pnr-ecp5

pnr-ice40:
	symbiflow pnr --oci-engine $(ENGINE) --part $(ICE40) \
		--pcf $(CONSDIR)/clk.pcf $(CONSDIR)/led.pcf \
		-o build-ice40 --project ice40

pnr-ecp5:
	symbiflow pnr --oci-engine $(ENGINE) --part $(ECP5) \
	-o build-ecp5 --project ecp5

#
# Bitstream generation examples
#

bit: bit-ice40 bit-ecp5

bit-ice40:
	symbiflow bit --oci-engine $(ENGINE) --part $(ICE40) -o build-ice40 --project ice40

bit-ecp5:
	symbiflow bit --oci-engine $(ENGINE) --part $(ECP5) -o build-ecp5 --project ecp5

#
# Programation examples
#

pgm-ice40:
	symbiflow pgm --oci-engine $(ENGINE) --part $(ICE40) -o build-ice40 --project ice40

pgm-ecp5:
	symbiflow pgm --oci-engine $(ENGINE) --part $(ECP5) -o build-ecp5 --project ecp5

#
# Clean
#

clean:
	@rm -fr build-*
