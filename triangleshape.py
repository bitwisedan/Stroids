import pygame
import math
from constants import *

class TriangleShape:
    def __init__(self, x, y, size):
        self.position = pygame.Vector2(x, y)
        self.size = size
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        
    def get_vertices(self):
        """Calculate the three vertices of the triangle based on position and rotation."""
        forward = pygame.Vector2(0, 1).rotate(-self.rotation)  # Negative because y increases downward
        right = pygame.Vector2(1, 0).rotate(-self.rotation)
        
        # Define points: front, bottom left, bottom right
        front = self.position + forward * self.size
        bottom_left = self.position - forward * (self.size * 0.5) - right * (self.size * 0.8)
        bottom_right = self.position - forward * (self.size * 0.5) + right * (self.size * 0.8)
        
        return [front, bottom_left, bottom_right]
    
    def collision(self, other):
        """Check collision with another object that has a position and radius."""
        # Simple distance check first for performance
        distance = self.position.distance_to(other.position)
        if distance > self.size + other.radius:
            return False
            
        # More precise triangle-circle collision check
        vertices = self.get_vertices()
        
        # Check if any vertex is inside the circle
        for vertex in vertices:
            if vertex.distance_to(other.position) <= other.radius:
                return True
                
        # Check if any edge of the triangle intersects the circle
        for i in range(3):
            start = vertices[i]
            end = vertices[(i + 1) % 3]
            
            # Vector from start to end of the edge
            edge = end - start
            # Vector from start to circle center
            start_to_center = other.position - start
            
            # Project the center onto the edge
            edge_length_sq = edge.length_squared()
            if edge_length_sq == 0:
                continue
                
            projection = start_to_center.dot(edge) / edge_length_sq
            projection = max(0, min(1, projection))  # Clamp to edge
            
            # Closest point on the edge to the circle center
            closest = start + projection * edge
            
            # If distance to closest point is less than radius, collision
            if closest.distance_to(other.position) <= other.radius:
                return True
                
        return False
