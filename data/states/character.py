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
        color = (100, 100, 100) if self.is_hovered else (70, 70, 70)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class CharacterState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = None
        self.button_font = None
        self.buttons = []
        self.character_name = "Hero"
        self.character_class = "Warrior"
        self.classes = ["Warrior", "Mage", "Rogue", "Archer"]
        self.class_index = 0
        self.typing_name = False
        self.cursor_timer = 0
        
    def enter(self):
        self.font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)
        
        self.buttons = [
            Button(200, 200, 150, 40, "Name", self.button_font),
            Button(450, 200, 40, 40, "<", self.button_font),
            Button(650, 200, 40, 40, ">", self.button_font),
            Button(250, 450, 120, 50, "Start Game", self.button_font),
            Button(430, 450, 120, 50, "Back", self.button_font)
        ]
        
    def update(self, dt):
        self.cursor_timer += dt
        
    def draw(self, screen):
        screen.fill((40, 20, 60))
        
        # Title
        title = self.font.render("Character Creation", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=400, y=50)
        screen.blit(title, title_rect)
        
        # Name section
        name_label = self.button_font.render("Name:", True, (255, 255, 255))
        screen.blit(name_label, (200, 160))
        
        # Name input box
        name_box = pygame.Rect(200, 200, 150, 40)
        color = (100, 100, 100) if self.typing_name else (70, 70, 70)
        pygame.draw.rect(screen, color, name_box)
        pygame.draw.rect(screen, (200, 200, 200), name_box, 2)
        
        # Name text with cursor
        name_text = self.character_name
        if self.typing_name and int(self.cursor_timer * 2) % 2:
            name_text += "|"
        name_surface = self.button_font.render(name_text, True, (255, 255, 255))
        screen.blit(name_surface, (name_box.x + 5, name_box.y + 8))
        
        # Class section
        class_label = self.button_font.render("Class:", True, (255, 255, 255))
        screen.blit(class_label, (450, 160))
        
        # Class display
        class_text = self.button_font.render(self.character_class, True, (255, 255, 255))
        class_rect = class_text.get_rect(center=(550, 220))
        screen.blit(class_text, class_rect)
        
        # Character preview (simple colored rectangle)
        preview_rect = pygame.Rect(300, 280, 200, 120)
        class_colors = {
            "Warrior": (200, 100, 100),
            "Mage": (100, 100, 200), 
            "Rogue": (100, 200, 100),
            "Archer": (200, 200, 100)
        }
        color = class_colors.get(self.character_class, (150, 150, 150))
        pygame.draw.rect(screen, color, preview_rect)
        pygame.draw.rect(screen, (255, 255, 255), preview_rect, 3)
        
        # Class description
        descriptions = {
            "Warrior": "Strong melee fighter with high defense",
            "Mage": "Casts powerful spells from a distance",
            "Rogue": "Quick and sneaky with critical strikes", 
            "Archer": "Ranged attacks with bow and arrow"
        }
        desc = descriptions.get(self.character_class, "")
        desc_surface = pygame.font.Font(None, 24).render(desc, True, (200, 200, 200))
        desc_rect = desc_surface.get_rect(centerx=400, y=420)
        screen.blit(desc_surface, desc_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
            
    def handle_event(self, event):
        # Handle button clicks
        for i, button in enumerate(self.buttons):
            if button.handle_event(event):
                if i == 0:  # Name button
                    self.typing_name = not self.typing_name
                elif i == 1:  # Previous class
                    self.class_index = (self.class_index - 1) % len(self.classes)
                    self.character_class = self.classes[self.class_index]
                elif i == 2:  # Next class
                    self.class_index = (self.class_index + 1) % len(self.classes)
                    self.character_class = self.classes[self.class_index]
                elif i == 3:  # Start Game
                    self.state_manager.change_state("game")
                elif i == 4:  # Back
                    self.state_manager.change_state("title")
                    
        # Handle name typing
        if self.typing_name:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    self.typing_name = False
                elif event.key == pygame.K_BACKSPACE:
                    self.character_name = self.character_name[:-1]
                else:
                    if len(self.character_name) < 12:  # Max name length
                        self.character_name += event.unicode