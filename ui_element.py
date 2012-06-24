import pygame
from style import *

class UIElement:
    def __init__(self,parent,x,y,width,height,background_color):
        self.parent = parent
        self.rel_x = x
        self.rel_y = y
        self.width = width
        self.height = height
        self.background_color = background_color
        self.children = []
        self.mousethru = False

    def attempt_handle(self,event):
        if self.mousethru:
            return False
        if self.contains(*event.pos):
            if self.interface() == self.parent:
                self.interface().top_element = self
            for c in self.children:
                if c.attempt_handle(event):
                    return True
            self.handle(event)
            return True
        else:
            return False

    def handle(self,event):
        None

    def interface(self):
        if not isinstance(self.parent,UIElement):
            return self.parent
        else:
            return self.parent.interface()
        
    def contains(self,x,y):
        return self.abs_x < x < (self.abs_x + self.width) and self.abs_y < y < (self.abs_y + self.height)
    def parent_is_ui_element(self):
        return isinstance(self.parent,UIElement)

    def get_abs_x(self):
        if self.parent_is_ui_element():
            return self.rel_x + self.parent.abs_x
        return self.rel_x
    def set_abs_x(self,x):
        if self.parent_is_ui_element():
            self.rel_x = x - self.parent.abs_x
        else:
            self.rel_x = x
    abs_x = property(get_abs_x,set_abs_x)
    
    def get_abs_y(self):
        if self.parent_is_ui_element():
            return self.rel_y + self.parent.abs_y
        return self.rel_y
    def set_abs_y(self,y):
        if self.parent_is_ui_element():
            self.rel_y = y - self.parent.abs_y
        else:
            self.rel_y = y
    abs_y = property(get_abs_y,set_abs_y)

    def get_x(self):
        assert("Stop using UIElement.x, it's too ambiguous"==None)
    x = property(get_x)

    def get_y(self):
        assert("Stop using UIElement.y, it's too ambiguous"==None)
    y = property(get_y)

    def surface(self):
        s = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        s.fill(self.background_color+(OPACITY,))
        return s

class ObjectInfoBox(UIElement):
    def __init__(self,parent,x,y,title="Object Info",border_width=1):
        UIElement.__init__(self,parent,x,y,150,100,DARK_GREEN)
        self.border_width = border_width
        header = Header(self,title)
        self.children.append(Header(self,title))
        #self.children.append(Button(self,25,25,60,15,DARK_GREEN,BLACK,"Test Button",lambda: print("Click!")))
        def body_info():
            s = self.interface().selected
            return ["Name: %s" % s.name,
                    "Mass: %.2E kg" % s.mass,
                    "Radius: %.2E km" % s.radius]
        self.children.append(Label(self,1,1+header.height,None,BLACK,body_info))

    def surface(self):
        s = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        s.fill(GREEN+(OPACITY,),(0,0,self.width,self.height))
        s.fill(self.background_color+(OPACITY,),(self.border_width,self.border_width,self.width-2*self.border_width,self.height-2*self.border_width))
        return s

class Header(UIElement):
    def __init__(self,parent,contents):
        UIElement.__init__(self,parent,0,0,parent.width,0,parent.background_color)
        label = Label(self,1,1,None,BLACK,contents)
        self.height = label.height+1
        self.children.append(label)

    def handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.interface().grabbed_element = self.parent
    
    def surface(self):
        s = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        s.fill(self.background_color+(OPACITY,),(self.parent.border_width,self.parent.border_width,self.width-2*self.parent.border_width,self.height))
        return s

class Button(UIElement):
    def __init__(self,parent,x,y,width,height,background_color,text_color,text,action):
        UIElement.__init__(self,parent,x,y,width,height,background_color)
        label = Label(self,0,0,None,text_color,text)
        label.rel_x = (self.width-label.width)/2
        label.rel_y = (self.height-label.height)/2
        self.children.append(label)
        self.action = action

    def handle(self,event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.action()

class Label(UIElement):
    def __init__(self,parent,x,y,background_color,text_color,text):
        self._text = text
        UIElement.__init__(self,parent,x,y,None,None,background_color)
        self.text_color = text_color
        self.mousethru = True

    def get_width(self):
        if isinstance(self.text,str):
            return FONT.size(self.text)[0]
        elif isinstance(self.text,list):
            return max(FONT.size(l)[0] for l in self.text)
    width = property(get_width,lambda self,width: None)

    def get_height(self):
        if isinstance(self.text,str):
            return FONT.size(self.text)[1]
        elif isinstance(self.text,list):
            return sum(FONT.size(l)[1] for l in self.text)
    height = property(get_height,lambda self,height: None)
    
    def get_text(self,*args):
        if hasattr(self._text,'__call__'):
            return self._text(*args)
        return self._text
    text = property(get_text)

    def surface(self):
        def str_to_canvas(text):
            if self.background_color:
                canvas = FONT.render(text, True, self.text_color, self.background_color)
            else:
                canvas = FONT.render(text, True, self.text_color)
            canvas.set_alpha(OPACITY)
            return canvas
        if isinstance(self.text,str):
            s = str_to_canvas(self.text)
        elif isinstance(self.text,list):
            s_ary = list(map(str_to_canvas,self.text))
            s = pygame.Surface((max(l.get_width() for l in s_ary),sum(l.get_height() for l in s_ary)), pygame.SRCALPHA)
            y = 0
            for l in s_ary:
                s.blit(l,(0,y))
                y = y + l.get_height()
        return s
