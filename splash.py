import pygame
from state_manager import BaseState

class SplashState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = None
        self.fade_timer = 0
        self.fade_duration = 2.0  # 2 seconds fade in/out
        self.display_duration = 1.0  # 1 second at full opacity
        self.total_duration = self.fade_duration * 2 + self.display_duration
        self.alpha = 0
        
    def enter(self):
        """Initialize splash screen elements"""
        self.font = pygame.font.Font(None, 72)
        self.fade_timer = 0
        
    def update(self, dt):
        """Handle fade in/out timing"""
        self.fade_timer += dt
        
        # Calculate alpha based on timer
        if self.fade_timer < self.fade_duration:
            # Fade in
            self.alpha = int(255 * (self.fade_timer / self.fade_duration))
        elif self.fade_timer < self.fade_duration + self.display_duration:
            # Full opacity
            self.alpha = 255
        elif self.fade_timer < self.total_duration:
            # Fade out
            fade_out_progress = (self.fade_timer - self.fade_duration - self.display_duration) / self.fade_duration
            self.alpha = int(255 * (1 - fade_out_progress))
        else:
            # Done, go to title screen
            self.state_manager.change_state("title")
            
    def draw(self, screen):
        """Draw splash screen"""
        screen.fill((0, 0, 0))
        
        # Create text surface
        text = self.font.render("Your Game Studio", True, (255, 255, 255))
        text.set_alpha(self.alpha)
        
        # Center text
        text_rect = text.get_rect()
        text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        
        screen.blit(text, text_rect)
        
    def handle_event(self, event):
        """Allow skipping splash with any key/click"""
        if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
            self.state_manager.change_state("title")