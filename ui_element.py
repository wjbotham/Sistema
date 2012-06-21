class UIElement:
    def __init__(self,interface,x,y,width,height,color):
        self.interface = interface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.buttons = []
        self.add_drag_bar()

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
