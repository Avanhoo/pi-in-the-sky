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

*insert image here*

We looked into the idea and saw that planes like this existed in real life already, called a twin-fuselage aircraft.     ↓ XP-32 Mustang

![North_American_XP-82_Twin_Mustang_44-83887 Color](https://github.com/Avanhoo/pi-in-the-sky/assets/113116247/ec0e30a9-d397-42a5-8819-e2bb1b982c01)

From the start we knew there would be a few major challenges: 
The software control would be tough. We realized early on that rc transmitters and recievers are at least $50 each, and if our groups were going to work together, it'd be cheaper to just get one. The plan as of writing is this: Vinnie and Matthias's team has the transmitter, and the reciever is on their plane. The planes will have wifi connection so that they are communicating with each other and flying as one plane. Once we have reached our desired altitude, we will send the signal for the planes to split, and they will physically detatch and start flying as 2 separate planes. From here, M & V's plane will continue to fly and be controlled like normal, and they will land it manually. Our group's will switch to an autonomous mode when it disconnects, and will land itself in a (hopefully) graceful manner. 

### Required Proof of Concepts
- **Planes can fly on their own**
  Creating a decent rc plane is a challenge on its own, so we need to be able to make a functional plane to begin with. RC planes often use these fancy lightweight brushless motors, and we don't have the budget for that. We're going to try using a normal brushed dc motor. Granted, the ones we have are bigger than usual, but we will need to conduct some tests to see if they can provide enough thrust, or if I'll have to bring in big 12V I have.
- **Physical Decoupling**
  The planes are going to be attached to each other by the wings, with one on top of the other. We need a sturdy way to lock them together that can also be quickly released reliably. My first idea is to have a push bar connected to multiple hooks, so that you can move the bar and retract the hooks with a single servo. The other plane could then have loops for the hooks to grab
  
  *insert image here*

- **Software Decoupling**
  The planes have to transition from flying as one, to flying as two. We have to figure out not only this transition, but how they can fly while conjoined. Making the plane fly autonomously will also be a challenge to say the least.
