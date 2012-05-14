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
        self.position += self.velocity

    def apply_gravity(self):
        gravity_sum = sum(self.attraction(other) for other in self.universe.bodies if other != self)
        self.velocity += gravity_sum / self.mass
         
    '''
    progression: the satellite's current progression around the ellipse
        0 is at the positive semi-major axis, pi/2 is at the positive semi-minor axis
        pi is at the negative semi-major axis, 3*pi/2 is at the negative semi-minor axis
    theta: azimuthal rotation of orbit ("up" or "down", so to speak)
    phi: rotation of orbit around z-axis ("left" or "right")
    incl_angle: angle at which to perform azimuthal rotation
        basically http://en.wikipedia.org/wiki/Longitude_of_the_ascending_node
    reverse_orbit: 
    '''
    def add_satellite(self,name,mass,semimajor_axis,eccentricity,progression,theta,phi,incl_angle,reverse_orbit=False):
        semiminor_axis = semimajor_axis * sqrt(1-eccentricity**2)
        
        # calculate position in ellipse
        d_focus_to_center = sqrt(semimajor_axis**2 - semiminor_axis**2)
        x = cos(progression)*semimajor_axis + d_focus_to_center
        y = sin(progression)*semiminor_axis
        rel_pos = Vector(y,x,0).rotated(0,incl_angle).rotated(theta,phi-incl_angle)
        position = self.position + rel_pos

        # calculate orbit speed
        stan_grav_param = self.universe.G * (self.mass + mass)
        rel_vel_magnitude = sqrt(stan_grav_param * (2/rel_pos.magnitude() - 1/semimajor_axis))

        # calculate orbit direction
        dx = -sin(progression)*semimajor_axis
        dy = cos(progression)*semiminor_axis
        rel_vel_direction = Vector(dy,dx,0).normalized().rotated(0,incl_angle).rotated(theta,phi-incl_angle)
        if reverse_orbit:
            rel_vel_direction = -rel_vel_direction
        
        rel_vel = rel_vel_direction * rel_vel_magnitude
        velocity = self.velocity + rel_vel
        self.universe.add_body(Body(name,mass,position,velocity))

    def attraction(self,other):
        rel_pos = other.position - self.position
        magnitude = (self.universe.G * self.mass * other.mass) / (rel_pos*rel_pos)
        unit_vector = rel_pos.normalized()
        return unit_vector * magnitude

    def angle_phi(self,other):
        rel_pos = self.position - other.position
        unit_vector = rel_pos.normalized()
        return acos(unit_vector.z/rel_pos.magnitude())/pi

    def angle_theta(self,other):
        unit_vector = (self.position - other.position).normalized()
        return atan2(unit_vector.y,unit_vector.x)/pi

    def distance(self,other):
        return (self.position - other.position).magnitude()
