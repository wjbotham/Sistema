from core.vector import Vector
from math import sqrt,cos,sin,acos,pi,atan2,ceil

class Body:
    def __init__(self,name,mass,density,color=(255,255,255),position=None,velocity=None,universe=None):
        if position is None:
            position = Vector()
        if velocity is None:
            velocity = Vector()
        self.name = name
        self.universe = universe
        self.universe.bodies.append(self)
        self.mass = mass
        self.radius = (3*mass/4/pi/density)**(1/3)
        self.universe.physics_cache.init_body(self, position, velocity)
        self.color = color
        self._primary = None
        # TODO: make adding/removing satellites (and therefore changing the system mass) happen in property methods
        self.satellites = []
        self._system_mass = mass
        self.regions = []

    def get_primary(self):
        return self._primary
    def set_primary(self, primary):
        # remove self from old primary's satellites
        if (self._primary):
            self._primary.satellites.remove(self)
            self._primary.system_mass -= self.system_mass
        # change primary
        self._primary = primary
        # add self to new primary's satellites
        if self._primary:
            self._primary.satellites.append(self)
            self._primary.system_mass += self.system_mass
    primary = property(get_primary, set_primary)

    '''
    the center of mass of the system consisting of this body and all its
    satellites/subsatellites/etc.
    '''
    def get_center_of_mass(self, turn):
        if not self.universe.physics_cache.has(turn):
            self.universe.calculate_physics(turn)
        com = self.universe.physics_cache.fetch_center_of_mass(self, turn)
        if (com == None):
            sat_part = sum(sat.get_center_of_mass(turn) * sat.system_mass for sat in self.satellites)
            own_part = self.get_position(turn) * self.mass
            com = (sat_part + own_part) / self.system_mass
            self.universe.physics_cache.set_center_of_mass(self, turn, com)
        return com
    center_of_mass = property(lambda self: self.get_center_of_mass(self.universe.time))

    def get_system_mass(self):
        return self._system_mass
    def set_system_mass(self, system_mass):
        change_in_mass = system_mass - self.system_mass
        self._system_mass = system_mass
        if self.primary:
            self.primary.system_mass += change_in_mass
    system_mass = property(get_system_mass, set_system_mass)

    def get_velocity(self, turn):
        if not self.universe.physics_cache.has(turn):
            self.universe.calculate_physics(turn)
        return self.universe.physics_cache.fetch_velocity(self, turn)
    velocity = property(lambda self: self.get_velocity(self.universe.time))

    def get_position(self, turn):
        if not self.universe.physics_cache.has(turn):
            self.universe.calculate_physics(turn)
        return self.universe.physics_cache.fetch_position(self, turn)
    position = property(lambda self: self.get_position(self.universe.time))

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
    def add_satellite(self,name,mass,density,color,semimajor_axis,eccentricity,progression,theta,phi,incl_angle,reverse_orbit=False):
        semiminor_axis = semimajor_axis * sqrt(1-eccentricity**2)
        
        # calculate position in ellipse
        d_focus_to_center = sqrt(semimajor_axis**2 - semiminor_axis**2)
        x = cos(progression)*semimajor_axis + d_focus_to_center
        y = sin(progression)*semiminor_axis
        rel_pos = Vector(y,x,0).rotated(0,incl_angle).rotated(theta,phi-incl_angle)
        position = self.position + rel_pos

        # calculate orbit speed
        stan_grav_param = self.universe.G * (self.mass + mass)
        rel_vel_magnitude = sqrt(stan_grav_param * (2/rel_pos.magnitude -
                                                    1/semimajor_axis))

        # calculate orbit direction
        dx = -sin(progression)*semimajor_axis
        dy = cos(progression)*semiminor_axis
        rel_vel_direction = Vector(dy,dx,0).normalized.rotated(0,incl_angle).rotated(theta,phi-incl_angle)
        if reverse_orbit:
            rel_vel_direction = -rel_vel_direction
        
        rel_vel = rel_vel_direction * rel_vel_magnitude
        velocity = self.velocity + rel_vel
        return Body(name, mass, density, color, position, velocity, universe=self.universe)

    '''
    This return value needs to be multiplied by the gravitational constant. (I
    don't multiply it here because the attraction value can be summed up from
    many pairwise interactions and THEN multiplied so we can save on a few
    calculations.)

    This basically returns (acceleration divided by G).
    '''
    def attraction(self, other, turn):
        if self == other:
            return 0

        self_pos = self.get_position(turn)
        if self.primary == other or self.primary == other.primary:
            self_pos = self.get_center_of_mass(turn)

        other_mass = other.mass
        other_pos = other.get_position(turn)
        if self == other.primary or self.primary == other.primary:
            other_mass = other.system_mass
            other_pos = other.get_center_of_mass(turn)
        
        # I would refactor this to be easier to read, but it's the result of a
        # ton of time optimizations, so enjoy!
        rel_pos = other_pos.fast_sub(self_pos)
        distance_squared = rel_pos[0]**2 + rel_pos[1]**2 + rel_pos[2]**2
        scalar = (other_mass / distance_squared) / sqrt(distance_squared)
        return Vector(scalar * rel_pos[0], scalar * rel_pos[1], scalar * rel_pos[2])

    def angle_phi(self, other, turn):
        rel_pos = self.get_position(turn) - other.get_position(turn)
        unit_vector = rel_pos.normalized
        return acos(unit_vector.z/rel_pos.magnitude)/pi

    def angle_theta(self, other, turn):
        unit_vector = (self.get_position(turn) - other.get_position(turn)).normalized
        return atan2(unit_vector.y,unit_vector.x)/pi

    def distance(self, other, turn=None):
        if (turn is None):
            turn = self.universe.time
        return (self.get_position(turn) - other.get_position(turn)).magnitude

    def travel_time(self, other, accel):
        time_from_match = (self.get_velocity(self.universe.time) - other.get_velocity(self.universe.time)).magnitude / accel
        time_from_travel = (4 * self.distance(other) / accel) ** 0.5
        return ceil(time_from_match + time_from_travel)
