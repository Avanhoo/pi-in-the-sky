# Afton Van Hooser - Py in the sky project
# file to be run on computer after data is collected. This visualizes the flight path in pygame, allowing for navigation with the arrow keys.
from time import sleep, monotonic
import numpy as np
from scipy import interpolate
from math import cos, sin, tan
from LiveGraph import LiveGraph
import pygame


pygame.init()
screen = pygame.display.set_mode((820, 320))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
running = True
playing = True
pressed = None

with open("C:/Users/avanhoo2498/Documents/Engineering_4_Notebook/Project/data.csv", "r") as datalog: # Gets data to graph
    read = datalog.read()
datalog.close()
memory = read.splitlines()# First 4 are time and calibration values, then each 4 after that are time, roll, pitch, heading, speed
print(f"Length: {len(memory)}")

time = memory[4::5]
roll_list = interpolate.splrep(time, memory[5::5]) # Makes an interpolation spline for all axes
pitch_list = interpolate.splrep(time, memory[6::5])
heading_list = interpolate.splrep(time, memory[7::5])
altitude_list =interpolate.splrep(time, memory[8::5])
image = pygame.image.load('pitch.png')
orig_image = image
rect = image.get_rect(center=(360, 130))

def rotate(image, rect, angle):
    """Rotate the image while keeping its center."""
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect

def graph(curr_time, roll, pitch, heading, altitude): # Quickly displays all components
    global orig_image, rect, time
    screen.fill('grey')
    img = font.render(f'Time: {round(curr_time,2)}', True, 'black')
    screen.blit(img, (20, 290))
    pygame.draw.rect(screen, 'black', (130, 290, 200, 18))
    pygame.draw.rect(screen, 'blue', (132, 292, 196*(i/float(time[-1])), 14))

    
    img = font.render('Roll', True, 'black') # 200 long + 20 padding edges, 40 padding between
    screen.blit(img, (110, 260))
    pygame.draw.aaline(screen, 'black', (120+100*cos(roll), 130+100*sin(roll)), (120-100*cos(roll), 130-100*sin(roll)))

    img = font.render('Pitch', True, 'black')
    screen.blit(img, (340, 260))

    image, rect = rotate(orig_image, rect, pitch*-90)
    screen.blit(image, rect)
    
    #pygame.draw.aaline(screen, 'black', (360+100*cos(pitch), 130+100*sin(pitch)), (360-100*cos(pitch), 130-100*sin(pitch)))

    img = font.render('Heading', True, 'black')
    screen.blit(img, (570, 260))
    pygame.draw.aaline(screen, 'black', (600+100*cos(heading), 130+100*sin(heading)), (600-100*cos(heading), 130-100*sin(heading)))

    img = font.render('Altitude', True, 'black') # 40 wide
    screen.blit(img, (750, 260)) 
    pygame.draw.aaline(screen, 'black', (750, 230), (810, 230))# Ground line
    pygame.draw.aaline(screen, 'blue', (760, 230-altitude*10), (800, 230-altitude*10))# Gauge

    pygame.display.flip()


tStart = monotonic()
i = 0
dTime = .016 # Delta Time, can be very small as data is interpolated, .016 is 60Hz

while i < float(time[-1]) and running: # Loops through all data points
    while monotonic()-tStart < i: # Only refreshed once the requested time is reached
        pass
    
    if pressed != pygame.key.get_pressed():
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            if i < 5:
                tStart += i
                i = 0
            else:
                i -= 5
                tStart +=5
        if pressed[pygame.K_RIGHT]:
            i += 5
            tStart -= 5

    print(f"time: {round(i,2)}   cycle: {round(i/dTime)}") # Prints the recorded time and cycle
    
    roll = (3.14159/180)*float(interpolate.splev(i, roll_list)) # Grabs interpolated values of the axex
    pitch = (3.14159/180)*float(interpolate.splev(i, pitch_list))
    heading = (3.14159/180)*float(interpolate.splev(i, heading_list))
    altitude = float(interpolate.splev(i, altitude_list))

    graph(i, roll, pitch, heading, altitude)


    for event in pygame.event.get(): # Checks if X on window is clicked
        if event.type == pygame.QUIT:
            running = False
    if playing:
        i += dTime
