class UIElement:
    def __init__(self,interface,x,y,width,height,color,header,parent=None):
        self.interface = interface
        self._x = x
        self._y = y
        self.width = width
        self.height = height
        self.color = color
        self._header = header
        self.buttons = []
        self.add_drag_bar()
        self.parent = parent

    def get_x(self):
        if self.parent:
            return self._x + self.parent.x
        return self._x
    def set_x(self,x):
        if self.parent:
            self._x = x + self.parent.x
        else:
            self._x = x
    x = property(get_x,set_x)
    
    def get_y(self):
        if self.parent:
            return self._y + self.parent.y
        return self._y
    def set_y(self,y):
        if self.parent:
            self._y = y + self.parent.y
        else:
            self._y = y
    y = property(get_y,set_y)

    def add_drag_bar(self):
        def pick_up(event):
            mx,my = event.pos
            self.picked_up = self.x-mx,self.y-my
            self.interface.grabbed_element = self
        self.buttons.append(Button(0,0,self.width,11,lambda event:None,pick_up,self.color))

    def contains(self,x,y):
        return self.x < x < (self.x + self.width) and self.y < y < (self.y + self.height)

    def handle_left_mouse_up(self,event):
        x,y = event.pos
        rel_x,rel_y = x-self.x,y-self.y
        for button in self.buttons:
            if button.x < rel_x < (button.x + button.width) and button.y < rel_y < (button.y + button.height):
                button.left_mouse_up(event)

    def handle_left_mouse_down(self,event):
        x,y = event.pos
        rel_x,rel_y = x-self.x,y-self.y
        for button in self.buttons:
            if button.x < rel_x < (button.x + button.width) and button.y < rel_y < (button.y + button.height):
                button.left_mouse_down(event)

    def get_header(self,*args):
        if hasattr(self._header,'__call__'):
            return self._header(*args)
        return self._header
    header = property(get_header)

class Button:
    def __init__(self,x,y,width,height,left_mouse_up_action,left_mouse_down_action,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_mouse_down_action = left_mouse_down_action
        self.left_mouse_up_action = left_mouse_up_action
        self.color = color

    def left_mouse_up(self,event):
        self.left_mouse_up_action(event)

    def left_mouse_down(self,event):
        self.left_mouse_down_action(event)
