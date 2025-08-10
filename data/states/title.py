import pygame
from state_manager import BaseState

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False
        
    def draw(self, screen):
        # Button background
        color = (100, 100, 100) if self.is_hovered else (70, 70, 70)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        # Button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class TitleState(BaseState):
    def __init__(self):
        super().__init__()
        self.title_font = None
        self.button_font = None
        self.buttons = []
        
    def enter(self):
        """Initialize title screen"""
        self.title_font = pygame.font.Font(None, 96)
        self.button_font = pygame.font.Font(None, 48)
        
        # Create buttons
        self.buttons = [
            Button(300, 250, 200, 60, "New Game", self.button_font),
            Button(300, 330, 200, 60, "Options", self.button_font),
            Button(300, 410, 200, 60, "Quit", self.button_font)
        ]
        
    def update(self, dt):
        """Update title screen"""
        pass
        
    def draw(self, screen):
        """Draw title screen"""
        screen.fill((20, 20, 40))
        
        # Draw title
        title_text = self.title_font.render("Your Game", True, (255, 255, 255))
        title_rect = title_text.get_rect()
        title_rect.centerx = screen.get_width() // 2
        title_rect.y = 100
        screen.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
            
    def handle_event(self, event):
        """Handle button clicks"""
        for i, button in enumerate(self.buttons):
            if button.handle_event(event):
                if i == 0:  # New Game
                    self.state_manager.change_state("character")
                elif i == 1:  # Options
                    self.state_manager.change_state("options")
                elif i == 2:  # Quit
                    pygame.event.post(pygame.event.Event(pygame.QUIT))