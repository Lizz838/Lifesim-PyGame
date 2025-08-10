import pygame
from state_manager import BaseState

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        self.handle_x = self.rect.x + int((self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_rect = pygame.Rect(self.handle_x - 10, self.rect.y - 5, 20, 30)
                if handle_rect.collidepoint(event.pos):
                    self.dragging = True
                    return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update slider position
            relative_x = event.pos[0] - self.rect.x
            relative_x = max(0, min(self.rect.width, relative_x))
            self.handle_x = self.rect.x + relative_x
            
            # Update value
            progress = relative_x / self.rect.width
            self.val = self.min_val + progress * (self.max_val - self.min_val)
            return True
        return False
        
    def draw(self, screen, font):
        # Draw label
        label_surface = font.render(f"{self.label}: {self.val:.1f}", True, (255, 255, 255))
        screen.blit(label_surface, (self.rect.x, self.rect.y - 25))
        
        # Draw slider track
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        # Draw slider handle
        handle_rect = pygame.Rect(self.handle_x - 10, self.rect.y - 5, 20, 30)
        pygame.draw.rect(screen, (150, 150, 150), handle_rect)
        pygame.draw.rect(screen, (255, 255, 255), handle_rect, 2)

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
        color = (100, 100, 100) if self.is_hovered else (70, 70, 70)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class OptionsState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = None
        self.button_font = None
        self.sliders = []
        self.buttons = []
        self.settings = {
            'master_volume': 0.7,
            'sfx_volume': 0.8,
            'music_volume': 0.6,
            'fullscreen': False
        }
        self.previous_state = "title"  # Track where we came from
        
    def enter(self):
        self.font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)
        
        # Create sliders
        self.sliders = [
            Slider(300, 200, 200, 0.0, 1.0, self.settings['master_volume'], "Master Volume"),
            Slider(300, 280, 200, 0.0, 1.0, self.settings['sfx_volume'], "SFX Volume"), 
            Slider(300, 360, 200, 0.0, 1.0, self.settings['music_volume'], "Music Volume")
        ]
        
        # Create buttons
        fullscreen_text = "Windowed" if self.settings['fullscreen'] else "Fullscreen"
        self.buttons = [
            Button(300, 440, 200, 50, fullscreen_text, self.button_font),
            Button(250, 520, 100, 40, "Back", self.button_font),
            Button(450, 520, 100, 40, "Apply", self.button_font)
        ]
        
    def update(self, dt):
        # Update settings from sliders
        self.settings['master_volume'] = self.sliders[0].val
        self.settings['sfx_volume'] = self.sliders[1].val
        self.settings['music_volume'] = self.sliders[2].val
        
    def draw(self, screen):
        screen.fill((20, 20, 40))
        
        # Title
        title = self.font.render("Options", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=400, y=50)
        screen.blit(title, title_rect)
        
        # Draw sliders
        for slider in self.sliders:
            slider.draw(screen, self.button_font)
            
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
            
        # Instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Drag sliders to adjust audio levels",
            "Changes take effect immediately"
        ]
        for i, instruction in enumerate(instructions):
            text = instruction_font.render(instruction, True, (180, 180, 180))
            screen.blit(text, (50, 100 + i * 25))
            
    def handle_event(self, event):
        # Handle sliders
        for slider in self.sliders:
            slider.handle_event(event)
            
        # Handle buttons
        for i, button in enumerate(self.buttons):
            if button.handle_event(event):
                if i == 0:  # Toggle fullscreen
                    self.settings['fullscreen'] = not self.settings['fullscreen']
                    button.text = "Windowed" if self.settings['fullscreen'] else "Fullscreen"
                elif i == 1:  # Back
                    # Return to previous state (could be title or game)
                    if hasattr(self.state_manager, 'states') and 'game' in self.state_manager.states:
                        # If we came from the game, go back to game
                        if self.previous_state == "game":
                            self.state_manager.change_state("game")
                        else:
                            self.state_manager.change_state("title")
                    else:
                        self.state_manager.change_state("title")
                elif i == 2:  # Apply
                    self.apply_settings()
                    
        # Handle ESC key to go back
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.previous_state == "game":
                    self.state_manager.change_state("game")
                else:
                    self.state_manager.change_state("title")
                    
    def set_previous_state(self, state_name):
        """Called by other states to track where we came from"""
        self.previous_state = state_name
        
    def apply_settings(self):
        """Apply the current settings (placeholder for actual implementation)"""
        print(f"Settings applied:")
        print(f"  Master Volume: {self.settings['master_volume']:.1f}")
        print(f"  SFX Volume: {self.settings['sfx_volume']:.1f}")
        print(f"  Music Volume: {self.settings['music_volume']:.1f}")
        print(f"  Fullscreen: {self.settings['fullscreen']}")
        
        # Here you would actually apply the settings:
        # - Set pygame volume levels
        # - Toggle fullscreen mode
        # - Save settings to file
        # etc.