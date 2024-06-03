# type: ignore
import board
import busio
import digitalio
import pwmio
from ulab import numpy as np
from digitalio import DigitalInOut, Direction, Pull
import mpl3115a2_highspeed as adafruit_mpl3115a2# Altimeter
from time import sleep, monotonic

# SENSORS
sda_pin = board.GP16
scl_pin = board.GP17
i2c = busio.I2C(scl_pin, sda_pin)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c) # Altimeter
#sensor.sealevel_pressure = 1070

ground = 0
weight = [3, 4, 4, 4, 5, 6, 7, 7, 8, 8, 9, 9]
alt_win_size = 12 # alt_window is smaller because altitude polls slowly
enum = 0
alt_window = np.zeros(alt_win_size) # Creates average array starting at ground


for i in range(25): # Finds ground average
    ground += sensor.altitude
    sleep(.01)
ground = (ground/25)
print(f"ground: {ground}")
inter = 0

pTime = 0
while True:

    pTime = monotonic() # How long the sensor takes to refresh
    alt = sensor.altitude - ground

    alt_window[0] = alt
    alt_window = np.roll(alt_window,1)
    final_alt = np.mean(alt_window)
    final_alt = sum(alt_window[g] * weight[g] for g in range(len(alt_window))) / sum(weight)
    if inter >= 14: # Only saves data every x refreshes
        print(monotonic()-pTime, final_alt)
        inter = 0
    inter += 1

    sleep(.01) # Altitude can only be polled every ~.5 seconds
    # Use weighted average because reaction is slow