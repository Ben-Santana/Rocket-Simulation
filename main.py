import numpy
import pygame
from body import Body
from particle import ParticleEmitter
from constants import ENDING_FUEL_COLOR, STARTING_FUEL_COLOR, WIDTH, BODY_RADIUS, HEIGHT, PFORCE, BACKGROUND, FPS, DRAW_FORCES

# Initialize Pygame ------------------------------------
pygame.init()

# Set up the display -----------------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulation")

# Create a Body instance -------------------------------
leftParticleEmitter = ParticleEmitter((WIDTH // 2 - BODY_RADIUS / 2), (HEIGHT // 2 + BODY_RADIUS / 2), -PFORCE, PFORCE, STARTING_FUEL_COLOR, ENDING_FUEL_COLOR, 20, 0.7)
rightParticleEmitter = ParticleEmitter((WIDTH // 2 + BODY_RADIUS / 2), (HEIGHT // 2 + BODY_RADIUS / 2), PFORCE, PFORCE, STARTING_FUEL_COLOR, ENDING_FUEL_COLOR, 20, 0.7)
body = Body(WIDTH // 2, HEIGHT // 2, 15, 100, leftParticleEmitter, rightParticleEmitter)

# Main loop --------------------------------------------
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key detection
    keys = pygame.key.get_pressed()
    DRAW_FORCES = keys[pygame.K_1]

    body.rightPropulsion = False
    body.leftPropulsion = False

    if(keys[pygame.K_LEFT] and body.fuel > 0):
        body.add_left_particle()
        body.fuel = max(body.fuel - 0.1, 0)
        # Propel rocket
        body.leftPropulsion = keys[pygame.K_LEFT]

    if(keys[pygame.K_RIGHT] and body.fuel > 0):
        body.add_right_particle()
        body.fuel = max(body.fuel - 0.1, 0)
        # Propel rocket 
        body.rightPropulsion = keys[pygame.K_RIGHT]

    if(keys[pygame.K_r]):
        body.fuel = body.tank_size
    
    # Fill the screen with the background color
    screen.fill(BACKGROUND)

    # Add Forces
    body.apply_propulsion()
    body.update()

    # Update particles
    body.update_particle_emitters()

    # Draw bar that will indicate amount of fuel left
    body.draw_fuelbar(screen)

    # Draw particles
    body.draw_particles(screen)

    # Draw the body
    body.draw(screen)

    # Display body information
    body.display_info(screen)

    # Draw forces
    if(DRAW_FORCES):
        body.draw_forces(screen)

    # Clear forces for next frame
    body.clear_forces()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
