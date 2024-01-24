# pi-in-the-sky

## Planning
### First ideas
- Ballista
- Aircraft carrier launcher
- Air cannon
- Rc plane
We were first thinking about making a big ballista and launching a simple sensor projectile, but after watching a youtube video where someone made a massive ballista and could hardly launch a stick we lost hope.
After that we though about making a parachuted projectile we'd drop from a plane, but we weren't fans of that or any of our other ideas.
Finally, while talking to Vinnie and Matthias we had the idea to make a splitting plane. Each group would make one, and they'd fly up together before splitting apart. At first that took the shape of one plane dropping another, then two planes conjoined on their stomachs, but then we thought about attaching them together by the wings.

![20231222_124618](https://github.com/Avanhoo/pi-in-the-sky/assets/113116247/0d76d982-8dc1-4656-b559-26f81509c28d)

We looked into the idea and saw that planes like this existed in real life already, called a twin-fuselage aircraft.     ↓ XP-32 Mustang

![North_American_XP-82_Twin_Mustang_44-83887 Color](https://github.com/Avanhoo/pi-in-the-sky/assets/113116247/ec0e30a9-d397-42a5-8819-e2bb1b982c01)

From the start we knew there would be a few major challenges: 
The software control would be tough. We realized early on that rc transmitters and recievers are at least $50 each, and if our groups were going to work together, it'd be cheaper to just get one. The plan as of writing is this: Vinnie and Matthias's team has the transmitter, and the reciever is on their plane. The planes will have wifi connection so that they are communicating with each other and flying as one plane. Once we have reached our desired altitude, we will send the signal for the planes to split, and they will physically detatch and start flying as 2 separate planes. From here, M & V's plane will continue to fly and be controlled like normal, and they will land it manually. Our group's will switch to an autonomous mode when it disconnects, and will land itself in a (hopefully) graceful manner. 

We're looking to 3d print our plane. At first we were going to make it out of foamboard or balsa wood and plastic wrap, but printing the parts would make attaching things like servos and the wing connections easier, as well as being easily and precisely repairable and iterable. We're thinking PETG as it's quite tough, but if we need it lighter we can try out lightweight or foaming PLA.

**Success** would be creating anything that can get into the sky and get down withough being completely destroyed. Even if it snaps off a wing on landing, if it is able to fly up and make a controlled descent, that will be a resounding success. If twin plane idea were to fall apart, we still should have a functional single plane that we can continue our idea with, and hopefully make fly, which, although different from our intended plan, would be okay if it were able to fly and collect data.

### Risk
Since we're making a plane that can fly autonomously, we need to account for flyaways. There are a few other safety measures we can put in place to reduce the chances of the plane causing damage:
- A large clear area to test in
- Preflight checks of all systems and parts
- Code that will stop the motor in the plane exits a defined area
- Code that will stop the motor if the plane is in the sky for too long
- A power kill switch on the remote controller

### Required Proof of Concepts
- **Planes can fly on their own**
  Creating a decent rc plane is a challenge on its own, so we need to be able to make a functional plane to begin with. RC planes often use these fancy lightweight brushless motors, and we don't have the budget for that. We're going to try using a normal brushed dc motor. Granted, the ones we have are bigger than usual, but we will need to conduct some tests to see if they can provide enough thrust, or if I'll have to bring in big 12V I have.
- **Physical Decoupling**
  The planes are going to be attached to each other by the wings, with one on top of the other. We need a sturdy way to lock them together that can also be quickly released reliably. My first idea was to have a push bar connected to multiple hooks, so that you can move the bar and retract the hooks with a single servo. The other plane could then have loops for the hooks to grab. We could also use a screw and socket design.
  
![20231222_124817 (1)](https://github.com/Avanhoo/pi-in-the-sky/assets/113116247/676130c4-7fe9-4420-91f7-a0bd322d6b5a)

- **Software Decoupling**
  The planes have to transition from flying as one, to flying as two. We have to figure out not only this transition, but how they can fly while conjoined. Making the plane fly autonomously will also be a challenge to say the least.


| Week           | Goal                                                         |
| -------------- | ------------------------------------------------------------ |
| W1: Jan 2-5 **CD** | Working wifi connection between picos                    |
| W2: Jan 8-12   | Coupling system tested                                       |
| W3: Jan 15-19  | Completed first design for plane, completed code             |
| W4: Jan 22-25 **P**| First assembly and ground tests                          |
| W5: Jan 29-2   | Iterate and fix issues with first build                      |
| W6: Feb 5-8    | Rebuild and retest                                           |
| W7: Feb 12-16  | Test autonomous flight and control with dropped glide tests  |
| W8: Feb 20-23  | Tweak controls and troubleshoot                              |
| W9: Feb 26-29  | Ground test tandem controls and troubleshoot communications  |
| W10: Mar 4-8 **F** | Test tandem flight and decoupling                        |
| W11: Mar 114   | Troubleshoot / rebuild after test                            |
| W12: Mar 18-22 | Final tweaks and building                                    |
| W13: Mar 25-28 | Ready to fly!                                                |

**CD** = Concept and Design time, doing proof of concepts, coding, and designing the aircraft

**P** = Prototyping time, testing and iterations

**F** = Finalizing time, prototype complete

### Pseudocode
```python
import necessary libs

Connect to other Pico

while not button held: # coupling loop
if button pressed:
	toggle coupling system
Lock coupling system
	
loop Tandem Flight
# The master pico will convert the inputs to work on a twin plane, sending only the necessary commands to the servant pico.
	Receive commands
	Execute commands
if “Split” signal received:
	Physical decouple
	Bank and drop away
	Motor off
	exit loop
while Autonomous Flight:
Maintain constant left bank angle (PID) 
Maintain constant drop speed (PID) # Plane will spiral down slowly
if altitude < 15ft and facing correct direction:
	Straighten out
	Maintain heading and slower altitude drop (PID)
	if altitude < 2ft:
		Flair nose
		Maintain flared nose 
		if still:
			Stop data collection
			End program
```
### BOM
Build:
1x Fuselage
1x Left wing
1x Right wing
1x Elevator
1x Vertical stabilizer
2x Front wheel brackets
2x Big wheels
1x Back wheel bracket
2x Small wheel
1x Nose
1x Propellor

Electronics:
1x Pi Pico W
1x Prototyping shield
1x Adafruit MPU 6050 IMU
1x Adafruit ultimate GPS module
1x Adafruit MPL3115A2 Temperature and Pressure sensor
1x Button
1x LED
3x 180 Micro Servos
1x DC Motor


