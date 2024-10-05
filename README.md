# Physics Simulation with Particle Emitters

This Python project simulates the physics of a body with particle emitters, subject to forces like gravity and propulsion, using the Pygame library. It includes custom classes for managing particles, forces, and body dynamics. The simulation allows for the visualization of force vectors and fuel consumption through a fuel bar display.

## Features

- **Body Simulation**: The main body in the simulation is affected by forces like gravity and propulsion. The body moves according to Newton's laws of motion.
- **Particle Emitters**: The simulation includes particle emitters that generate particles when propulsion is applied. These particles dissipate over time and change color.
- **Force Visualization**: Forces applied to the body are visualized as lines that indicate the direction and magnitude of the forces.
- **Fuel Management**: A fuel bar is displayed, showing the amount of fuel left for propulsion. Fuel consumption is tied to propulsion.

## Project Structure

- `body.py`: Defines the `Body` class, which handles the body’s physical attributes, movement, forces, and drawing on the screen.
- `constants.py`: Contains all the constants used throughout the simulation, such as colors, gravity, and screen dimensions.
- `force.py`: Defines the `Force` class, which applies forces to the body.
- `particle.py`: Defines the `ParticleEmitter` class, which manages the creation, update, and drawing of particles.
- `main.py`: The main file that initializes the Pygame environment and runs the simulation.

## Requirements

- Python 3.x
- Pygame

To install Pygame, run the following command:

```bash
pip install pygame
