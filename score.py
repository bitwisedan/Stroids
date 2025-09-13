import pygame

class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.SysFont(None, 36)
    
    def add(self, points):
        """Add points to the current score."""
        self.value += points
    
    def reset(self):
        """Reset the score to zero."""
        self.value = 0
    
    def draw(self, screen):
        """Draw the current score on the screen."""
        score_text = self.font.render(f'Score: {self.value}', True, (255, 255, 255))
        text_rect = score_text.get_rect(midtop=(screen.get_width()//2, 10))
        screen.blit(score_text, text_rect)
    
    def get_score(self):
        """Get the current score value."""
        return self.value
