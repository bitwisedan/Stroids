from circleshape import *
from constants import *
import pygame
import random
import math

class Asteroid(CircleShape):
    containers = ()
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        for group in self.containers:
            group.add(self)
        
        # Generate asteroid shape points once during initialization
        self.num_points = random.randint(5, 9)  # Fewer points for a more stable shape
        self.point_offsets = []
        
        # Generate relative offsets for the asteroid shape
        for i in range(self.num_points):
            angle = (2 * 3.14159 * i) / self.num_points
            # More subtle radius variation for a less chaotic look
            r = 0.85 + 0.3 * random.random()  # Between 0.85 and 1.15 of radius
            self.point_offsets.append((r * math.cos(angle), r * math.sin(angle)))
        
        # Generate craters once during initialization
        self.craters = []
        num_craters = random.randint(1, 2)  # Fewer craters for cleaner look
        for _ in range(num_craters):
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(0, self.radius * 0.7)  # Keep craters away from edge
            offset_x = distance * math.cos(angle)
            offset_y = distance * math.sin(angle)
            crater_radius = random.uniform(self.radius * 0.1, self.radius * 0.2)
            self.craters.append((offset_x, offset_y, crater_radius))

    def draw(self, screen):
        # Calculate the current points based on position and rotation
        points = []
        for dx, dy in self.point_offsets:
            x = self.position.x + dx * self.radius
            y = self.position.y + dy * self.radius
            points.append((x, y))
        
        # Draw the main asteroid shape (filled)
        pygame.draw.polygon(screen, (80, 80, 80), points)  # Dark gray fill
        pygame.draw.polygon(screen, (150, 150, 150), points, 1)  # Light gray outline
        
        # Draw the craters (as dark circles for depth)
        for dx, dy, crater_radius in self.craters:
            pygame.draw.circle(screen, (60, 60, 60),  # Darker gray for craters
                             (int(self.position.x + dx), 
                              int(self.position.y + dy)), 
                             int(crater_radius))
    
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