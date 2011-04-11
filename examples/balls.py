import pygame
from APH import *
import math
from APH.Utils import *
from APH.Game import *
from APH.Screen import *
from APH.Sprite import *


WIDTH = 400
HEIGHT = 300

class Ball(Sprite):
    im = {}
    def __init__(self, layer, color, speed, center = (200, 150), arc_size = 100):
        """ Layer is the layer to render on. Color is a color tuple. Speed is
            number of rotations per second, the center is the center of the arc,
            and the arc_size is the radius of the arc. """
        Sprite.__init__(self)
        if color not in Ball.im:
            Ball.im[color] = new_surface((22,22))
            pygame.draw.circle(Ball.im[color], color, (11, 11), 10)
        self.image = Ball.im[color]
        self.layer = layer
        self.center = (200, 150)
        self.position = (0,0)
        self.speed = speed
        self.arc_size = arc_size
        
    def update(self, t):
        theta = t * 2 / self.speed * math.pi / 180 
        self.position = (self.center[0] + self.arc_size * math.sin(theta),
                    self.center[1] + self.arc_size * math.cos(theta))

class Circles(NewGame):
    def __init__(self, *args):
        NewGame.__init__(self, *args)
        self.set_layers(['red', 'green', 'blue'])
        
        red = Ball('red', (255, 0, 0), 0.5)
        green = Ball('green', (0, 255, 0), 0.75)
        blue = Ball('blue', (0, 0, 255), 0.25)
        
        self.circle_group = Group(red, green, blue)
        self.t = 0
        self.quit = False
        
    def main_loop(self):
        self.t = self.t + 1
        self.circle_group.update(self.t)
        self.circle_group.draw()
        
        Screen().draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.quit = True
        
        
if __name__ == "__main__":
    g = Circles((255, 255, 255), (WIDTH, HEIGHT), (0,0), True)
    g.push_state()
    print 'test'
    
    clock = pygame.time.Clock()

    while not Game().quit:
        clock.tick(30)
        Game().main_loop()
        print clock.get_fps()