class UIElement:
    def __init__(self,interface,x,y,width,height,color):
        self.interface = interface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.buttons = []
        self.add_drag_button()

    def add_drag_button(self):
        def pick_up(event):
            if self.interface.grabbed_element == self:
                self.interface.grabbed_element = None
            else:
                mx,my = event.pos
                self.picked_up = self.x-mx,self.y-my
                self.interface.grabbed_element = self
        self.buttons.append(Button(self.width-17,5,12,12,pick_up,self.color))

    def contains(self,x,y):
        return self.x < x < (self.x + self.width) and self.y < y < (self.y + self.height)

    def handle_left_click(self,event):
        x,y = event.pos
        rel_x,rel_y = x-self.x,y-self.y
        for button in self.buttons:
            if button.x < rel_x < (button.x + button.width) and button.y < rel_y < (button.y + button.height):
                button.click(event)

class Button:
    def __init__(self,x,y,width,height,action,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.color = color

    def click(self,event):
        self.action(event)
