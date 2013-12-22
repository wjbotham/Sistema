class Kinematic:
    def __init__(self, position, velocity, sat_accel=0):
        self.position = position
        self.velocity = velocity
        self.sat_accel = sat_accel

    def accelerate(self, acceleration):
        self.velocity += acceleration
