set -e # Exit immediately if a command exits with a non-zero status.

echo "Synthesis (Verilog)"

symbiflow syn --oci-engine docker --part hx1k-tq144 \
  --top Blink -o build-icestick --project icestick ../resources/verilog/blink.v

echo "Place and Route"

symbiflow pnr --oci-engine docker --part hx1k-tq144 \
  --pcf ../resources/constraints/icestick/clk.pcf --pcf ../resources/constraints/icestick/led.pcf \
  -o build-icestick --project icestick

echo "Bitstream generation"

symbiflow bit --oci-engine docker --part hx1k-tq144 -o build-icestick --project icestick

if [ "$1" == "program" ]; then

    echo "Programation"

    symbiflow pgm --oci-engine docker --part hx1k-tq144 -o build-icestick --project icestick

fi

echo "From Synthesis to Bitstream generation in one step (VHDL)"

symbiflow all --oci-engine docker --part hx1k-tq144 \
  --pcf ../resources/constraints/icestick/clk.pcf --pcf ../resources/constraints/icestick/led.pcf \
  --top Blink -o build-icestick --project icestick ../resources/vhdl/blink.vhdl

if [ "$1" == "program" ]; then

    echo "Programation"

    symbiflow pgm --oci-engine docker --part hx1k-tq144 -o build-icestick --project icestick

fi
