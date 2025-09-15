import pygame
import time

class Score:
    def __init__(self):
        self.value = 0
        self.multiplier = 1
        self.last_hit_time = 0
        self.multiplier_timeout = 2.0  # seconds before multiplier resets
        self.max_multiplier = 10  # Maximum multiplier cap
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.bar_width = 100
        self.bar_height = 10
    
    def update(self, current_time):
        """Update the multiplier based on time since last hit."""
        if current_time - self.last_hit_time > self.multiplier_timeout and self.multiplier > 1:
            self.multiplier = 1
    
    def add(self, points):
        """Add points to the current score with multiplier."""
        current_time = time.time()
        
        # If last hit was recent, increase multiplier (capped at max_multiplier)
        if current_time - self.last_hit_time < self.multiplier_timeout:
            self.multiplier = min(self.multiplier + 1, self.max_multiplier)
        else:
            self.multiplier = 1
            
        self.last_hit_time = current_time
        self.value += points * self.multiplier
    
    def reset(self):
        """Reset the score and multiplier to default values."""
        self.value = 0
        self.multiplier = 1
        self.last_hit_time = 0
    
    def draw(self, screen):
        """Draw the current score, multiplier, and multiplier timer bar on the screen."""
        # Draw score in top-left corner
        score_text = self.font.render(f'Score: {self.value}', True, (255, 255, 255))
        score_rect = score_text.get_rect(topleft=(10, 10))
        screen.blit(score_text, score_rect)
        
        # Draw multiplier below score if greater than 1
        if self.multiplier > 1:
            # Draw multiplier text
            multiplier_text = self.small_font.render(f'Multiplier: x{self.multiplier}', True, (255, 255, 0))
            multiplier_rect = multiplier_text.get_rect(topleft=(10, score_rect.bottom + 5))
            screen.blit(multiplier_text, multiplier_rect)
            
            # Calculate remaining time before multiplier resets
            current_time = time.time()
            time_remaining = max(0, (self.last_hit_time + self.multiplier_timeout) - current_time)
            time_ratio = time_remaining / self.multiplier_timeout
            
            # Draw timer bar background
            bar_bg_rect = pygame.Rect(10, multiplier_rect.bottom + 5, self.bar_width, self.bar_height)
            pygame.draw.rect(screen, (100, 100, 100), bar_bg_rect)
            
            # Draw timer bar fill
            bar_fill_width = int(self.bar_width * time_ratio)
            if bar_fill_width > 0:
                bar_fill_rect = pygame.Rect(10, multiplier_rect.bottom + 5, bar_fill_width, self.bar_height)
                # Change color based on time remaining (green to red)
                color_value = int(255 * time_ratio)
                bar_color = (255 - color_value, color_value, 0)
                pygame.draw.rect(screen, bar_color, bar_fill_rect)
    
    def get_score(self):
        """Get the current score value."""
        return self.value
