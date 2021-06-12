# How to test in hardware

## IceStick

### Using the bash script

```bash
bash icestick.sh
```

or (to program the board)

```bash
bash icestick.sh program
```

### Using the Makefile

```bash
make syn-ice40
make imp-ice40
make bit-ice40
make pgm-ice40
```

or

```bash
make all-ice40
make pgm-ice40
```
