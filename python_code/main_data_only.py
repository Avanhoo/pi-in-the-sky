# type : ignore
# Afton Van Hooser - Pi in the sky project
# file to be run on pico when in flight. Collects rotational data and altitude.
import board
import busio
import digitalio
from math import acos, asin, degrees
from ulab import numpy as np
from digitalio import DigitalInOut, Direction, Pull
import adafruit_mpu6050 # Gyro
import mpl3115a2_highspeed as adafruit_mpl3115a2 # Altimeter
from time import sleep, time, monotonic

sda_pin = board.GP16
scl_pin = board.GP17
i2c = busio.I2C(scl_pin, sda_pin)

# LIGHTS
sled = digitalio.DigitalInOut(board.LED) # Maybe capitalize LED?
sled.direction = digitalio.Direction.OUTPUT

# SWITCH
switch = DigitalInOut(board.GP18)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# SENSORS
imu = adafruit_mpu6050.MPU6050(i2c, address=0x68) # Accelerometer
sensor = adafruit_mpl3115a2.MPL3115A2(i2c) # Altimeter

# FILTERING
angle_win_size = 25 # size of angle smoothening window
alt_win_size = 12
weight = [3, 4, 4, 4, 5, 6, 7, 7, 8, 8, 9, 9] # For altitude quick response
angle_enum = 0
angle_window = np.zeros(angle_win_size)
roll_window = np.zeros(angle_win_size)
pitch_window = np.zeros(angle_win_size)
alt_window = np.zeros(alt_win_size) # Creates average array starting at ground


# VARIABLES
stage = 0 # 0 is calibrating and waiting for button press, 1 is standby to fly, 
roll = 0
pitch = 0
flipped = 0
altitude = 0
ground = 0 # Base for altimeter


def updata(): # Can be called on to refresh the information about the airplane's position and orientation
    global roll, pitch, flipped, altitude
    global angle_win_size, angle_enum
    global roll_window, pitch_window
    global alt_win_size, alt_window
    global calib0, calib1, calib2

    imu_roll = (imu.acceleration[0]+calib0)/9.8 # Calculates roll angle in rads
    if imu_roll > 1: # stops it from breaking the trig
        imu_roll = 1
    elif imu_roll < -1:
        imu_roll = -1
    imu_roll = (round(degrees(asin(imu_roll))))

    imu_pitch = (imu.acceleration[1]+calib1)/9.8 # Calculates pitch angle in rads
    if imu_pitch > 1: # stops it from breaking the trig
        imu_pitch = 1
    elif imu_pitch < -1:
        imu_pitch = -1
    imu_pitch = (round(degrees(asin(imu_pitch)))) # Converts from rads to degrees

    if imu.acceleration[2] <(-1.5 + calib2): # Checks if plane is flipped
        flipped = 1
    else:
        flipped = 0


    if angle_enum > angle_win_size -1: # Stops array from overflowing
        angle_enum = 0
    roll_window[angle_enum] = imu_roll
    pitch_window[angle_enum] = imu_pitch # Move filtering before trig?
    angle_enum += 1
    
    alt = sensor.altitude - ground
    alt_window[0] = alt
    alt_window = np.roll(alt_window,1)
    final_alt = np.mean(alt_window)

    roll = round(sum(roll_window) / angle_win_size,1)
    pitch = round(sum(pitch_window) / angle_win_size,1)
    altitude = sum(alt_window[g] * weight[g] for g in range(len(alt_window))) / sum(weight)
    # END FUNCTION


def store():
    global roll, pitch, flipped, sltitude
    memory.append((monotonic()-STARTTIME))
    memory.append(roll)
    memory.append(pitch)
    memory.append(flipped)
    memory.append(altitude)
    
ground = sensor.altitude
calib0 = -0.951494 # Baselines
calib1 = -0.427249
calib2 = -7.94627
memory = [int(time()), calib0, calib1, calib2] # Stores start time and calibrations

def Calibrate():
    global calib0, calib1, calib2
    calib0 = 0
    calib1 = 0
    calib2 = 0
    for i in range(150): # Finds baseline for sensors, DO NOT MOVE PICO while calibrating
        calib0 += imu.acceleration[0]
        calib1 += imu.acceleration[1]
        calib2 += imu.acceleration[2]
        sleep(.01)
    calib0 = -(calib0/150)
    calib1 = -(calib1/150)
    calib2 = -(calib2/150)
    # with open("/data.csv", "a") as datalog: # Opens the data 
    #         datalog.write(f"{calib0},{calib1},{calib2}") # Save calibration values
    #         datalog.flush()

for i in range(25): # Finds ground average, required on every start
    ground += sensor.altitude
    sleep(.01)
ground = (ground/25)


print("Initialized, waiting for switch")
switch_count = 0
timer = 0
prevSwitch = switch.value

while stage == 0: # Switch once to enter standby, twice to calibrate, 2 second window
    #print(switch.value)
    if (switch.value != prevSwitch) and switch_count == 0: # 1st switch
        print("1st Switch")
        timer = float(monotonic())
        switch_count = 1
        prevSwitch = switch.value

    elif (switch.value != prevSwitch) and float(monotonic()) < timer+2: # Calibrates if switched again
        print("Calibrating in 2s")
        sleep(2)
        Calibrate()
        print(f"Calibrated at {calib0}, {calib1}, {calib2}")
        switch_count = 0
        prevSwitch = switch.value

    elif float(monotonic()) > timer+2 and switch_count == 1: # Moves on
        timer = float(monotonic())
        stage = 1
    sleep(.05)
sleep(.5)

print("WAITING FOR THROW")
while stage == 1: # Standby, waits for acceleration of throw
    prevSwitch = switch.value
    if abs(imu.acceleration[1]-calib1) > 5:
        stage = 2
        print("STARTING")


# ----RECORDING STAGE----
prevSwitch = switch.value
STARTTIME = monotonic() # used for determining time since recording start
inter = 0
while stage == 2:
    updata() # Gets current positional and rotational data
    print(altitude)
    if inter >= 14: # Only saves data every x refreshes
        store()
        inter = 0
    
    sleep(.01)# MAKE WAIT UNTIL .25 SECS HAVE PASSED

    if (switch.value != prevSwitch):
        stage = 6
        print("WRITING...")
    inter += 1

print(memory)
while stage == 6: # Shutdown
    
    with open("/data.csv", "w") as datalog: # Opens the data, 'w' mode clears previous contents of file
        for i in range(len(memory)):
            print(str(memory[i]))
            datalog.write(f"{memory[i]}\n") # Save all cached data to csv file
        datalog.flush()
        stage = 7
        
print("COMPLETE")

'''
CH1:
CH2: R Tail
CH3: Throttle
CH4: L Tail
CH5:
CH5:
'''
