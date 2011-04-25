# APH is APH Pygame Helper
# This file allows the user to import module APH
from Borg import BorgImpl
__all__ = ['Screen', 'Game', 'Utils', 'Sprite', 'Mouse']

def World():
    """ Returns a class which has it's state shared across all instances of
        the class. Use sparingly when information needs to be transferred
        between states and cannot be done via cleaner methods, such as
        abstraction into a module, or calling added member functions of the
        GameStates before pushing or popping on the stack. """
    return BorgImpl()