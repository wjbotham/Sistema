from math import ceil,sqrt
from interface import Interface
from threading import Thread
from vector import Vector
from time import clock

class Universe:
    def __init__(self,generator,paused=True,G = 8.648208e-15):
        self.bodies = []
        self.time = 0
        # gravitational constant is in kilometers cubed per kilogram per turn squared
        # 1 turn = 6 minutes
        self.G = G
        self.view = None
        self.paused = paused
        self.generator = generator
        self.sun = None

    def pass_turn(self):
        print(self.time)
        self.time += 1
        dev = self.generator.generate_development()
        if dev:
            print("Development: %d at t=%d" % (dev,self.time))
        if self.view:
            self.view.update()

    def center_of_mass(self):
        total_mass = sum(body.mass for body in self.bodies)
        if total_mass == 0:
            return Vector(0,0,0)
        return sum((body.get_position(self.time) * body.mass) for body in self.bodies)/total_mass

    def travel_time(self,b1,b2,accel):
        velocity_diff = (b1.velocity - b2.velocity).magnitude()
        distance = (b1.position - b2.position).magnitude()
        return ceil((velocity_diff/accel)+(distance/sqrt(accel*distance/4)))

    def ui_loop(self):
        self.view = Interface(self)
        self.view.ui_loop()

    def describe_system(self):
        plural = "s"
        if self.time == 1:
            plural = ""
        print("time = "+str(self.time)+" turn"+plural)
        sun = self.bodies[0]
        print(sun.name+": mass="+('%.2E' % sun.mass))
        for i in range(1,len(self.bodies)):
            bodyi = self.bodies[i]
            dist = (self.bodies[0].position - bodyi.position).magnitude()
            orbit_speed = (self.bodies[0].velocity - bodyi.velocity).magnitude()
            print(bodyi.name+": dist=("+('%.2E' % dist)+"), orbit speed=("+('%.2E' % orbit_speed)+"), mass="+('%.2E' % bodyi.mass))
        print()

    def run(self):
        t = Thread(target=self.ui_loop)
        t.start()
        while not self.view:
            pass
        seconds_per_turn = 1
        next_turn = clock() + seconds_per_turn
        while self.view:
            while clock() < next_turn:
                if self.paused:
                    time_left = next_turn - clock()
                    while self.paused:
                        pass
                    next_turn = clock() + time_left
                pass
            self.pass_turn()
            next_turn += seconds_per_turn
