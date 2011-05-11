import pygame
from Utils import *
from math import floor, ceil

class ScreenState(object):
    """ This will store the state of the screen and handle scaling. """
    _screen = None
    
    def __init__(self, bg, virtual_size, real_size = (0,0), fullscreen = False):
        """ Initializes a screen state. On first call, sets up the pygame
            display, on subsequent calls, will readjust the virtual size
            if the scaling would like to be changed for a subportion of the
            program. bg is a tuple representing background color,
            virtual_size is a tuple representing the size of the virtual canvas,
            real_size is a tuple representing the real size of the canvas, if
            (0,0), it defaults to the current screen resolution, and
            fullscreen is a boolean which determines whether the game is
            fullscreened."""
        self._dirty_rects = []
        self._clear_this_frame = []
        self._clear_next_frame = []
        self._layers = []
        self._blits = []
        self._static_blits = {}

        if ScreenState._screen is None:
            flags = 0
            if fullscreen:
                flags = pygame.FULLSCREEN
            ScreenState._screen = pygame.display.set_mode(real_size, flags)
            pygame.display.set_caption("APH")
            real_size = ScreenState._screen.get_size()
            pygame.font.init()

        background = pygame.Surface(real_size)
        background.fill(bg)
        ScreenState._screen.blit(background, (0,0))
        pygame.display.flip()
        self._background = background

        real_size = self._screen.get_size()

        self._scalefactor = (float(real_size[0])/virtual_size[0],
                        float(real_size[1])/virtual_size[1])
        self._vsize, self._rsize = virtual_size, real_size
        
    def get_size(self):
        """ Returns the virtual resolution of the screen. """
        return self._vsize
        
    def set_background(self, bg):
        """ Set a new background image for the screen. Automatically
        scales it to the appropriate size. """
        if bg.get_size() != self._rsize:
            bg = pygame.transform.smoothscale(bg, self._rsize).convert()
        self._clear_this_frame.append(pygame.Rect((0,0), self._rsize))
        self._background = bg

        
    def copy(self):
        """ Makes a "copy" of the current screen state, which includes only
        the same virtual size, background, and layers. All static blits and
        other features will be ignored """
        s = ScreenState((0,0,0), self._vsize)
        s.set_background(self._background)
        s._layers = self._layers[:] # We don't want to ruin the original
        return s
        
    def set_layers(self, layers):
        """ Sets the layers for drawing, from bottom to highest. """
        self._layers = layers[:] # We don't want to rely on the original
    
    def get_layers(self):
        return self._layers[:]
    
    def __verify_layer(self, layer):
        """ Ensures that the layer passed in is a valid layer and returns it.
        If the layer is invalid, gives the bottom-most layer."""
        if layer in self._layers:
            return layer
        else:
            return self._layers[0]
            
    def redraw(self):
        """ Forces a redraw of everything in this screen. """
        self._clear_this_frame.append(self._screen.get_rect())
            
    def static_blit(self, name, surface, position, layer):
        r = pygame.rect.Rect(position, surface.get_size())
        self._static_blits['name'] = (self.__scale_surface(surface),
                                      self.scale_rect(r),
                                      self.__verify_layer(layer))
        # We also add this as a moving blit for one frame, so that it actually
        # gets drawn for the first time
        self.moving_blit(surface, position, layer)
    
    def moving_blit(self, surface, position, layer = ''):
        self._blits.append( (self.__scale_surface(surface),
                             self.scale_pos(position),
                             self.__verify_layer(layer)))
            
    def draw(self):
        """ Draws the current frame. Should be called only once per frame by
        the current GameState. """
        
        # The function for sorting blits. No use anywhere else
        def sort_blits(blits):
            """ Takes in a list of tuples (surface, position, layer) and sorts
            it by layer in place. """
            def sort_blits_cmp(x, y):
                # These calls to _layers.index could get costly with more layers
                return self._layers.index(x[2]) - self._layers.index(y[2])
            # This may get slow if there are a lot of layers, but it's the least
            # memory intensive version
            blits.sort(sort_blits_cmp)
        
        
        # Let's finish up any rendering from the previous frame
        # First, we put the background over all blits
        for i in self._clear_this_frame:
            b = self._background.subsurface(i)
            self._screen.blit(b, i)
        
        # Now, we need to blit layers, while simultaneously re-blitting
        # any static blits which were obscured    
        s = self._static_blits.values()
        sort_blits(s)
        sort_blits(self._blits)
        i = j = 0
        # Reminder: blits are (surf, pos, layer)
        for layer in self._layers:
            while i < len(s) and s[i][2] == layer:
                surf, pos, layer = s[i]
                # Now, does this need to be redrawn
                for rect in self._clear_this_frame:
                    if pos.colliderect(rect):
                        x = pos.clip(rect)
                        y = x.move(-pos.left,-pos.top)
                        b = surf.subsurface(y)
                        _screen.blit(b, x)
                i = i+1
            while j < len(self._blits) and self._blits[j][2] == layer:
                # These are moving blits, so we need to make sure that
                # they will be cleared on the next frame
                surf, pos = self._blits[j][0], self._blits[j][1]
                screen_rect = self._screen.get_rect()
                blit_rect = pygame.Rect(pos, surf.get_size())
                if screen_rect.contains(blit_rect):
                    r = self._screen.blit(surf, pos)
                    self._clear_next_frame.append(r)
                elif screen_rect.colliderect(blit_rect):
                    x = blit_rect.clip(screen_rect)
                    y = x.move(-blit_rect.left,-blit_rect.top)
                    b = surf.subsurface(y)
                    r = self._screen.blit(b, x)
                    self._clear_next_frame.append(r)              
                j = j + 1
        
        # Do the display update
        pygame.display.update(self._clear_next_frame + self._clear_this_frame)
        # Get ready for the next call
        self._clear_this_frame = self._clear_next_frame
        self._clear_next_frame = []
        self._blits = []
        
    def scale_pos(self, t):
        """ Scales a position tuple """
        global _scalefactor
        return (floor(t[0] * self._scalefactor[0]),
                ceil(t[1]  * self._scalefactor[1]))
    
    def unscale_pos(self, t):
        """ Unscales a position tuple """
        global _scalefactor
        return (floor(t[0] / self._scalefactor[0]),
                ceil(t[1]  / self._scalefactor[1]))
    
    def scale_rect(self, r):
        """ Scales a rectangle """
        return pygame.Rect((floor(r.left   * self._scalefactor[0]),
                            floor(r.top    * self._scalefactor[1])),
                           (ceil( r.width  * self._scalefactor[0]),
                            ceil( r.height * self._scalefactor[1])))
    
    def unscale_rect(self, r):
        """ Unscales a retangle """
        global _scalefactor
        return pygame.Rect((floor(r.left   / self._scalefactor[0]),
                            floor(r.top    / self._scalefactor[1])),
                           (ceil( r.width  / self._scalefactor[0]),
                            ceil( r.height / self._scalefactor[1])))
    
    def __scale_surface(self, s):
        """ Scales a surface from the virtual size to the real size """
        @memoize
        def scale(s, factor):
            size = s.get_size()
            new_size = (int(ceil(size[0] * factor[0])),
                       int(ceil(size[1] * factor[1])))
            t = pygame.transform.smoothscale(s,
                    new_size,
                    new_surface(new_size))
            return t
        return scale(s, self._scalefactor)