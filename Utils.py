import pygame

class memoize(object):
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
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
    return image.convert_alpha()
    
def dist2(x,y):
    return (x[0]-y[0]) ** 2 + (x[1]-y[1]) ** 2