import pygame
from Utils import *

# Let's setup some global variables
_dirty_rects = []
_clear_this_frame = []
_clear_next_frame = []
_layers = []
_static_blits = {}
_blits = []

## Auxillary functions to help with scaling
def _scale_pos(t):
    """ Scales a position tuple """
    global _scalefactor
    return (int(t[0] * _scalefactor[0]), int(t[1] * _scalefactor[1]))
    
def _unscale_pos(t):
    """ Unscales a position tuple """
    global _scalefactor
    return (int(t[0] / _scalefactor[0]), int(t[1] / _scalefactor[1]))
    
def _scale_rect(r):
    """ Scales a rectangle """
    global _scalefactor
    return pygame.Rect(_scale_pos((r.left, r.top)),
                       _scale_pos((r.width, r.height)))

def _unscale_rect(r):
    """ Unscales a retangle """
    global _scalefactor
    return pygame.Rect(_unscale_pos((r.left, r.top)),
                       _unscale_pos((r.width, r.height)))

@memoize
def _scale_surface(s):
    t = pygame.transform.smoothscale(s, _scale_pos(s.get_size()), pygame.Surface(_scale_pos(s.get_size())).convert_alpha())
    return t

def static_blit(name, surface, position, layer):
    global _static_blits
    r = pygame.rect.Rect(position, surface.get_size())
    _static_blits['name'] = (_scale_surface(surface),
                             _scale_rect(r),
                             __verify_layer(layer))
    # We also add this as a moving blit for one frame, so that it actually
    # gets drawn
    moving_blit(surface, position, layer)

def moving_blit(surface, position, layer):
    global _blits
    _blits.append( (_scale_surface(surface),
                    _scale_pos(position),
                    __verify_layer(layer)))

def __sort_blits(blits):
    """ Takes in a list of tuples (surface, position, layer) and sorts it by
    layer in place. """
    global _layers
    # This may get slow if there are a lot of layers, but it's the least
    # memory intensive version
    blits.sort(__sort_blits_cmp)

def __sort_blits_cmp(x, y):
    global _layers
    return _layers.index(x[2]) - _layers.index(y[2])

def __verify_layer(layer):
    global _layers
    if layer in _layers:
        return layer
    else:
        return _layers[0]

def init(bg, virtual_size = (1024,768), real_size = (0,0), fullscreen = 0):
    global _vsize, _rsize, _scalefactor, _screen, _background
    
    flags = 0
    if fullscreen:
        flags = pygame.FULLSCREEN
    screen = pygame.display.set_mode(real_size, flags)
    real_size = screen.get_size()

    pygame.display.set_caption("APH")
    background = load_image(bg)
    background = pygame.transform.smoothscale(background, real_size).convert()
    screen.blit(background, (0,0))
    pygame.display.flip()
    

    _scalefactor = (float(real_size[0])/virtual_size[0],
              float(real_size[1])/virtual_size[1])
    _vsize, _rsize = virtual_size, real_size
    _screen = screen
    _background = background
    
def init_layers(layers):
    global _layers
    _layers = layers
    
def __update():
    global _dirty_rects, _clear_this_frame, _clear_next_frame, _layers
    global _blits, _static_blits, _background, _screen
    
    # Let's finish up any rendering from the previous frame
    # First, we put the background over all blits
    for i in _clear_this_frame:
        b = _background.subsurface(i)
        _screen.blit(b, i)

    # Now, we need to blit layers, while simultaneously re-blitting
    # any static blits which were obscured    
    s = _static_blits.values()
    __sort_blits(s)
    __sort_blits(_blits)
    i = j = 0
    print s
    print _blits
    # Reminder: blits are (surf, pos, layer)
    for layer in _layers:
        while i < len(s) and s[i][2] == layer:
            surf, pos, layer = s[i]
            # Now, does this need to be redrawn
            for rect in _clear_this_frame:
                if pos.colliderect(rect):
                    x = pos.clip(rect)
                    y = x.move(-pos.left,-pos.top)
                    b = surf.subsurface(y)
                    _screen.blit(b, x)
            i = i+1
        while j < len(_blits) and _blits[j][2] == layer:
            # These are moving blits, so we need to make sure that
            # they will be cleared on the next frame
            r = _screen.blit(_blits[j][0], _blits[j][1])
            _clear_next_frame.append(r)
            j = j + 1
    
    # Do the display update
    pygame.display.update(_clear_next_frame + _clear_this_frame)
    # Get ready for the next call
    _clear_this_frame = _clear_next_frame
    _clear_next_frame = []
    _blits = []