from machine import Pin, SoftI2C, WDT
from adxl345 import ADXL345
import time

# Intervals for generating pulses simulating the sound of a motor
# Lower value - higher frequency
DEFAULT_SPEAKER_INTERVAL = 80000  # Idling (minimum RPM)
MIN_SPEAKER_INTERVAL = 10000  # Maximum RPM

ACCUMULATOR_DEADZONE = 250  # Adjust to eliminate speaker-accelerometer feedback loop
SPEED_DECRIMENT = 15  # Dynamics of decreasing RPM
SPEED_INCRIMENT = 25  # Dynamics of increasing RPM
MOTOR_NOOP_TIMEOUT_SECONDS = 10  # Engine shutdown when idle, sec.

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
speaker_pin = Pin(10, Pin.OUT)
accel = ADXL345(i2c)
wdt = WDT(timeout=2000)

speaker_pin_state = False
speaker_pin.value(speaker_pin_state)

current_speaker_interval = DEFAULT_SPEAKER_INTERVAL

last_speaker_tick = time.ticks_us()
last_speaker_on_tick = last_speaker_tick

prev_x = prev_y = prev_z = 0

accumulator = 0

motor_enabled = False
last_motor_enabled_tick = 0


def convert_value(current_val):
    if current_val > 32768:
        return -(65536 - current_val)
    return current_val


first_loop = True

while True:
    wdt.feed()

    x, y, z = (convert_value(v) for v in accel.read())

    if accumulator < 5000 and not first_loop:
        accumulator += abs(prev_x - x) + abs(prev_y - y) + abs(prev_z - z)

    prev_x, prev_y, prev_z = x, y, z

    if first_loop:
        first_loop = False
        continue

    if accumulator > ACCUMULATOR_DEADZONE:
        motor_enabled = True
        last_motor_enabled_tick = time.ticks_ms()
        current_speaker_interval -= SPEED_INCRIMENT
        accumulator -= SPEED_DECRIMENT
    else:
        accumulator = 0
        current_speaker_interval += SPEED_INCRIMENT

    if current_speaker_interval > DEFAULT_SPEAKER_INTERVAL:
        current_speaker_interval = DEFAULT_SPEAKER_INTERVAL
    elif current_speaker_interval < MIN_SPEAKER_INTERVAL:
        current_speaker_interval = MIN_SPEAKER_INTERVAL

    if not motor_enabled:
        continue

    if (
        time.ticks_diff(time.ticks_ms(), last_motor_enabled_tick)
        >= MOTOR_NOOP_TIMEOUT_SECONDS * 1000
    ):
        motor_enabled = False
        continue

    if time.ticks_diff(time.ticks_us(), last_speaker_tick) >= current_speaker_interval:
        speaker_pin_state = not speaker_pin_state
        speaker_pin.value(speaker_pin_state)
        last_speaker_tick = time.ticks_us()
        if speaker_pin_state:
            last_speaker_on_tick = last_speaker_tick

    # Здесь можно настроить скважность импульсов
    if (
        speaker_pin_state
        and time.ticks_diff(time.ticks_us(), last_speaker_on_tick) >= 500
    ):
        speaker_pin.value(False)
