import pygame

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
    return image.convert()
    
def dist2(x,y):
    return (x[0]-y[0]) ** 2 + (x[1]-y[1]) ** 2