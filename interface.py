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

        self.ui_elements = [UIElement(self,100,100,100,100,GREEN)]
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
                    self.handle_left_click(event)
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
                else:
                    print(event)

    def handle_key_down(self,event):
        if event.unicode == 'a' or event.unicode == 'A':
            self.km_radius *= 1.9
        elif event.unicode == 'z' or event.unicode == 'Z':
            # this filter is here so we don't magnify to the point where it breaks,
            # so fix that bug and then remove this TODO
            if self.km_radius > 10000:
                self.km_radius /= 1.9
        elif event.unicode == 'p' or event.unicode == 'P':
            self.universe.paused = not self.universe.paused

    def handle_left_click(self,event):
        x,y = event.pos
        for element in self.ui_elements:
            if element.contains(x,y):
                element.handle_left_click(event)
                return
        self.recenter_click(event)
        
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
        self.draw_text(["%.2E" % self.km_radius, "T+%d" % self.universe.time], 1, 1, LIGHT_GRAY, BLACK)
        '''
        text = self.font.render("%.2E" % self.km_radius, True, LIGHT_GRAY, BLACK)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = (24,7)
        self.window.blit(text, textRect)
        text = self.font.render("T+%d" % self.universe.time, True, LIGHT_GRAY, BLACK)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = (24,7+11)
        self.window.blit(text, textRect)
        '''
        for body in sorted(self.universe.bodies,key=lambda b: b.mass):
            self.draw_body(body)
        for element in self.ui_elements:
            self.draw_element(element)
        #draw it to the screen
        # TODO: implement some way of tracking changes, then translate
        #       this to use pygame.display.update(rectangles)
        pygame.display.flip()

    def draw_body(self,body):
        pos = self.km_to_px(body.position.x,body.position.y)
        text = self.font.render(body.name, True, LIGHT_GRAY, BLACK)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = pos
        textRect.centery += 8
        self.window.blit(text, textRect)
        if body != self.selected:
            x_offset,y_offset,z_offset = (body.position - self.selected.position).coord()
            xy_dist = sqrt(x_offset**2 + y_offset**2)
            #if abs(z_offset) >= xy_dist/10:
            #    text = self.font.render("%.2E" % z_offset, True, LIGHT_GRAY, BLACK)
            #    textRect = text.get_rect()
            #    textRect.centerx,textRect.centery = pos
            #    textRect.centery += 19
            #    self.window.blit(text, textRect)
        rel_height = ((body.position.z-self.selected.position.z)/self.km_radius)+0.5
        rel_height = max(0,min(1,rel_height))
        height_color = tuple(map(lambda n:n*rel_height,body.color))
        pygame.draw.circle(self.window, height_color, pos, 2, 0)
        if body == self.selected:
            pygame.draw.circle(self.window, GREEN, pos, 5, 1)

    def draw_element(self,element):
        s = pygame.Surface((element.height,element.width), pygame.SRCALPHA)
        s.fill(element.color+(128,))
        self.window.blit(s, (element.x,element.y))
        for button in element.buttons:
            s = pygame.Surface((button.height,button.width))
            s.fill(button.color+(255,))
            self.window.blit(s, (button.x+element.x,button.y+element.y))
        #pygame.draw.rect(self.window, RED, (element.x,element.y,element.height,element.width), 0)
        info = [self.selected.name,
                "Mass: %.2E" % self.selected.mass,
                "Dist: %.2E" % (self.selected.position - self.universe.sun.position).magnitude()]
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
        
