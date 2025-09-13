import pygame
from constants import *
from player import *
from asteroid import *
import sys
from asteroidfield import *
from shot import *

updateable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()
Player.containers = updateable, drawable
Asteroid.containers = updateable, drawable, asteroids
AsteroidField.containers = updateable
Shot.containers = shots, updateable, drawable

def main():
    clock = pygame.time.Clock()
    dt = 0
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT /2))
    asteroidfield = AsteroidField()
    while True:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))
        updateable.update(dt)
        for obj in drawable:
            obj.draw(screen)  # Call each object's draw method
        for obj in asteroids:
            if player.collision(obj):
                print("Game over!")
                sys.exit()
            for obj in asteroids:
                for shot in shots:
                    if obj.collision(shot):
                        new_asteroids = obj.split()  # Split asteroid
                        shot.kill()
                        for a in new_asteroids:
                            pass  # Asteroids are auto-added to groups via containers
                        break
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0
        


if __name__ == "__main__":
    main()
