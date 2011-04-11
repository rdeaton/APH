import pygame
from APH import *

class Sprite(object):
    """ Analagous to Sprite in pygame, but automatically handles dirty updates,
    and supports adding self.layer to allow layered rendering. This means that
    if the Sprite is repositioned or killed, the game background will
    automatically redraw over the sprite. These sprites support one additional
    feature, setting Sprite.position will automatically set Sprite.rect to a
    rect starting from position with the size of the image, and accessing
    Sprite.position will return the top left coordinate of Sprite.rect """
    
    def __setattr__(self, item, value):
        if item == 'position':
            self.rect = pygame.Rect((value[1], value[0]), self.image.get_size())
        else:
            self.__dict__[item] = value
            
    def __getattr__(self, item):
        if item == 'position':
            return (self.rect.top, self.rect.left)
        else:
            return self.__dict__[item]
    
    def __init__(self, *groups):
        """ Adds this sprite to any number of groups by default. """
        self.image = None
        self.rect = None
        self.layer = None
        self._groups = []
        self.add(*groups)
        
    def add(self, *groups):
        """ Add this sprite to groups."""
        for g in groups:
            if g.add(self):
                self._groups.append(g)
                
    def kill(self):
        """ Remove this sprite from all groups. """
        for g in self.groups:
            g.remove(self)
            
    def alive(self):
        """ Return True if this sprite belongs to any groups, false otherwise"""
        return len(groups) > 0
        
    def groups(self):
        """ Return a list of groups that this sprite belongs to. """
        return self._groups[:]
        
    def draw(self):
        """ Draw this object to the display. It will always use the current
            screen state for drawing. """
        Screen().moving_blit(self.image,
                             self.position,
                             self.layer)
    def update(self, *args):
        """ Called once per frame. """
        pass
        
class Group(object):
    """ Behaves like sprite.Group in pygame. """
    
    def __init__(self, *sprites):
        self._sprites = list(sprites)
        
    def draw(self):
        """ Calls draw on all of its Sprites. """
        map(lambda x: x.draw(), self._sprites)
    
    def update(self, *args):
        """ Calls update on all of its Sprites. """ 
        map(lambda x: x.update(*args), self._sprites)
        
    def remove(self, *sprites):
        """ Removes Sprites from this Group. """
        for sprite in sprites:
            if sprite in self._sprites:
                self._sprites.remove(sprite)
    
    def add(self, *sprites):
        """ Adds an object to its drawable list. """
        for sprite in sprites:
            if sprite not in self._sprites:
                self._sprites.append(sprite)
                sprite.add(self)
    
    def has(self, *sprites):
        """ Return true if all sprites are contained in the group. Unlike
        pygame, this does not take an iterator for each argument, only sprites.
        """
        for sprite in sprites:
            if sprite not in self._sprites:
                return False
        return True
    
    def empty(self):
        """ Clears all sprites from the group. """
        for sprite in self._sprites:
            sprite.remove(self)
        self._sprites = []