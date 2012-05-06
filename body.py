from vector import Vector
from math import sqrt,cos,sin,acos,pi,atan2

class Body:
    def __init__(self,name,mass,position=Vector(),velocity=Vector(),universe=None):
        self.name = name
        self.universe = universe
        self.mass = mass
        self.position = position
        self.velocity = velocity

    def apply_velocity(self):
        self.position = self.position.add(self.velocity)

    def apply_gravity(self):
        gravity_sum = Vector()
        for other in self.universe.bodies:
            if other != self:
                gravity_sum = gravity_sum.add(self.attraction(other))
        self.velocity = self.velocity.add(gravity_sum.divide(self.mass))
        
    '''
    progression: the satellite's current progression around the ellipse
        0 is at the positive semi-major axis, pi/2 is at the positive semi-minor axis
        pi is at the negative semi-major axis, 3*pi/2 is at the negative semi-minor axis
    theta: azimuthal rotation of orbit ("up" or "down", so to speak)
    phi: rotation of orbit around z-axis ("left" or "right")
    '''
    def add_satellite(self,name,mass,semimajor_axis,eccentricity=0,progression=0,theta=0,phi=0,reverse_orbit=False):
        semiminor_axis = semimajor_axis * sqrt(1-eccentricity**2)
        
        # calculate position in ellipse
        d_focus_to_center = sqrt(semimajor_axis**2 - semiminor_axis**2)
        x = cos(progression)*semimajor_axis + d_focus_to_center
        y = sin(progression)*semiminor_axis
        rel_pos = Vector(y,x,0).rotate(theta,phi)
        position = self.position.add(rel_pos)

        # calculate orbit speed
        stan_grav_param = self.universe.G * (self.mass + mass)
        rel_vel_magnitude = sqrt(stan_grav_param * (2/rel_pos.magnitude() - 1/semimajor_axis))

        # calculate orbit direction
        dx = -sin(progression)*semimajor_axis
        dy = cos(progression)*semiminor_axis
        rel_vel_direction = Vector(dy,dx,0).normalize().rotate(theta,phi)
        if reverse_orbit:
            rel_vel_direction = rel_vel_direction.neg()
        
        rel_vel = rel_vel_direction.multiply(rel_vel_magnitude)
        velocity = self.velocity.add(rel_vel)
        self.universe.add_body(Body(name,mass,position,velocity))

    def attraction(self,other):
        rel_pos = other.position.subtract(self.position)
        magnitude = (self.universe.G * self.mass * other.mass) / rel_pos.dot_product()
        unit_vector = rel_pos.normalize()
        return unit_vector.multiply(magnitude)

    def get_angle_phi(self,other):
        rel_pos = self.position.subtract(other.position)
        unit_vector = rel_pos.normalize()
        return acos(unit_vector.z/rel_pos.magnitude())/pi

    def get_angle_theta(self,other):
        unit_vector = self.position.subtract(other.position).normalize()
        return atan2(unit_vector.y,unit_vector.x)/pi

    def get_distance(self,other):
        return self.position.subtract(other.position).magnitude()
