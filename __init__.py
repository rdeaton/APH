# APH is APH Pygame Helper
# This file allows the user to import module APH, and it will
# load the appropriate submodules and expose it's entire API through this file

import Screen

def init(bg, virtual_size = (1024, 768), real_size = (0,0), fullscreen = False):
    """ Initialize the APH library. bg is a color tuple for pygame,
    virtual_size is the drawable size available to the user,
    real_size is the size of the actual display. If real_size is (0,0),
    APH uses the current screen resolution, or a close size if fullscreened """
    Screen.init(bg, virtual_size, real_size, fullscreen)
    
def init_layers(layers):
    """ Turn on the optional layered rendering. layers is  list of layers which
    the application can draw to, ordered from bottom-most to top-most. """
    Screen.init_layers(layers)

def moving_blit(surface, position, layer=''):
    """ Blit an object to the screen which is moving, that is, blit for this
    frame only, and then clear it for the next frame. If layer is '', default
    to the bottom-most layer. """
    Screen.moving_blit(surface, position, layer)
    
def add_static_blit(name, surface, position, layer=''):
    """ Blit an object to the screen which is static, that is, blit it
    for every frame, ensuring that it remains blitted e.g. if a moving blit
    obscures it for a frame. Associated with the static_blit is a name so that
    it can be removed once it is no longer needed on screen. If layer is '',
    default to the bottom-most layer. """
    Screen.static_blit(name, surface, position, layer)
    
def update():
    """ Must be called once per frame. """
    Screen.update()
    
def set_background(im):
    """ Sets a new surface as the background image for the game. If im is not
    the size of the real display, then it is scaled accordingly """
    Screen.set_background(im)