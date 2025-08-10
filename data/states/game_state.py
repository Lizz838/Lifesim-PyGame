import pygame
from state_manager import BaseState

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200  # pixels per second
        self.size = 30
        
    def update(self, dt, keys):
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed * dt
            
        # Keep player on screen
        self.x = max(self.size//2, min(800 - self.size//2, self.x))
        self.y = max(self.size//2, min(600 - self.size//2, self.y))
        
    def draw(self, screen):
        pygame.draw.circle(screen, (100, 150, 255), (int(self.x), int(self.y)), self.size//2)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size//2, 3)

class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = None
        self.small_font = None
        self.player = None
        self.score = 0
        self.game_time = 0
        self.paused = False
        
    def enter(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.player = Player(400, 300)
        self.score = 0
        self.game_time = 0
        self.paused = False
        
    def update(self, dt):
        if not self.paused:
            self.game_time += dt
            
            # Get current key states
            keys = pygame.key.get_pressed()
            self.player.update(dt, keys)
            
            # Simple scoring system (time-based)
            self.score = int(self.game_time * 10)
        
    def draw(self, screen):
        # Background
        screen.fill((20, 40, 20))
        
        # Draw a simple grid pattern
        grid_size = 50
        for x in range(0, 800, grid_size):
            pygame.draw.line(screen, (0, 60, 0), (x, 0), (x, 600))
        for y in range(0, 600, grid_size):
            pygame.draw.line(screen, (0, 60, 0), (0, y), (800, y))
            
        # Draw player
        self.player.draw(screen)
        
        # HUD - Score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # HUD - Time
        time_text = self.font.render(f"Time: {self.game_time:.1f}s", True, (255, 255, 255))
        screen.blit(time_text, (10, 50))
        
        # HUD - Controls
        controls = [
            "WASD/Arrow Keys: Move",
            "ESC: Options",
            "P: Pause"
        ]
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, (200, 200, 200))
            screen.blit(control_text, (10, 550 + i * 20))
            
        # Pause overlay
        if self.paused:
            overlay = pygame.Surface((800, 600))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(400, 280))
            screen.blit(pause_text, pause_rect)
            
            resume_text = self.small_font.render("Press P to resume", True, (200, 200, 200))
            resume_rect = resume_text.get_rect(center=(400, 320))
            screen.blit(resume_text, resume_rect)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state("options")
            elif event.key == pygame.K_p:
                self.paused = not self.paused