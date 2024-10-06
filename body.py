import math
import pygame
from constants import AIR_DENSITY, BODY_COLOR, BODY_RADIUS, FORCE_LINE_COLOR, FORCE_LINE_WIDTH, GRAVITY, GROUND_FRICTION_COEF, HEIGHT, PFORCE, ROCKET_DRAG_COEF
from particle import ParticleEmitter
from force import Force

class Body:
    def __init__(self, x, y, mass, fuel, left_emitter: ParticleEmitter, right_emitter: ParticleEmitter) -> None:
        # Particle Emitters
        self.left_particle_emitter = left_emitter
        self.right_particle_emitter = right_emitter
        # Fuel
        self.tank_size = fuel
        self.fuel = fuel
        # Mass (kg)
        self.mass = mass
        self.fuel_mass = self.fuel * 0.1
        # Kinematics
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.ax = 0
        self.ay = 0
        # Forces
        self.forces = []
        # Propulsion
        self.leftPropulsion = False
        self.rightPropulsion = False
        self.on_ground = False  # Whether the body is on the ground or not
        self.max_height = 0.0
    
    def draw(self, screen):
        # Draw the body as a circle on the screen
        pygame.draw.circle(screen, BODY_COLOR, (int(self.x), int(self.y)), BODY_RADIUS)

    def draw_forces(self, screen):
        for f in self.forces:
            pygame.draw.line(screen, 
                             FORCE_LINE_COLOR, 
                             (int(self.x), int(self.y)), 
                             (int(self.x) + (f.x), int(self.y) + (f.y)),
                             FORCE_LINE_WIDTH)
            
    def draw_fuelbar(self, screen):
        # Draw bar to represent amount of fuel in tank
        barHeight = 3 * HEIGHT // 5
        fuelPercent = (self.fuel / self.tank_size)
        fuelHeight = fuelPercent * barHeight
        margin = HEIGHT // 5

        blue_green = min(800 * fuelPercent, 255)

        pygame.draw.rect(screen, (25, 25, 25), (20, margin, 30, barHeight))
        pygame.draw.rect(screen, (255, blue_green, blue_green), (20, margin + (barHeight - fuelHeight), 30, fuelHeight))
    
    def clear_forces(self):
        self.forces = []

    def check_ground_collision(self):
        if self.y >= HEIGHT - BODY_RADIUS:  # Ground collision check
            NORMAL_FORCE = Force(0, -1 * (self.mass + self.fuel_mass) * GRAVITY)
            self.dy = 0
            self.y = HEIGHT - BODY_RADIUS
            self.forces.append(NORMAL_FORCE)
            self.on_ground = True
        else:
            self.on_ground = False
    
    def apply_propulsion(self):
        if self.leftPropulsion:
            # Add propulsion force
            self.forces.append(Force(PFORCE, -PFORCE))  # Only horizontal force
        if self.rightPropulsion:
            # Add propulsion force
            self.forces.append(Force(-PFORCE, -PFORCE))  # Only horizontal force

    # Calculates net force acting on the body
    def net_force(self):
        net = Force(0, 0)
        for f in self.forces:
            net.x += f.x
            net.y += f.y
        return net

    def apply_friction(self):
        if self.on_ground:
            normal_force = (self.mass + self.fuel_mass) * abs(GRAVITY)
            friction_force = normal_force * GROUND_FRICTION_COEF
            if self.dx > 0:
                friction_force = min(friction_force, self.dx)  # Ensure friction doesn't reverse the direction
                self.forces.append(Force(-friction_force, 0))  # Apply friction to the left
            elif self.dx < 0:
                friction_force = min(friction_force, -self.dx)
                self.forces.append(Force(friction_force, 0))  # Apply friction to the right

    def apply_drag(self):
        # Calculate the cross-sectional area of the body (circular cross-section)
        cross_sectional_area = math.pi * (BODY_RADIUS ** 2)
        
        # Calculate the velocity magnitude
        velocity_magnitude = math.sqrt(self.dx**2 + self.dy**2)

        if velocity_magnitude > 0:
            # Calculate drag force magnitude
            drag_magnitude = 0.5 * AIR_DENSITY * (velocity_magnitude ** 2) * ROCKET_DRAG_COEF * cross_sectional_area

            # Drag acts opposite to the direction of velocity, so we apply the drag force in the opposite direction
            drag_x = -drag_magnitude * (self.dx / velocity_magnitude)
            drag_y = -drag_magnitude * (self.dy / velocity_magnitude)

            print(self.y)

            # Add drag force to the list of forces
            self.forces.append(Force(drag_x, drag_y))
    
    def display_info(self, screen):
        # Create the text to display
        font = pygame.font.SysFont(None, 25)
        mass_text = font.render(f"Total Mass: {round(self.mass + self.fuel_mass, 2)} kg", True, (255, 255, 255))
        velocity_text = font.render(f"Velocity: ({self.dx:.2f}, {-1 * self.dy:.2f})", True, (255, 255, 255))
        max_height_text = font.render(f"Highest Altitude: {round(self.max_height, 2)}m", True, (255, 255, 255))

        # Blit the text to the screen at specific positions
        screen.blit(mass_text, (20, 20))
        screen.blit(velocity_text, (20, 45))
        screen.blit(max_height_text, (20, 70))

    def update(self):
        # Add force of gravity
        f_gravity = Force(0, GRAVITY * (self.mass + self.fuel_mass))
        self.forces.append(f_gravity)

        # Apply drag
        #self.apply_drag()

        # Check for ground collision
        self.check_ground_collision()

        # Apply friction if on the ground
        self.apply_friction()


        # Calculate net force and update acceleration
        net = self.net_force()
        self.ax = (net.x / 60) / (self.mass + self.fuel_mass)
        self.ay = (net.y / 60) / (self.mass + self.fuel_mass)

        # Update velocity
        self.dx += self.ax
        self.dy += self.ay

        # Update position
        self.x += self.dx
        self.y += self.dy

        self.fuel_mass = self.fuel * 0.1
        self.max_height = max(self.max_height, 0.01 * (HEIGHT - self.y))

    def update_particle_emitters(self):
        # Update emitter positions
        self.left_particle_emitter.x = self.x
        self.left_particle_emitter.y = self.y
        self.right_particle_emitter.x = self.x
        self.right_particle_emitter.y = self.y
        # Update particles
        self.left_particle_emitter.update_particles()
        self.right_particle_emitter.update_particles()

    def draw_particles(self, screen):
        # Draw particles
        self.left_particle_emitter.draw_particles(screen)
        self.right_particle_emitter.draw_particles(screen)

    def add_left_particle(self):
        # Generate new particle
        self.left_particle_emitter.add_particle()
    
    def add_right_particle(self):
        # Generate new particle
        self.right_particle_emitter.add_particle()
