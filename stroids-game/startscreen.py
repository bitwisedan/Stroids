import pygame
import sys

import pygame
import sys

def show_start_screen(screen):
    font = pygame.font.SysFont(None, 48)
    start_text = font.render("Start Game", True, (255, 255, 255))
    directions_text = font.render("Directions", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 40))
    directions_rect = directions_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 40))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(start_text, start_rect)
        screen.blit(directions_text, directions_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return "start"
                if directions_rect.collidepoint(event.pos):
                    return "directions"


def show_directions_screen(screen):
    font = pygame.font.SysFont(None, 36)
    lines = [
        "Directions:",
        "Arrow keys or WASD to move",
        "Spacebar to shoot",
        "Avoid asteroids!",
        "Press any key to return"
    ]
    screen.fill((0, 0, 0))
    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        rect = text.get_rect(center=(screen.get_width()//2, 100 + i*50))
        screen.blit(text, rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

import pygame
import sys

def show_gameover_screen(screen):
    font = pygame.font.SysFont(None, 48)
    gameover_text = font.render("Game Over!", True, (255, 0, 0))
    restart_text = font.render("Restart", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))
    gameover_rect = gameover_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 60))
    restart_rect = restart_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    quit_rect = quit_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 60))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(gameover_text, gameover_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()