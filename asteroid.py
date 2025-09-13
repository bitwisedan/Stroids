from circleshape import *
from constants import *
import pygame
import random

class Asteroid(CircleShape):
    containers = ()
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        for group in self.containers:
            group.add(self)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return []
        else:
            random_angle = random.uniform(20, 50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_vector_1 = self.velocity.rotate(random_angle)
            new_vector_2 = self.velocity.rotate(-random_angle)
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = new_vector_1
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2.velocity = new_vector_2
            return [asteroid1, asteroid2]