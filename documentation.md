# First Prototype

## Design

## Code

For the first few weeks of the prototype we still were planning on doing a twin plane project with another group. Thus the code was designed to control the plane autonomously after it separated from its twin. When we switched over to a RC plan I abandoned the PID for the control surfaces, though most of my previous work could be repurposed. Now that the pico only has to worry about logging data, the determining the rotation of the airplane and saving that data becomes the most important part of the programming.

The rotation approximation code works by using the accelerometers in the gyroscope and the reference of gravity. While you might expect the rotation part of the gyroscope to be used, that approach would introduce drift. Even with a perfectly calibrated gyroscope, a long mission with high liklihood of shake would call for a specialized algorithm for the gyroscopes to keep their accuracy. For the sake of reliability and project scope, I settled with using the positional accelerometers and gravity in order to approximate the pitch and roll of the plane. The only exception is the heading, which I address in the 2nd prototype. The data collecion, is a rudimentary variable system. Each cycle of the code I save the current time and position data to a list. At the end of the flight when the system is switched off, it writes this list to a CSV file. My worry is that the pico will run out of memory over the course of a flight, and writing the list to the file at the end of the flight can take a worrying amount of seconds.

## Build

## Results

# Second Prototype

## Design

## Code

