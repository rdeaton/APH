# APH is APH Pygame Helper
# This file allows the user to import module APH
from Game import GameState

def GetGame():
    """ Returns the current GameState. """
    return GameState.stack[-1]
    
def GetScreen():
    """ Returns the current ScreenState from the current GameState"""
    return GetGame().screen_state