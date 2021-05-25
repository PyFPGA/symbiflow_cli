VHDLDIR = ../resources/vhdl
VLOGDIR = ../resources/verilog

test: all syn imp bit

#
# Synthesis test cases
#

syn: vhdl-simple vhdl-complex vlog-simple vlog-complex syn-ice40 syn-ecp5

vhdl-simple:
	symbiflow syn --oci-engine docker \
		--vhdl $(VHDLDIR)/blink.vhdl \
		--top Blink -o build-$@ $@

vhdl-complex:
	symbiflow syn --oci-engine docker \
		--vhdl \
			$(VHDLDIR)/blink.vhdl,blink_lib \
			$(VHDLDIR)/blink_pkg.vhdl,blink_lib \
			$(VHDLDIR)/top.vhdl \
		--top Top -o build-$@ $@

vlog-simple:
	symbiflow syn --oci-engine docker \
		--vlog $(VLOGDIR)/blink.v \
		--top Blink -o build-$@ $@

vlog-complex:
	symbiflow syn --oci-engine docker \
		--vlog \
			$(VLOGDIR)/blink.v \
			$(VLOGDIR)/top.v \
		--top Top -o build-$@ $@

syn-ice40:
	symbiflow syn --oci-engine docker \
		--vlog $(VLOGDIR)/blink.v \
		--part hx4k-tq144 \
		--top Blink -o build-ice40 ice40

syn-ecp5:
	symbiflow syn --oci-engine docker \
		--vlog $(VLOGDIR)/blink.v \
		--part um5g-85k-CABGA381 \
		--top Blink -o build-ecp5 ecp5

#
# Implementation test cases
#

imp: imp-ice40 imp-ecp5

imp-ice40:
	symbiflow imp --oci-engine docker --part hx4k-tq144 -o build-ice40 ice40

imp-ecp5:
	symbiflow imp --oci-engine docker --part 25k-CSFBGA285 -o build-ecp5 ecp5

#
# Bitstream generation test cases
#

bit:
	symbiflow $@ project-$@

#
# Complete flow test cases
#

all:

#
# Clean
#

clean:
	@rm -fr build-*
