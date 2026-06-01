# UAV Swarm Formation

A swarm of drones that flies together with no central controller. Each drone
only looks at its nearby neighbors and follows three classic "boids" rules plus
collision avoidance:

- **separation** – don't crash into close neighbors
- **alignment** – fly the same direction as the group
- **cohesion** – stay near the group's center

On top of that they all steer toward a shared target. Click anywhere to move
the target and watch the whole swarm flow toward it. This is how real drone
light-shows and search swarms coordinate.

## run

```bash
pip install pygame
python sim.py
```

tags: ai, swarm, drones, boids, simulation, pygame, robotics

emergent behavior is so cool - simple rules per drone make a smart looking swarm.
