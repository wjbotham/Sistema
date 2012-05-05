from vector import Vector
from math import sqrt,cos,sin,acos,pi,atan2
from decimal import Decimal

class Body:
    def __init__(self,name,mass,position=Vector(),velocity=Vector(),universe=None):
        self.name = name
        self.universe = universe
        self.mass = Decimal(mass)
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

    def add_satellite(self,name,mass,orbit_radius,theta=0,phi=0,orbit_direction=0):
        mass = Decimal(mass)
        rel_pos = Vector(orbit_radius,0,0).rotate(theta,phi)
        position = self.position.add(rel_pos)
        stan_grav_param = self.universe.G * (self.mass + mass)
        rel_vel = Vector(0,cos(orbit_direction),sin(orbit_direction)).rotate(theta,phi).multiply(sqrt(stan_grav_param / orbit_radius))
        velocity = self.velocity.add(rel_vel)
        self.universe.add_body(Body(name,mass,position,velocity))

    '''
        progression: the satellite's current progression around the ellipse
            0 is at the positive semi-major axis, pi/2 is at the positive semi-minor axis
            pi is at the negative semi-major axis, 3*pi/2 is at the negative semi-minor axis
        theta: how far to rotate the entire ellipse within its 2D plane, around the z-axis; this changes the location of the axes
        phi: how far to rotate the ellipse up into the third dimension
        orbit_direction: how much to rotate the satellite's current velocity direction
    '''
    def add_satellite_elliptic(self,name,mass,semimajor_axis,eccentricity=0,progression=0,theta=0,phi=0,orbit_direction=0):
        mass = Decimal(mass)
        semimajor_axis = Decimal(semimajor_axis)
        semiminor_axis = semimajor_axis * Decimal(sqrt(1-eccentricity**2))
        
        #calculate position in ellipse
        d_focus_to_center = (semimajor_axis**2 - semiminor_axis**2).sqrt()
        x = Decimal(cos(progression))*semimajor_axis + d_focus_to_center
        y = Decimal(sin(progression))*semiminor_axis
        rel_pos = Vector(y,x,0).rotate(theta,phi)
        position = self.position.add(rel_pos)

        # calculate orbit speed
        stan_grav_param = self.universe.G * (self.mass + mass)
        rel_vel_magnitude = sqrt(stan_grav_param * (2/rel_pos.magnitude() - 1/semimajor_axis))

        # calculate orbit direction
        dx = -Decimal(sin(progression))*semimajor_axis
        dy = Decimal(cos(progression))*semiminor_axis
        rel_vel_direction = Vector(dy,dx,0).normalize().rotate(theta,phi)
        
        rel_vel = rel_vel_direction.multiply(rel_vel_magnitude)
        velocity = self.velocity.add(rel_vel)
        self.universe.add_body(Body(name,mass,position,velocity))

    def attraction(self,other):
        rel_pos = other.position.subtract(self.position)
        magnitude = (self.universe.G * self.mass * other.mass) / rel_pos.dot_product()
        unit_vector = rel_pos.normalize()
        return unit_vector.multiply(magnitude)

    def ellipse_acceleration(self,other,a,b,t):
        return Vector(-a*cos(t),-b*sin(t),0)

    def get_angle_phi(self,other):
        rel_pos = self.position.subtract(other.position)
        unit_vector = rel_pos.normalize()
        return acos(unit_vector.z/rel_pos.magnitude())/pi

    def get_angle_theta(self,other):
        unit_vector = self.position.subtract(other.position).normalize()
        return atan2(unit_vector.y,unit_vector.x)/pi

    def get_distance(self,other):
        return self.position.subtract(other.position).magnitude()
