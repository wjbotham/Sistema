from tkinter import *

class CommandInterface:
    def __init__(self,universe):
        self.Tk = Tk()
        self.Tk.protocol("WM_DELETE_WINDOW", lambda: None)
        self.frame = Frame(self.Tk, width=128, height=128)
        self.frame.pack_propagate(1)
        self.frame.pack()
        
        def addLabel():
            a = Label(self.Tk, anchor=W)
            a.pack(fill=X)
            return a
        self.frame.body_name = addLabel()
        self.frame.body_mass = addLabel()

        self.universe = universe
        def toggle_timer():
            self.universe.paused = not self.universe.paused
        self.frame.timer_button = Button(self.Tk, text="Toggle Timer", command = toggle_timer)
        self.frame.timer_button.pack()

    def update_displayed_body(self,body):
        self.frame.body_mass.config(text="Mass: %.2E kg" % body.mass)
        self.frame.body_name.config(text="Name: "+body.name)

    def mainloop(self):
        self.Tk.mainloop()

    def quit(self):
        self.Tk.quit()
