class Drawable(Object):
    """ This class is somewhat analagous to Sprites in pygame. In APH,  they
    are much simpler, as all the dirty rendering and layering is hidden
    behind the scenes. A Drawable object needs to do nothing but implement a
    draw() method, and it should use one of the APH blit methods to draw
    the sprite, and an update() method which can be called each frame."""
    def draw():
        """ Draw this object to the display. """
        raise NotImplementedError("Drawable objects should implement draw()")
    def update():
        """ Called once per frame. """
        raise NotImplementedError("Drawable objects should implement update()")
        
class DrawableGroup(Object):
    """ This class is somewhat analagous to sprite groups in pygame. """
    
    def __init__(self, *args):
        self.drawables = list(args)
        
    def draw(self):
        """ Calls draw on all of its drawable objects. """
        map(lambda x: x.draw(), self.drawables)
    
    def update(self):
        """ Calls update on all of its drawable objects. """ 
        map(lambda x: x.update(), self.drawables)
        
    def remove(self, obj):
        """ Removes an object from its drawable list. """
        if obj in self.drawables:
            self.drawables.remove(obj)
    
    def add(self, obj):
        """ Adds an object to its drawable list. """
        self.drawables.append(obj)
        
    def get_list(self):
        """ Returns its list of drawable objects. """
        return self.drawables