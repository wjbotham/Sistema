from math import ceil,sqrt

class Universe:
    def __init__(self,G = 8.6493e-13):
        self.bodies = []
        self.time = 0
        # gravitational constant is in kilometers cubed per kilogram per hour squared
        self.G = G

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

    def travel_time(self,b1,b2,accel):
        velocity_diff = (b1.velocity - b2.velocity).magnitude()
        distance = (b1.position - b2.position).magnitude()
        return ceil((velocity_diff/accel)+(distance/sqrt(accel*distance/4)))

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
