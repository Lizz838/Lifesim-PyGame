import pygame
import sys
from state_manager import StateManager
from states.splash import SplashState
from states.title import TitleState
from states.character import CharacterState
from states.game_state import GameState
from states.options import OptionsState

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Your Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize state manager
        self.state_manager = StateManager()
        
        # Create and add states
        self.state_manager.add_state("splash", SplashState())
        self.state_manager.add_state("title", TitleState())
        self.state_manager.add_state("character", CharacterState())
        self.state_manager.add_state("game", GameState())
        self.state_manager.add_state("options", OptionsState())
        
        # Start with splash screen
        self.state_manager.change_state("splash")
        
    def run(self):
        """Main game loop"""
        while self.running:
            # Calculate delta time (in seconds)
            dt = self.clock.tick(60) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.state_manager.handle_event(event)
            
            # Update
            self.state_manager.update(dt)
            
            # Draw
            self.screen.fill((0, 0, 0))  # Clear screen
            self.state_manager.draw(self.screen)
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
