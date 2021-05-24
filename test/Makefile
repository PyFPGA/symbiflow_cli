VHDLDIR = ../resources/vhdl
VLOGDIR = ../resources/verilog

test: all syn imp bit

#
# Synthesis test cases
#

syn: vhdl-simple vhdl-complex vlog-simple vlog-complex

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

#
# Implementation test cases
#

imp:
	symbiflow $@ project-$@
	
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
