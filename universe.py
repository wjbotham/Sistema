from math import ceil,sqrt
from view import View
from threading import Thread
from vector import Vector
from time import clock

class Universe:
    def __init__(self,paused=True,G = 8.6493e-13):
        self.bodies = []
        self.time = 0
        # gravitational constant is in kilometers cubed per kilogram per hour squared
        self.G = G
        self.view = None
        self.paused = paused

    def add_body(self,body):
        body.universe = self
        self.bodies.append(body)

    def pass_hour(self,hours=1):
        for i in range(hours):
            self.time += 1
            for body in self.bodies:
                body.apply_velocity()
            for body in self.bodies:
                body.apply_gravity()
        if self.view:
            self.view.update()

    def center_of_mass(self):
        total_mass = sum(body.mass for body in self.bodies)
        if total_mass == 0:
            return Vector(0,0,0)
        return sum((body.position * body.mass) for body in self.bodies)/total_mass

    def travel_time(self,b1,b2,accel):
        velocity_diff = (b1.velocity - b2.velocity).magnitude()
        distance = (b1.position - b2.position).magnitude()
        return ceil((velocity_diff/accel)+(distance/sqrt(accel*distance/4)))

    def ui_loop(self):
        self.view = View(self)
        self.view.ui_loop()

    def describe_system(self):
        plural = "s"
        if self.time == 1:
            plural = ""
        print("time = "+str(self.time)+" hour"+plural)
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
        next_tick = clock()+1
        while self.view:
            while clock() < next_tick:
                if self.paused:
                    time_left = next_tick - clock()
                    while self.paused:
                        pass
                    next_tick = clock() + time_left
                pass
            self.pass_hour(1)
            next_tick += 1
