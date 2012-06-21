import pygame
from vector import Vector
from math import sqrt
from ui_element import UIElement

BLACK      = (0,0,0)
WHITE      = (255,255,255)
LIGHT_GRAY = (127,127,127)
GREEN      = (0,255,0)
RED        = (255,0,0)

class Interface:
    def __init__(self,universe,height=800,width=1000):
        self.universe = universe
        self._selected = max(self.universe.bodies, key=lambda b: b.mass)
        
        pygame.init()
        self.font = pygame.font.SysFont(None, 14)
        #create the screen
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self._origin = universe.center_of_mass()
        self._km_per_pixel = max((body.position - self.origin).magnitude() for body in self.universe.bodies)*1.05/min(height,width)

        self.ui_elements = [UIElement(self,100,150,100,150,GREEN)]
        self.grabbed_element = None
        self.update()

    def quit(self):
        pygame.quit()
        self.universe.view = None

    def get_origin(self):
        return self._origin
    def set_origin(self, origin):
        self._origin = origin
    origin = property(get_origin,set_origin)

    def get_km_per_pixel(self):
        return self._km_per_pixel
    def set_km_per_pixel(self,km_per_pixel):
        self._km_per_pixel = km_per_pixel
        self.update()
    km_per_pixel = property(get_km_per_pixel,set_km_per_pixel)

    def get_aspect_ratio(self):
        return self.pixel_height / self.pixel_width
    aspect_ratio = property(get_aspect_ratio)

    def get_pixel_width(self):
        return self.window.get_size()[0]
    pixel_width = property(get_pixel_width)

    def get_pixel_height(self):
        return self.window.get_size()[1]
    pixel_height = property(get_pixel_height)

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
                    self.handle_left_mouse_up(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_left_mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    self.ranging_click(event)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_down(event)
                elif event.type == pygame.MOUSEMOTION:
                    if self.grabbed_element:
                        mx,my = event.pos
                        ox,oy = self.grabbed_element.picked_up
                        self.grabbed_element.x,self.grabbed_element.y = mx+ox,my+oy
                        self.update()
                elif event.type == pygame.VIDEORESIZE:
                    self.window = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    # TODO Move floaty windows so they don't get lost outside of the display area
                    # TODO Figure out how to avoid the ugly streaking when resized larger
                    self.update()
                else:
                    print(event)

    def handle_key_down(self,event):
        if event.unicode == 'a' or event.unicode == 'A':
            self.km_per_pixel *= 1.9
        elif event.unicode == 'z' or event.unicode == 'Z':
            # this filter is here so we don't magnify to the point where it breaks,
            # so fix that bug and then remove this TODO
            if self.km_per_pixel / 1.9 > 2:
                self.km_per_pixel /= 1.9
        elif event.unicode == 'p' or event.unicode == 'P':
            self.universe.paused = not self.universe.paused

    def handle_left_mouse_up(self,event):
        self.grabbed_element = None
        x,y = event.pos
        for element in self.ui_elements:
            if element.contains(x,y):
                element.handle_left_mouse_up(event)
                return
        self.recenter_click(event)

    def handle_left_mouse_down(self,event):
        x,y = event.pos
        for element in self.ui_elements:
            if element.contains(x,y):
                element.handle_left_mouse_down(event)
                return
        
    def recenter_click(self,event):
        subject = self.find_subject_body(event)
        if subject:
            self.selected = subject

    def ranging_click(self,event):
        subject = self.find_subject_body(event)
        if subject:
            if self.selected:
                print("%.2E" % subject.distance(self.selected))
                
    def pixel_radius(self,body):
        return max(2,round(body.radius / self.km_per_pixel))

    def find_subject_body(self,event):
        ev_x,ev_y = event.pos
        candidates = []
        for body in self.universe.bodies:
            b_x,b_y = self.km_to_px(body.position.x,body.position.y)
            dist = sqrt((ev_x-b_x)**2 + (ev_y-b_y)**2)
            if dist <= 10 + self.pixel_radius(body):
                candidates.append(body)                    
        if len(candidates) > 0:
            return max(candidates,key=lambda body: body.mass)
        else:
            return None

    def km_to_px(self,x,y):
        ox,oy = self.origin.x,self.origin.y
        nx = round(((x-ox) / self.km_per_pixel) + (self.pixel_width  / 2))
        ny = round(((y-oy) / self.km_per_pixel) + (self.pixel_height / 2))
        return (nx,ny)
    
    def px_to_km(self,x,y):
        ox,oy = self.origin.x,self.origin.y
        nx = ((x - (self.pixel_width  / 2)) * self.km_per_pixel) + ox
        ny = ((y - (self.pixel_height / 2)) * self.km_per_pixel) + oy
        return (nx,ny)

    def update(self):
        if self.selected:
            x = self.selected.position.x
            y = self.selected.position.y
            self.origin = Vector(x,y,0)
        else:
            self.origin = self.universe.center_of_mass()
        self.window.fill(BLACK)
        self.draw_text(["%.2E" % self.km_per_pixel, "T+%d" % self.universe.time], 1, 1, LIGHT_GRAY, BLACK)
        for body in sorted(self.universe.bodies,key=lambda b: b.mass):
            self.draw_body(body)
        for element in reversed(self.ui_elements):
            self.draw_element(element)
        # draw it to the screen
        # TODO: implement some way of tracking changes, then translate
        #       this to use pygame.display.update(rectangles)
        pygame.display.flip()

    def draw_body(self,body):
        pos = self.km_to_px(body.position.x,body.position.y)
        pixel_radius = self.pixel_radius(body)
        visible_x = (-pixel_radius <= pos[0] <= self.pixel_width  + pixel_radius)
        visible_y = (-pixel_radius <= pos[1] <= self.pixel_height + pixel_radius)
        if not (visible_x and visible_y):
            return
        pygame.draw.circle(self.window, body.color, pos, pixel_radius, 0)
        text = self.font.render(body.name, True, LIGHT_GRAY, BLACK)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = pos
        textRect.centery += 6 + pixel_radius
        self.window.blit(text, textRect)

    def draw_element(self,element):
        s = pygame.Surface((element.width,element.height), pygame.SRCALPHA)
        s.fill(element.color+(128,))
        self.window.blit(s, (element.x,element.y))
        for button in element.buttons:
            s = pygame.Surface((button.width,button.height))
            s.fill(button.color+(255,))
            self.window.blit(s, (button.x+element.x,button.y+element.y))
        info = [self.selected.name,
                "%.2E kg" % self.selected.mass,
                "%.2E km" % (self.selected.position - self.universe.sun.position).magnitude()]
        self.draw_text(info, element.x+2, element.y+2, BLACK, None, 128)

    def draw_text(self,text_ary,x,y,text_color,background_color=None,alpha=255):
        line = text_ary[0]

        w,h = self.font.size(line)
        if background_color:
            text = self.font.render(line, True, text_color, background_color)
        else:
            text = self.font.render(line, True, text_color)
        text.set_alpha(alpha)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = x+w/2,y+h/2

        if len(text_ary) > 1:
            self.draw_text(text_ary[1:], x, y+h, text_color, background_color, alpha)
        self.window.blit(text, textRect)
        
