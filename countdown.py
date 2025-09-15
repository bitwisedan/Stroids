import pygame
import time

def show_countdown(screen, starfield=None, player=None):
    """Display a 3-2-1 countdown before the game starts with game background."""
    font = pygame.font.SysFont(None, 120)
    
    for i in range(3, 0, -1):
        # Clear with solid black
        screen.fill((0, 0, 0))
        
        # Draw the game background (starfield and player if provided)
        if starfield is not None:
            starfield.draw(screen)
        if player is not None:
            player.draw(screen)
            
        # Draw countdown number in a circle for better visibility
        count_text = font.render(str(i), True, (255, 255, 255))
        text_rect = count_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
        
        # Draw a circle behind the number
        circle_radius = max(count_text.get_width(), count_text.get_height()) // 2 + 20
        pygame.draw.circle(screen, (0, 0, 0), text_rect.center, circle_radius)
        pygame.draw.circle(screen, (255, 255, 255), text_rect.center, circle_radius, 3)  # White border
        
        # Draw the number
        screen.blit(count_text, text_rect)
        
        pygame.display.flip()
        time.sleep(1)  # Wait for 1 second
        
        # Check for quit events during countdown
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
    
    # Clear the screen one last time
    screen.fill((0, 0, 0))
    if starfield is not None:
        starfield.draw(screen)
    if player is not None:
        player.draw(screen)
    pygame.display.flip()
    return True
