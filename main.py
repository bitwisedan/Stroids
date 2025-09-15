import pygame
import sys
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from startscreen import *
from score import Score
from starfield import Starfield

updateable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()
Player.containers = updateable, drawable
Asteroid.containers = updateable, drawable, asteroids
AsteroidField.containers = updateable
Shot.containers = shots, updateable, drawable

from startscreen import show_start_screen, show_directions_screen, show_gameover_screen

def main():
    clock = pygame.time.Clock()
    dt = 0
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Stroids')
    
    # Create starfield background
    starfield = Starfield(num_stars=150)
    while True:
        choice = show_start_screen(screen)
        if choice == "directions":
            show_directions_screen(screen)
            continue  # Show start screen again
        if choice == "start":
            player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT /2))
            asteroidfield = AsteroidField()
            score = Score()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                # Clear screen with black
                screen.fill((0, 0, 0))
                
                # Update and draw starfield based on player movement
                if hasattr(player, 'velocity'):
                    starfield.update(player.velocity.x * 0.1, player.velocity.y * 0.1)
                starfield.draw(screen)
                
                # Update game objects
                updateable.update(dt)
                for obj in drawable:
                    obj.draw(screen)
                score.draw(screen)
                game_over = False
                for obj in asteroids:
                    if player.collision(obj):
                        game_over = True
                        break
                for obj in asteroids:
                    for shot in shots:
                        if obj.collision(shot):
                            new_asteroids = obj.split()
                            score.add(10)  # Award 10 points for each asteroid destroyed
                            shot.kill()
                            break
                pygame.display.flip()
                dt = clock.tick(60) / 1000.0
                if game_over:
                    result = show_gameover_screen(screen, score.get_score())
                    if result == "restart":
                        # Clear all groups for a fresh start
                        updateable.empty()
                        drawable.empty()
                        asteroids.empty()
                        shots.empty()
                        score.reset()
                        break  # Restart game loop


if __name__ == "__main__":
    main()