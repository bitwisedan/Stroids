import pygame
import math
from constants import *
from circleshape import *

class Shot(CircleShape):
    containers = ()
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.length = radius * 6  # Slightly shorter laser
        self.rect = pygame.Rect(0, 0, self.length, radius)  # Thinner laser
        
    def draw(self, screen):
        # Calculate the angle of the shot's velocity
        angle = math.atan2(self.velocity.y, self.velocity.x)
        
        # Create a surface for the rotated laser
        laser_surf = pygame.Surface((self.length, self.radius * 2), pygame.SRCALPHA)
        
        # Calculate dimensions for perfect centering
        laser_width = self.radius
        half_width = laser_width / 2
        center_y = laser_surf.get_height() / 2
        
        # Draw the main rectangle (centered vertically)
        rect_y = center_y - half_width
        pygame.draw.rect(laser_surf, (255, 255, 255), 
                        (0, rect_y, self.length, laser_width))
        
        # Draw rounded ends (perfect half-circles at each end)
        radius = half_width
        pygame.draw.circle(laser_surf, (255, 255, 255), 
                         (int(radius), int(center_y)), int(radius))
        pygame.draw.circle(laser_surf, (255, 255, 255), 
                         (int(self.length - radius), int(center_y)), int(radius))
        
        # Rotate the surface to match the shot's direction
        rotated_laser = pygame.transform.rotate(laser_surf, -math.degrees(angle))
        
        # Get the rect of the rotated surface and position it so the front is at self.position
        rect = rotated_laser.get_rect()
        # Calculate the offset to position the front of the laser at self.position
        offset = pygame.Vector2(math.cos(angle), math.sin(angle)) * (self.length / 2)
        rect.center = (self.position.x + offset.x, self.position.y + offset.y)
        
        # Draw the rotated laser
        screen.blit(rotated_laser, rect.topleft)
        
    def update(self, dt):
        self.position += self.velocity * dt