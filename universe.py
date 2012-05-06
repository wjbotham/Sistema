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

    def pass_hour(self):
        self.time += 1
        for body in self.bodies:
            body.apply_velocity()
        for body in self.bodies:
            body.apply_gravity()

    def travel_time(self,b1,b2,accel):
        velocity_diff = b1.velocity.subtract(b2.velocity).magnitude()
        distance = b1.position.subtract(b2.position).magnitude()
        return ceil((velocity_diff/accel)+(distance/sqrt(accel*distance/4)))

    def report(self):
        plural = "s"
        if self.time == 1:
            plural = ""
        print("time = "+str(self.time)+" hour"+plural)
        for i in range(len(self.bodies)):
            bodyi = self.bodies[i]
            #print(bodyi.name+": pos=("+('%.2E' % bodyi.position.x)+","+('%.2E' % bodyi.position.y)+","+('%.2E' % bodyi.position.z)+"), vel=("+('%.2E' % bodyi.velocity.x)+","+('%.2E' % bodyi.velocity.y)+","+('%.2E' % bodyi.velocity.z)+")")
            for j in range(i+1,len(self.bodies)):
                bodyj = self.bodies[j]
                rel_pos = bodyi.position.subtract(bodyj.position)
                unit_vector = rel_pos.normalize()
                print(bodyi.name+" <=> "+bodyj.name+": distance="+('%.2E' % bodyi.get_distance(bodyj))+", theta="+str(bodyi.get_angle_theta(bodyj))+", phi="+str(bodyi.get_angle_phi(bodyj))+", travel time at 500 km/s^2 = "+str(self.travel_time(bodyi,bodyj,500*60*60))+", travel time at 50 km/s^2 = "+str(self.travel_time(bodyi,bodyj,50*60*60)))
        print()
