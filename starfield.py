import pygame
import random
import math
from constants import *

class Starfield:
    def __init__(self, num_stars=200):
        self.stars = []
        self.speeds = [0.2, 0.5, 0.8]  # Different speeds for parallax effect
        self.layers = [[] for _ in self.speeds]
        
        # Create stars for each layer
        for _ in range(num_stars):
            layer = random.randint(0, len(self.speeds) - 1)
            star = {
                'x': random.uniform(0, SCREEN_WIDTH),
                'y': random.uniform(0, SCREEN_HEIGHT),
                'size': random.uniform(0.5, 2.5),
                'layer': layer
            }
            self.layers[layer].append(star)
    
    def update(self, dx, dy):
        # Update star positions based on player movement and layer speed
        for layer_idx, layer in enumerate(self.layers):
            speed = self.speeds[layer_idx]
            for star in layer:
                star['x'] -= dx * speed
                star['y'] -= dy * speed
                
                # Wrap stars around the screen
                if star['x'] < 0:
                    star['x'] = SCREEN_WIDTH
                elif star['x'] > SCREEN_WIDTH:
                    star['x'] = 0
                if star['y'] < 0:
                    star['y'] = SCREEN_HEIGHT
                elif star['y'] > SCREEN_HEIGHT:
                    star['y'] = 0
    
    def draw(self, screen):
        for layer in self.layers:
            for star in layer:
                # Draw star as a small circle
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),  # White stars
                    (int(star['x']), int(star['y'])),
                    max(1, int(star['size']))  # At least 1 pixel in size
                )
