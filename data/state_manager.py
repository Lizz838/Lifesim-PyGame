import pygame

class StateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.next_state = None
        
    def add_state(self, name, state):
        """Add a state to the manager"""
        self.states[name] = state
        state.state_manager = self
        
    def change_state(self, state_name):
        """Queue a state change"""
        if state_name in self.states:
            self.next_state = state_name
            
    def update(self, dt):
        """Update current state and handle state changes"""
        # Handle state transitions
        if self.next_state:
            if self.current_state:
                self.states[self.current_state].exit()
            self.current_state = self.next_state
            self.states[self.current_state].enter()
            self.next_state = None
            
        # Update current state
        if self.current_state:
            self.states[self.current_state].update(dt)
            
    def draw(self, screen):
        """Draw current state"""
        if self.current_state:
            self.states[self.current_state].draw(screen)
            
    def handle_event(self, event):
        """Pass events to current state"""
        if self.current_state:
            self.states[self.current_state].handle_event(event)

class BaseState:
    """Base class for all game states"""
    def __init__(self):
        self.state_manager = None
        
    def enter(self):
        """Called when entering this state"""
        pass
        
    def exit(self):
        """Called when leaving this state"""
        pass
        
    def update(self, dt):
        """Update state logic"""
        pass
        
    def draw(self, screen):
        """Draw state to screen"""
        pass
        
    def handle_event(self, event):
        """Handle pygame events"""
        pass