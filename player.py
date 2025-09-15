import pygame
import math
from constants import *
from shot import *
from circleshape import CircleShape

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

    def get_triangle_vertices(self):
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        right = pygame.Vector2(1, 0).rotate(-self.rotation)
        
        front = self.position + forward * self.radius * 1.5
        back_left = self.position - forward * self.radius - right * self.radius
        back_right = self.position - forward * self.radius + right * self.radius
        
        return [front, back_left, back_right]

    def draw(self, screen):
        # Get triangle vertices
        v = self.get_triangle_vertices()
        vertices = [(int(p.x), int(p.y)) for p in v]
        
        # Draw filled triangle
        pygame.draw.polygon(screen, (255, 255, 255), vertices)
        
        # Draw outline
        pygame.draw.polygon(screen, (200, 200, 200), vertices, 1)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer -= dt
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                self.timer = PLAYER_SHOOT_COOLDOWN
                return self.shoot()
                
        
    def clamp_to_screen(self):
        self.position.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.position.x))
        self.position.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.position.y))
        
    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        self.velocity = forward * PLAYER_SPEED * dt
        self.position += self.velocity
        self.clamp_to_screen()

    def shoot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        # Use the same rotation direction as the player's movement
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        return shot