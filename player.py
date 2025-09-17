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
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.spawn_position = pygame.Vector2(x, y)

    def get_triangle_vertices(self):
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        right = pygame.Vector2(1, 0).rotate(-self.rotation)
        
        front = self.position + forward * self.radius * 1.5
        back_left = self.position - forward * self.radius - right * self.radius
        back_right = self.position - forward * self.radius + right * self.radius
        
        return [front, back_left, back_right]

    def draw(self, screen):
        v = self.get_triangle_vertices()
        vertices = [(int(p.x), int(p.y)) for p in v]
        
        if self.invincible and int(pygame.time.get_ticks() / 100) % 2 == 0:
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)
            
        pygame.draw.polygon(screen, color, vertices)
        pygame.draw.polygon(screen, (200, 200, 200), vertices, 1)
        
    def draw_lives(self, screen):
        for i in range(self.lives):
            x = 20 + i * 30
            y = screen.get_height() - 30
            size = 10
            points = [
                (x, y - size),
                (x - size, y + size),
                (x + size, y + size)
            ]
            color = (200, 200, 200) if i == self.lives - 1 and not self.invincible else (100, 100, 100)
            pygame.draw.polygon(screen, color, points)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def lose_life(self):
        if self.invincible:
            return False
            
        self.lives -= 1
        if self.lives <= 0:
            return True
            
        self.position = pygame.Vector2(self.spawn_position)
        self.velocity = pygame.Vector2(0, 0)
        self.invincible = True
        self.invincible_timer = 3.0
        return False
        
    def update(self, dt):
        # Update invincibility timer
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
                
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
        # Get the front vertex of the player's triangle
        front_vertex = self.get_triangle_vertices()[0]
        shot = Shot(front_vertex.x, front_vertex.y, SHOT_RADIUS)
        # Use the same rotation direction as the player's movement
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        return shot