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
		--pcf $(CONSDIR)/clk.pcf --pcf $(CONSDIR)/led.pcf \
		--top Blink -o build-ice40 --project ice40 $(VLOGDIR)/blink.v

#
# Synthesis examples
#

syn: \
  vhdl-simple vhdl-complex vhdl-param vhdl-arch \
  vlog-simple vlog-complex vlog-define vlog-include vlog-param \
  syn-ice40 syn-ecp5

vhdl-simple:
	symbiflow syn --oci-engine $(ENGINE) \
		--top Blink -o build-$@ --project $@ $(VHDLDIR)/blink.vhdl

vhdl-complex:
	symbiflow syn --oci-engine $(ENGINE) \
		--top Top -o build-$@ --project $@ \
		$(VHDLDIR)/blink.vhdl,blink_lib $(VHDLDIR)/blink_pkg.vhdl,blink_lib $(VHDLDIR)/top.vhdl

vhdl-param:
	symbiflow syn --oci-engine $(ENGINE) \
		--param BOO True --param INT 255 \
		--top Params -o build-$@ --project $@ $(VHDLDIR)/generics.vhdl

vhdl-arch:
	symbiflow syn --oci-engine $(ENGINE) \
		--arch Second \
		--top Arch -o build-$@ --project $@ $(VHDLDIR)/arch.vhdl

vlog-simple:
	symbiflow syn --oci-engine $(ENGINE) \
		--top Blink -o build-$@ --project $@ $(VLOGDIR)/blink.v

vlog-complex:
	symbiflow syn --oci-engine $(ENGINE) \
		--top Top -o build-$@ --project $@ $(VLOGDIR)/blink.v  $(VLOGDIR)/top.v

vlog-define:
	symbiflow syn --oci-engine $(ENGINE) \
		--define DEFAULT_FREQ 10000000 --define DEFAULT_SECS 2 \
		--top Defines -o build-$@ --project $@ $(VLOGDIR)/defines.v

vlog-include:
	symbiflow syn --oci-engine $(ENGINE) \
		--include $(VLOGDIR)/path1 --include $(VLOGDIR)/path2 \
		--top Paths -o build-$@ --project $@ $(VLOGDIR)/paths.v

vlog-param:
	symbiflow syn --oci-engine $(ENGINE) \
		--param BOO 1 --param INT 255 --param LOG 1 \
		--top Params -o build-$@ --project $@ $(VLOGDIR)/parameters.v

syn-ice40:
	symbiflow syn --oci-engine $(ENGINE) --part $(ICE40) \
		--top Blink -o build-ice40 --project ice40 $(VLOGDIR)/blink.v

syn-ecp5:
	symbiflow syn --oci-engine $(ENGINE) --part $(ECP5) \
		--top Blink -o build-ecp5 --project ecp5 $(VLOGDIR)/blink.v

#
# Place and Route examples
#

pnr: pnr-ice40 pnr-ecp5

pnr-ice40:
	symbiflow pnr --oci-engine $(ENGINE) --part $(ICE40) \
		--pcf $(CONSDIR)/clk.pcf --pcf $(CONSDIR)/led.pcf \
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
