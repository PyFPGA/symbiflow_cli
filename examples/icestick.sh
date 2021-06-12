set -e # Exit immediately if a command exits with a non-zero status.

echo "Synthesis (Verilog)"

symbiflow syn --oci-engine docker --part hx1k-tq144 \
  --vlog ../resources/verilog/blink.v \
  --top Blink -o build-icestick --project icestick

echo "Implementation"

symbiflow imp --oci-engine docker --part hx1k-tq144 \
  --icf ../resources/constraints/icestick/clk.pcf ../resources/constraints/icestick/led.pcf \
  -o build-icestick --project icestick

echo "Bitstream generation"

symbiflow bit --oci-engine docker --part hx1k-tq144 -o build-icestick --project icestick

if [ "$1" == "program" ]; then

    echo "Programation"

    symbiflow pgm --oci-engine docker --part hx1k-tq144 -o build-icestick --project icestick

fi

echo "From Synthesis to Bitstream generation in one step (VHDL)"

symbiflow all --oci-engine docker --part hx1k-tq144 \
  --vhdl ../resources/vhdl/blink.vhdl \
  --icf ../resources/constraints/icestick/clk.pcf ../resources/constraints/icestick/led.pcf \
  --top Blink -o build-icestick --project icestick

if [ "$1" == "program" ]; then

    echo "Programation"

    symbiflow pgm --oci-engine docker --part hx1k-tq144 -o build-icestick --project icestick

fi
