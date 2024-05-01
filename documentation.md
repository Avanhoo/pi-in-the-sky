# First Prototype

## Design

## Code

For the first few weeks of the prototype we still were planning on doing a twin plane project with another group. Thus the code was designed to control the plane autonomously after it separated from its twin. When we switched over to a RC plan I abandoned the PID for the control surfaces, though most of my previous work could be repurposed. Now that the pico only has to worry about logging data, the determining the rotation of the airplane and saving that data becomes the most important part of the programming.

The rotation approximation code works by using the accelerometers in the gyroscope and the reference of gravity. While you might expect the rotation part of the gyroscope to be used, that approach would introduce drift. Even with a perfectly calibrated gyroscope, a long mission with high liklihood of shake would call for a specialized algorithm for the gyroscopes to keep their accuracy. For the sake of reliability and project scope, I settled with using the positional accelerometers and gravity in order to approximate the pitch and roll of the plane. The only exception is the heading, which I address in the 2nd prototype. The data collecion is a rudimentary variable system. Each cycle of the code I save the current time and position data to a list. At the end of the flight when the system is switched off, it writes this list to a CSV file. My worry is that the pico will run out of memory over the course of a flight, and writing the list to the file at the end of the flight can take a worrying amount of seconds.

## Build

When we first got the shell of the plane together we were stoked as it looked fantastic. As we started to get the electronics in we became more and more worried about the length of the wings. The plane already weighed **insert**, and with its short wings it would have had to go extremely fast to stay in the air. So we lengthened the wings - *a lot*:

**picture**

Fitting all of the modules into the plane was a serious challenge. The individual parts that needed to fit in the feuselage were: 
- Pico with prototyping board
- 3.7v Li-Po, 5v battery connector, and 3.3v step down module
- RC receiver module
- 850mah 3s Li-Po
- Motor ESC
- Long, delicate wires

All of these components together took up a lot of space, and we were barely able to close the plane's top. The problem arose from the fact that we hadn't planned out the interior. Though we had a mount for the pico, the rest was simply crammed in, meaning it was very easy to unplug something accidentally, and very hard to access any important components.

The RC Module we used was the [Flysky -i6X 2.4GHz 10ch Afhds 2A RC with -iA10B Receiver](https://www.flysky-cn.com/fsi6x). It was the cheapest programmable transciever that came with a reciever, and it worked wonderfully for all of our needs. It really took the pressure off of us to not have to worry about another part of the project being disfuctional.

## Results

The First prototype didn't fly. Maybe we should have known from the high weight and small thrust and lift, but our first and only test ended up in the ground:

**video**

There were a few key leaned lessons.
1. The balance of the plane needs to be planned out *before* it is assembled. You need to have at least a basic idea of how the weigh and COM will play out. In the video of our 1st prototype you can see that it had lots of weight and lift in the front, but nothing in the back; the tail falls and the plane stalls.
2. Smaller and lighter is better. We knew this innately when starting a plane project, but we didn't realize the extent to which weight mattered. A smaller plane can go slower, meaning better control and less risk of collisions.
3. The code needed a complete rework. Half of the lines were leftovers from the autonomous era, and the rest were a mess that didn't properly record.

# Second Prototype

## Design

## Code

Where I had focused on the data filtering part of the code on the first prototype, I shifted to woking on data storage and analysis during this time. I switched to using new lines as separators instead of commas in my .csv file, and made it so that the recording program would only save a data point every set interval, instead of randomly, hundreds of times per second. On the data analysis side I created a program which reads the data.csv file and visualizes it at a 1:1 speed. I was going to graph it at first, but decided on using pygame to visualize each axis instead.

Once the graph was working I wanted to make the data smoother, as even with the recording program running at maximum speed the data was coming in at ~0.3 second intervals. To do this I used scipy's spline interpolation. I created a spline for each recording axis, and switched from using the recording's time to a set delta time every cycle. This leaves me with a buttery smooth visualization of the plane's flight.


