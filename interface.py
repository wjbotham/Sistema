import pygame
from vector import Vector
from math import sqrt
from threading import Thread

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GRAY = (127,127,127)
GREEN = (0,255,0)

class Interface:
    def __init__(self,universe):
        self.universe = universe
        self._selected = max(self.universe.bodies, key=lambda b: b.mass)
        self.pixel_width = 800
        
        pygame.init()
        self.font = pygame.font.SysFont(None, 14)
        #create the screen
        self.window = pygame.display.set_mode((self.pixel_width, self.pixel_width))
        self._origin = universe.center_of_mass()
        self._km_radius = max((body.position - self.origin).magnitude() for body in self.universe.bodies)*1.05
        self.update()

    def quit(self):
        pygame.quit()
        self.universe.view = None

    def get_origin(self):
        return self._origin
    def set_origin(self, origin):
        self._origin = origin
    origin = property(get_origin,set_origin)

    def get_km_radius(self):
        return self._km_radius
    def set_km_radius(self,km_radius):
        self._km_radius = km_radius
        self.update()
    km_radius = property(get_km_radius,set_km_radius)

    def get_selected(self):
        return self._selected
    def set_selected(self,selected):
        self._selected = selected
        self.update()
    selected = property(get_selected,set_selected)

    def ui_loop(self):
        while True: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.recenter_click(event)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    self.ranging_click(event)
                elif event.type == pygame.KEYDOWN and (event.unicode == 'a' or event.unicode == 'A'):
                    self.km_radius *= 1.9
                elif event.type == pygame.KEYDOWN and (event.unicode == 'z' or event.unicode == 'Z'):
                    self.km_radius /= 1.9
                elif event.type == pygame.KEYDOWN and (event.unicode == 'p' or event.unicode == 'P'):
                    self.universe.paused = not self.universe.paused
                #else:
                #    print(event)

    def recenter_click(self,event):
        subject = self.find_subject_body(event)
        if subject:
            self.selected = subject

    def ranging_click(self,event):
        subject = self.find_subject_body(event)
        if subject:
            if self.selected:
                print("%.2E" % subject.distance(self.selected))

    def find_subject_body(self,event):
        ev_x,ev_y = event.pos
        candidates = []
        for body in self.universe.bodies:
            b_x,b_y = self.km_to_px(body.position.x,body.position.y)
            dist = sqrt((ev_x-b_x)**2 + (ev_y-b_y)**2)
            if dist <= 12:
                candidates.append(body)                    
        if len(candidates) > 0:
            return max(candidates,key=lambda body: body.mass)
        else:
            return None

    def km_to_px(self,x,y):
        nx = (x + self.km_radius - self.origin.x)*(self.pixel_width / (2*self.km_radius))
        ny = (y - self.km_radius - self.origin.y)*(self.pixel_width / (2*self.km_radius))*(-1)
        return (round(nx),round(ny))
    
    def px_to_km(self,x,y):
        nx = (x * 2 * self.km_radius / self.pixel_width     ) - self.km_radius + self.origin.x
        ny = (y * 2 * self.km_radius / self.pixel_width * -1) + self.km_radius + self.origin.y
        return (nx,ny)

    def update(self):
        if self.selected:
            x = self.selected.position.x
            y = self.selected.position.y
            self.origin = Vector(x,y,0)
        else:
            self.origin = self.universe.center_of_mass()
        self.window.fill(BLACK)
        text = self.font.render("%.2E" % self.km_radius, True, LIGHT_GRAY, BLACK)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = (24,7)
        self.window.blit(text, textRect)
        text = self.font.render("T+%d" % self.universe.time, True, LIGHT_GRAY, BLACK)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = (24,7+11)
        self.window.blit(text, textRect)
        for body in sorted(self.universe.bodies,key=lambda b: b.mass):
            pos = self.km_to_px(body.position.x,body.position.y)
            text = self.font.render(body.name, True, LIGHT_GRAY, BLACK)
            textRect = text.get_rect()
            textRect.centerx,textRect.centery = pos
            textRect.centery += 8
            self.window.blit(text, textRect)
            if body != self.selected:
                x_offset = body.position.x-self.selected.position.x
                y_offset = body.position.y-self.selected.position.y
                z_offset = body.position.z-self.selected.position.z
                xy_dist = sqrt(x_offset**2 + y_offset**2)
                if abs(z_offset) >= xy_dist/10:
                    text = self.font.render("%.2E" % z_offset, True, LIGHT_GRAY, BLACK)
                    textRect = text.get_rect()
                    textRect.centerx,textRect.centery = pos
                    textRect.centery += 19
                    self.window.blit(text, textRect)
            rel_height = ((body.position.z-self.selected.position.z)/self.km_radius)+0.5
            rel_height = max(0,min(1,rel_height))
            height_color = tuple(map(lambda n:n*rel_height,body.color))
            pygame.draw.circle(self.window, height_color, pos, 2, 0)
            if body == self.selected:
                pygame.draw.circle(self.window, GREEN, pos, 5, 1)
        #draw it to the screen
        # TODO: implement some way of tracking changes, then translate
        #       this to use pygame.display.update(rectangles)
        pygame.display.flip()
