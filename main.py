import pygame
import sys
import time
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from startscreen import *
from score import Score
from starfield import Starfield
from countdown import show_countdown

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
            
            # Show countdown with starfield and player in background
            if not show_countdown(screen, starfield, player):
                return  # User quit during countdown
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                # Clear screen with black
                screen.fill((0, 0, 0))
                
                if hasattr(player, 'velocity'):
                    starfield.update(player.velocity.x * 0.1, player.velocity.y * 0.1)
                starfield.draw(screen)
                
                updateable.update(dt)
                score.update(time.time())
                
                for obj in drawable:
                    obj.draw(screen)
                score.draw(screen)
                player.draw_lives(screen)
                
                game_over = False
                if not player.invincible:
                    for obj in asteroids:
                        if player.collision(obj):
                            if player.lose_life():
                                game_over = True
                            break
                        
                for obj in asteroids:
                    for shot in shots:
                        if obj.collision(shot):
                            obj.split()
                            score.add(10)
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
                        
                        # Reinitialize game objects
                        player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
                        asteroidfield = AsteroidField()
                        score = Score()
                        
                        # Show countdown with starfield and player in background
                        if not show_countdown(screen, starfield, player):
                            break  # User quit during countdown, go back to start screen
                        
                        # Reset game loop variables
                        dt = 0
                        game_over = False
                        continue  # Continue with the new game state
                    else:
                        # If not restarting, go back to start screen
                        break


if __name__ == "__main__":
    main()