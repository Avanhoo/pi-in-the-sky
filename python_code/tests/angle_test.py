# type: ignore
import board
import busio
import digitalio
import pwmio
from ulab import numpy as np #NEW
#import asyncio #NEW
from math import acos, asin, degrees
from digitalio import DigitalInOut, Direction, Pull
import adafruit_mpu6050 # Gyro
import adafruit_mpl3115a2 # Altimeter
from adafruit_motor import servo
from time import sleep, monotonic
from simple_pid import PID

sda_pin = board.GP16
scl_pin = board.GP17
i2c = busio.I2C(scl_pin, sda_pin)

# SENSORS
imu = adafruit_mpu6050.MPU6050(i2c, address=0x68) # Accelerometer


# PID & VARIABLES
roll = 0
pitch = 0
angle_win_size = 25 # size of angle smoothening window
angle_enum = 0
roll_window = np.zeros(angle_win_size) # Creates average array starting at ground
pitch_window = np.zeros(angle_win_size)

calib0 = 0
calib1 = 0
calib2 = 0
for i in range (150): # Finds baseline for sensors, DO NOT MOVE PICO while calibrating
    calib0 += imu.acceleration[0]
    calib1 += imu.acceleration[1]
    calib2 += imu.acceleration[2]
    sleep(.01)
calib0 = -(calib0/150)
calib1 = -(calib1/150)
calib2 = -(calib2/150)
print(calib1)

def update_angles():
    global roll, pitch
    global angle_win_size, angle_enum
    global roll_window, pitch_window
    
    imu_roll = (imu.acceleration[2]+calib2)/9.8 # Calculates roll angle in rads
    if imu_roll > 1: # stops it from breaking the trig
        imu_roll = 1
    elif imu_roll < -1:
        imu_roll = -1

    if imu.acceleration[0] <(-1.5 + calib0): # Checks if plane is flipped
        imu_roll = 180-(round(degrees(asin(imu_roll))))
    else:
        imu_roll = (round(degrees(asin(imu_roll))))


    imu_pitch = (imu.acceleration[1]+calib1)/9.8 # Calculates pitch angle in rads
    if imu_pitch > 1: # stops it from breaking the trig
        imu_pitch = 1
    elif imu_pitch < -1:
        imu_pitch = -1
    imu_pitch = (round(degrees(asin(imu_pitch)))) # Converts from rads to degrees



    if angle_enum > angle_win_size -1: # Stops array from overflowing
        angle_enum = 0
    roll_window[angle_enum] = imu_roll
    pitch_window[angle_enum] = imu_pitch # Move filtering before trig?
    angle_enum += 1
    
    roll = round(sum(roll_window) / angle_win_size,1)
    pitch = round(sum(pitch_window) / angle_win_size,1)

while True:
    update_angles()
    print(roll, pitch)
    sleep(.001)
