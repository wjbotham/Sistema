import pygame
from vector import Vector
import sys

class View:
    def __init__(self,universe):
        self.universe = universe
        self.origin = universe.center_of_mass()

        self.draw_limit = 1000
        pygame.init()
        #create the screen
        self.window = pygame.display.set_mode((self.draw_limit, self.draw_limit))
        self.update()

    def get_origin(self):
        return self._origin
    def set_origin(self, origin):
        self._origin = origin
        self.math_limit = max((body.position - self.origin).magnitude() for body in self.universe.bodies)
    origin = property(get_origin,set_origin)

    def ui_loop(self):
        #input handling (somewhat boilerplate code):
        while True: 
           for event in pygame.event.get(): 
              if event.type == pygame.QUIT:
                  pygame.quit()
                  return
              else:
                  print(event)
        
    def math_to_draw(self,x,y):
        nx = (x + self.math_limit - self.origin.x)*(self.draw_limit / (2*self.math_limit))
        ny = (y - self.math_limit + self.origin.y)*(self.draw_limit / (2*self.math_limit))*(-1)
        return (round(nx),round(ny))

    def update(self):
        self.window.fill((0,0,0))
        for body in self.universe.bodies:
            pygame.draw.circle(self.window, (255, 255, 255), self.math_to_draw(body.position.x,body.position.y), 2, 1)
        #draw it to the screen
        pygame.display.flip()
