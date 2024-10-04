import random
import pygame

class Particle:
    def __init__(self, x, y, dx, dy, color, radius):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = radius
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

class ParticleEmitter():
    def __init__(self, x, y, dx, dy, startColor, endColor, maxStartRadius, dRadius = 0.1):
        self.x = x
        self.y = y
        self.dRadius = dRadius
        self.particles = []
        self.dx = dx
        self.dy = dy
        self.startColor = startColor
        self.endColor = endColor
        self.maxStartRadius = maxStartRadius

    def draw_particles(self, screen):
        for p in self.particles:
            p.draw(screen)
    
    def add_particle(self):
        self.particles.append(Particle(self.x, 
                                       self.y,
                                       self.dx + random.random() * 1.2,
                                       self.dy + random.random() * 1.2,
                                       self.startColor, 
                                       self.maxStartRadius * random.random()))

    def update_particles(self):
        for p in self.particles:
            if(p.radius < 0):
                self.particles.remove(p)
            else:
                # Update particle position
                p.x += p.dx
                p.y += p.dy
                p.radius -= self.dRadius
                 # Decompose color into RGB components
                r, g, b = p.color
                end_r, end_g, end_b = self.endColor

                # Update color values gradually
                if r != end_r:
                    r += (end_r - r) / 4
                if g != end_g:
                    g += (end_g - g) / 4
                if b != end_b:
                    b += (end_b - b) / 4

                # Reassign the updated color back to the particle
                p.color = (int(r), int(g), int(b))
                

    