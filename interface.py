import pygame
from vector import Vector
from math import sqrt
from ui_element import ObjectInfoBox
from style import *
from time import clock
from threading import Thread

class Interface:
    def __init__(self,universe,width=1000,height=800):
        pygame.init()
        
        self.universe = universe
        self._selected = max(self.universe.bodies, key=lambda b: b.mass)
        
        #create the screen
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self._origin = self.universe.center_of_mass
        self._km_per_pixel = max((body.position - self.origin).magnitude() for body in self.universe.bodies)*1.25/min(height,width)

        self.ui_elements = [ObjectInfoBox(self,100,100)]
        self.grabbed_element = None

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
    km_per_pixel = property(get_km_per_pixel,set_km_per_pixel)

    def get_aspect_ratio(self):
        return self.height / self.width
    aspect_ratio = property(get_aspect_ratio)

    def get_width(self):
        return self.window.get_size()[0]
    width = property(get_width)

    def get_height(self):
        return self.window.get_size()[1]
    height = property(get_height)

    def get_selected(self):
        return self._selected
    def set_selected(self,selected):
        self._selected = selected
    selected = property(get_selected,set_selected)

    def get_fps(self):
        return 1/self._seconds_per_frame
    def set_fps(self, fps):
        self._seconds_per_frame = 1/fps
    fps = property(get_fps, set_fps)

    def get_top_element(self):
        return self.ui_elements[0]
    def set_top_element(self,element):
        self.ui_elements.remove(element)
        self.ui_elements.insert(0,element)
    top_element = property(get_top_element,set_top_element)

    def graphics_update_loop(self):
        self.fps = 30
        next_update = clock() + self._seconds_per_frame
        while True:
            while clock() < next_update:
                pass
            self.update()
            next_update += self._seconds_per_frame

    def ui_loop(self):
        gu_t = Thread(target=self.graphics_update_loop)
        gu_t.start()
        while True:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    self.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_down(event)
                elif event.type == pygame.MOUSEMOTION:
                    if self.grabbed_element:
                        dx,dy = event.rel
                        self.grabbed_element.abs_x += dx
                        self.grabbed_element.abs_y += dy
                elif event.type == pygame.VIDEORESIZE:
                    self.resize(event.size)
                    # TODO Move floaty windows so they don't get lost outside of the display area
                    # TODO Figure out how to avoid the ugly streaking when resized larger
                else:
                    print(event)

    def resize(self,size):
        if size[0] < 300:
            size = (300,size[1])
        if size[1] < 300:
            size = (size[0],300)
        for e in self.ui_elements:
            e.abs_x *= size[0]/self.width
            e.abs_y *= size[1]/self.height
        self.window = pygame.display.set_mode(size, pygame.RESIZABLE)
        
    def handle_click(self,event):
        # if left mouse release, release a grabbed element
        if self.grabbed_element and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.grabbed_element = None
        for e in self.ui_elements:
            if e.attempt_handle(event):
                return
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_left_mouse_up(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_left_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.handle_right_mouse_up(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.zoomIn()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.zoomOut()

    def handle_key_down(self,event):
        if event.unicode == 'p' or event.unicode == 'P':
            self.universe.paused = not self.universe.paused
        elif event.unicode == '[':
            self.zoomOut()
        elif event.unicode == ']':
            self.zoomIn()
        elif event.unicode == '1':
            self.universe.seconds_per_turn = 360
        elif event.unicode == '2':
            self.universe.seconds_per_turn = 10
        elif event.unicode == '3':
            self.universe.seconds_per_turn = 1
        elif event.unicode == '4':
            self.universe.seconds_per_turn = 0.5
        elif event.unicode == '5':
            self.universe.seconds_per_turn = 0.2
        elif event.unicode == '6':
            self.universe.seconds_per_turn = 0.1
        elif event.unicode == '7':
            self.universe.seconds_per_turn = 0.05
        elif event.unicode == '8':
            self.universe.seconds_per_turn = 0.025
        elif event.unicode == '9':
            self.universe.seconds_per_turn = 0.0125

    def handle_left_mouse_up(self,event):
        self.grabbed_element = None
        # find a body near the click event and select it
        subject = self.find_subject_body(event)
        if subject:
            self.selected = subject

    def handle_left_mouse_down(self,event):
        None

    def handle_right_mouse_up(self,event):
        subject = self.find_subject_body(event)
        if subject:
            if self.selected:
                print("%.2E" % subject.distance(self.selected))
                
    def zoomIn(self):
        # this filter is here so we don't magnify to the point where it breaks,
        # so fix that bug and then remove this TODO
        if self.km_per_pixel / 1.75 > 2:
            self.km_per_pixel /= 1.75

    def zoomOut(self):
        self.km_per_pixel *= 1.75

    def pixel_radius(self,body):
        return max(2,round(body.radius / self.km_per_pixel))

    def find_subject_body(self,event):
        ev_x,ev_y = event.pos
        candidates = []
        for body in self.universe.bodies:
            b_x,b_y = self.km_to_px(body.position.x,
                                    body.position.y)
            dist = sqrt((ev_x-b_x)**2 + (ev_y-b_y)**2)
            if dist <= 10 + self.pixel_radius(body):
                candidates.append(body)                    
        if len(candidates) > 0:
            return max(candidates,key=lambda body: body.mass)
        else:
            return None

    def km_to_px(self,x,y):
        ox,oy = self.origin.x,self.origin.y
        nx = round(((x-ox) / self.km_per_pixel) + (self.width  / 2))
        ny = round(((y-oy) / self.km_per_pixel) + (self.height / 2))
        return (nx,ny)
    
    def px_to_km(self,x,y):
        ox,oy = self.origin.x,self.origin.y
        nx = ((x - (self.width  / 2)) * self.km_per_pixel) + ox
        ny = ((y - (self.height / 2)) * self.km_per_pixel) + oy
        return (nx,ny)

    def update(self):
        if self.selected:
            x = self.selected.position.x
            y = self.selected.position.y
            self.origin = Vector(x,y,0)
        else:
            self.origin = self.universe.center_of_mass
        self.window.fill(BLACK)
        time_flow = 360/self.universe.seconds_per_turn
        if self.universe.paused:
            pause_status = "Paused"
        else:
            pause_status = "Running"
        time_info = "%dx (%s)" % (time_flow, pause_status)
        self.draw_text(["%.2E" % self.km_per_pixel,
                        "T+%.3f hours" % ((self.universe.time + 1-self.universe.turn_left)/10),
                        "%d future turns cached" % (self.universe.last_cached_turn - self.universe.time),
                        "%d total turns cached" % len(self.universe.physics_locks.keys()),
                        time_info], 1, 1, LIGHT_GRAY, BLACK)
        for body in sorted(self.universe.bodies,key=lambda b: b.mass):
            self.draw_body(body)
        for element in reversed(self.ui_elements):
            self.draw_element(element)
        # draw it to the screen
        # TODO: implement some way of tracking changes, then translate
        #       this to use pygame.display.update(rectangles)
        pygame.display.flip()

    def draw_body(self,body):
        pos = self.km_to_px(body.position.x,
                            body.position.y)
        pixel_radius = self.pixel_radius(body)
        visible_x = (-pixel_radius <= pos[0] <= self.width  + pixel_radius)
        visible_y = (-pixel_radius <= pos[1] <= self.height + pixel_radius)
        if not (visible_x and visible_y):
            return
        pygame.draw.circle(self.window, body.color, pos, pixel_radius, 0)
        text = FONT.render(body.name, True, LIGHT_GRAY, BLACK)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = pos
        textRect.centery += 6 + pixel_radius
        self.window.blit(text, textRect)

    def draw_element(self,element):
        self.window.blit(element.surface(), (element.abs_x,element.abs_y))
        for child in element.children:
            self.draw_element(child)

    def draw_text(self,text_ary,x,y,text_color,background_color=None,alpha=255):
        assert(text_ary.__class__ == list)
        line = text_ary[0]

        w,h = FONT.size(line)
        if background_color:
            text = FONT.render(line, True, text_color, background_color)
        else:
            text = FONT.render(line, True, text_color)
        text.set_alpha(alpha)
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = x+w/2,y+h/2

        if len(text_ary) > 1:
            self.draw_text(text_ary[1:], x, y+h, text_color, background_color, alpha)
        self.window.blit(text, textRect)
        
