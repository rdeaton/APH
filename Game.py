import pygame
from Utils import *
from math import floor, ceil
from Screen import *

def GetGame():
    """ Returns the current GameState. """
    return GameState.stack[-1]
    
def GetScreen():
    """ Returns the current ScreenState from the current GameState"""
    return GetGame().screen_state

class GameState(object):
    """ Controls the current state of the program. """
    stack = []
    
    def __init__(self):
        """ Do some initialization. This puts filler variables in place
        of required instance variables. """
        self.quit = False
        self.screen_state = None
        self.layers = []
    
    def transition_in(self):
        """ Called when this state is transitioned into being. """
        pass

    def transition_out(self):
        """ Called when this state is transitioned out of being. """
        pass
        
    def main_loop(self):
        """ Called once per frame by APH. Should be sure to draw its
        ScreenState. """
        pass
        
    def push_state(self):
        """ Pushes the current state onto the stack and transitions into it. """
        if GameState.stack != []:
            GameState.stack[-1].transition_out()
        GameState.stack.append(self)
        self.transition_in()
        
    def pop_state(self):
        """ Pops the current state off of the stack and transitions back
        into the previous state. """
        self.transition_out()
        g = GameState.stack.pop()
        GetScreen().redraw()
        g.transition_in()
        
    def set_layers(self, layers):
        """ Sets the layers for the current game state, as a list of layers
        from bottom-most to top-most. """
        self.layers = layers
        self.screen_state.set_layers(layers)
        
class NewGame(GameState):
    """ Represents a new game, and sets up the screen accordingly. """
    def __init__(self, bg, virtual_size, real_size = (0,0), fullscreen = False):
        """ See: ScreenState.__init__ """
        GameState.__init__(self)
        self.screen_state = ScreenState(bg, virtual_size, real_size, fullscreen)

class SubGame(GameState):
    """ A game state which will set up the screen with the same parameters as
    used earlier in the game. Should be the base subclass for most GameStates.
    """
    def __init__(self):
        GameState.__init__(self)
        self.screen_state = GetScreen().copy()