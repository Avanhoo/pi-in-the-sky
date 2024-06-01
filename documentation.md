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

### CAD

This version of the plane was intended to be a much more realistic design for a remote control plane. To this end, the design philosophy was to make a plane that was much more convenient for assembly and tinkering purposes, as well as having a much better chance of actually flying. 

The general idea for the assembly of this version was to have a front and a rear subassembly, which would be connected via carbon fiber tubes, and the wing would also be connected in a similar fashion. 

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/sketch.png?raw=true" width="800"> 

Like this!

The first part I worked on was the wings. I made the airfoil profile, which would just be a spar that we would print many times and stack on a rod, to be covered with some sort of film to make a complete wing.

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/airfoil.png?raw=true" width="800"> 
Here's the airfoil.

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/wing.png?raw=true" width="800"> 

And here's the wing. 

After making the wing, I worked on the rear assembly. The bulk of the rear assembly is the two rear wings, which are connected to the main rod with another part. 

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/rearwings.png?raw=true" width="800"> 

Connected to each wing will be a flat rudder piece, which will be connected to the servos in the front assembly with a fishing line. 

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/rudder.png?raw=true" width="800"> 

The final and most complicated step for the CAD was to make the front assembly. This is the part that would house all the electronics, so getting a good housing that securely holds each component while also being convenient to tinker with would be tricky. In the end, I decided that the biggest components (except for the servos) would be connected to the housing with magnets, so they could be easily removed and replaced with minimal effort. The top cover is also connected with magnets and is much bigger than the previous design.

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/bodydiagram.png?raw=true" width="800"> 

The other big part of the front assembly is the joint that would connect the front, rear, and wing assemblies, which looks like this. 

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/connector.png?raw=true" width="800"> 

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/frontassembly.png?raw=true" width="800"> 

Here's what the whole front assembly looks like without the cover on. 

## Code

Where I had focused on the data filtering part of the code on the first prototype, I shifted to woking on data storage and analysis during this time. I switched to using new lines as separators instead of commas in my .csv file, and made it so that the recording program would only save a data point every set interval, instead of randomly, hundreds of times per second. On the data analysis side I created a program which reads the data.csv file and visualizes it at a 1:1 speed. I was going to graph it at first, but decided on using pygame to visualize each axis instead.

![image](https://github.com/Avanhoo/pi-in-the-sky/assets/113116247/e80ce33f-00e8-4641-94f5-27146e30f542)

Once the graph was working I wanted to make the data smoother, as even with the recording program running at maximum speed the data was coming in at ~0.3 second intervals. To do this I used scipy's spline interpolation. I created a spline for each recording axis, and switched from using the recording's time to a set delta time every cycle. This leaves me with a buttery smooth visualization of the plane's flight.

## Build

Getting the main body of the plane together was a total breeze (thanks Matthew!). The magnet idea made tinkering and removing parts incredibly easy and never led to any falling apart issues. This combined with the realization that the pico and flight electronics could remain separate systems (the esc could provide power to the reciever), made the body the easiest part.

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/2ndBuild.jpg?raw=true" width="400"> 

It can't be all sunshine and rainbows, unfortunately, and we ran into trouble with the v-tail's "ruddervators" (that's a real word). The use of fishing line to pull on the rudders was very finicky due to its unruly nature. We at first tried to pull on one side of each rudder, with a spring pulling back the other way. In practice, the springs were too strong and when the string would hit the hinge and the servo would lose any meaningful torque against the spring. While we tried moving the string connection point on the rudder, we settled on using a piece of string on each side of the rudders. It was inconsistent because of the different tensions and lengths of the strings, but it worked.

![ruddervators!](/images/ruddervator.gif)

We had planned to wrap the wings in shrink wrap, but with that not working we opted for a light fabric. It was lighter and easier than using paper or printed covers. Our one concern after attaching the wings was the center of mass. It was still a bit behind the wings because of how far out the tail was, but aside from weighing down the body with spare metal, there was nothing that could be done. Besides, the thing was a beauty:

<img src="https://github.com/Avanhoo/pi-in-the-sky/blob/main/images/fullPlane.jpg?raw=true" width="600"> 



