# APH is APH Pygame Helper
# This file allows the user to import module APH
from Game import GameState

def Game():
    """ Returns the current GameState. """
    return GameState.stack[-1]
    
def Screen():
    return Game().screen_state