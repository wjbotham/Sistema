class UIElement:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self,x,y):
        return self.x < x < (self.x + self.width) and self.y < y < (self.y + self.height)

    def handle_left_click(self,event):
        print(event)
