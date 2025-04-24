# Engine sound emulator

This ESP32-C3 based device allows you to simulate the sound of an internal combustion engine. It uses a three-axis accelerometer board to change the frequency of the reproduced sound. The device can be used in children's toys, balance bikes and bicycles.

## Wiring diagram

![Wiring diagram](/img/wiring_diagram.png)

## Firmware settings

You can adjust firmware settings for your application.

```python
# Intervals for generating pulses simulating the sound of a motor
# Lower value - higher frequency
DEFAULT_SPEAKER_INTERVAL = 80000  # Idling (minimum RPM)
MIN_SPEAKER_INTERVAL = 10000  # Maximum RPM

ACCUMULATOR_DEADZONE = 250  # Adjust to eliminate speaker-accelerometer feedback loop
SPEED_DECRIMENT = 15  # Dynamics of decreasing RPM
SPEED_INCRIMENT = 25  # Dynamics of increasing RPM
MOTOR_NOOP_TIMEOUT_SECONDS = 10  # Engine shutdown when idle, sec.
```

## Firmware flashing

1. Install `micropython==1.24.1` release into ESP32-C3 devboard (https://micropython.org/download/ESP32_GENERIC_C3/);
2. Clone this repo. Install dependencies:

```sh
$ git clone https://github.com/itclub-irk/motor_emulator.git
$ cd motor_emulator
$ uv sync
```

3. Connect devboard to computer, transfer firmware files:

```sh
$ ampy -p /dev/ttyACM0 put adxl345.py adxl345.py
$ ampy -p /dev/ttyACM0 put main.py main.py
```

4. Reboot devboard, test sound effects.
