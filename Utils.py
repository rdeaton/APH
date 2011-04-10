import pygame

class memoize(object):
    """ This is a decorator to allow memoization of function calls. """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            res = self.func(*args)
            self.cache[args] = res
            return res
        except TypeError:
            return self.func(*args)
    def __repr__(self):
        return self.func.__doc__

@memoize
def load_image(fullname, colorkey=None):
    """ Load an image from a filename. colorkey is an optional parameter, if it
    is set, then the colorkey of the image is set. If colorkey is -1, then the
    colorkey is automatically determined from the top left corner. """
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
    return image.convert_alpha()
    
def dist2(pt1,pt2):
    """ Returns the square of a distance between two points"""
    return (pt1[0]-pt2[0]) ** 2 + (pt1[1]-pt2[1]) ** 2