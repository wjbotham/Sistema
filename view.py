import pygame
from vector import Vector
from math import sqrt
from threading import Thread
import tkinter

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GRAY = (127,127,127)
GREEN = (0,255,0)

class View:
    def __init__(self,universe):
        self.universe = universe
        self._trackee = max(self.universe.bodies, key=lambda b: b.mass)
        self._range_sel = None
        self.pixel_width = 800
        
        pygame.init()
        self.font = pygame.font.SysFont(None, 14)
        #create the screen
        self.window = pygame.display.set_mode((self.pixel_width, self.pixel_width))
        self._origin = universe.center_of_mass()
        self._km_radius = max((body.position - self.origin).magnitude() for body in self.universe.bodies)*1.05
        self.update()

        # all of this should be abstracted into a ControlPanel class or something
        self.info_panel = tkinter.Tk()
        self.info_panel.protocol("WM_DELETE_WINDOW", lambda: None)
        self.info_frame = tkinter.Frame(self.info_panel, width=256, height=512)
        self.info_frame.pack_propagate(0)
        self.info_frame.pack()
        self.info_panel.body_name = tkinter.Label(self.info_frame, text="Hello, World!", anchor=tkinter.W)
        self.info_panel.body_name.pack(fill=tkinter.X)
        self.info_panel.body_mass = tkinter.Label(self.info_frame, text="Hello, World!", anchor=tkinter.W)
        self.info_panel.body_mass.pack(fill=tkinter.X)

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

    def get_trackee(self):
        return self._trackee
    def set_trackee(self,trackee):
        self._trackee = trackee
        self.info_panel.body_mass.config(text="Mass: %.2E kg" % self._trackee.mass)
        self.info_panel.body_name.config(text="Name: "+self._trackee.name)
        self.update()
    trackee = property(get_trackee,set_trackee)

    def get_range_sel(self):
        return self._range_sel
    def set_range_sel(self,range_sel):
        self._range_sel = range_sel
        self.update()
    range_sel = property(get_range_sel,set_range_sel)

    def ui_loop(self):
        info_panel_thread = Thread(target=self.info_panel.mainloop)
        info_panel_thread.start()
        #input handling (somewhat boilerplate code):
        while True: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.info_panel.quit()
                    self.universe.view = None
                    return
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.recenter_click(event)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    self.ranging_click(event)
                elif event.type == pygame.KEYDOWN and (event.unicode == 'a' or event.unicode == 'A'):
                    self.km_radius *= 1.6
                elif event.type == pygame.KEYDOWN and (event.unicode == 'z' or event.unicode == 'Z'):
                    self.km_radius /= 1.6
                #else:
                #    print(event)

    def recenter_click(self,event):
        subject = self.find_subject_body(event)
        if subject:
            self.trackee = subject

    def ranging_click(self,event):
        subject = self.find_subject_body(event)
        if subject:
            if self.range_sel:
                print("%.2E" % subject.distance(self.range_sel))
                self.range_sel = None
            else:
                self.range_sel = subject

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
        if self.trackee:
            x = self.trackee.position.x
            y = self.trackee.position.y
            self.origin = Vector(x,y,0)
        else:
            self.origin = self.universe.center_of_mass()
        self.window.fill(BLACK)
        text = self.font.render("%.2E" % self.km_radius, True, LIGHT_GRAY, BLACK)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = (24,7)
        self.window.blit(text, textRect)
        for body in sorted(self.universe.bodies,key=lambda b: b.mass):
            pos = self.km_to_px(body.position.x,body.position.y)
            text = self.font.render(body.name, True, LIGHT_GRAY, BLACK)
            textRect = text.get_rect()
            textRect.centerx,textRect.centery = pos
            textRect.centery += 8
            self.window.blit(text, textRect)
            text = self.font.render("%.2E" % body.position.z, True, LIGHT_GRAY, BLACK)
            textRect = text.get_rect()
            textRect.centerx,textRect.centery = pos
            textRect.centery += 19
            self.window.blit(text, textRect)
            pygame.draw.circle(self.window, WHITE, pos, 2, 0)
            if body == self.range_sel:
                pygame.draw.circle(self.window, GREEN, pos, 5, 1)
        #draw it to the screen
        # TODO: implement some way of tracking changes, then translate
        #       this to use pygame.display.update(rectangles)
        pygame.display.flip()
