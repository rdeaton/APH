import pygame
from APH import *
import math
from APH.Utils import *
from APH.Game import *
from APH.Screen import *
from APH.Sprite import *


WIDTH = 400
HEIGHT = 300
FPS = 30.

class Ball(Sprite):
    """ A silly example which has a ball revolving around a point. """
    im = {}
    def __init__(self, layer, color, speed, center = (200,150), arc_size = 100):
        """ Layer is the layer to render on. Color is a color tuple. Speed is
            number of revolution per second, the center is the center of the arc,
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
        theta = (float(t) / FPS) * 2 * math.pi * self.speed
        self.position = (self.center[0] + self.arc_size * math.sin(theta),
                    self.center[1] + self.arc_size * math.cos(theta))

class Circles(SubGame):
    def __init__(self):
        SubGame.__init__(self)
        self.set_layers(['red', 'green', 'blue'])
        
        red = Ball('red', (255, 0, 0), 0.25)
        green = Ball('green', (0, 255, 0), 0.25 / 2.)
        blue = Ball('blue', (0, 0, 255), 0.5)
        
        self.circle_group = Group(red, green, blue)
        self.t = 0
        
    def main_loop(self):
        self.t = self.t + 1
        self.circle_group.update(self.t)
        self.circle_group.draw()
        
        GetScreen().draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                self.pop_state()

class Menu(NewGame):
    def __init__(self, *args):
        NewGame.__init__(self, *args)
        self.set_layers(['menu'])
        pygame.font.init()
        font = pygame.font.Font("assets/VeraMono.ttf", 20)
        text = font.render("Welcome to the ball demo", True, (0, 0, 0))
        
        welcome = Sprite()
        welcome.image = text
        welcome.position = ((WIDTH - text.get_width()) / 2, 100)
        
        font = pygame.font.Font("assets/VeraMono.ttf", 16)
        text = font.render("Press any key to continue", True, (0, 0, 0))

        cont = Sprite()
        cont.image = text
        cont.position = ((WIDTH - text.get_width()) / 2, 200)
        
        print welcome
        
        self.group = Group(welcome, cont)
        
    def main_loop(self):
        self.group.draw()
        
        GetScreen().draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                g = Circles()
                g.push_state()
        
if __name__ == "__main__":
    g = Menu((255, 255, 255), (WIDTH, HEIGHT), (0,0), True)
    g.push_state()
    clock = pygame.time.Clock()

    while not GetGame().quit:
        clock.tick(FPS)
        GetGame().main_loop()