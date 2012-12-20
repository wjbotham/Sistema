from universe import Universe
from body import Body
from random import Random
from math import pi,log
tau = 2*pi

# TODO
# Perhaps there should be a class that instantiates
# the RNG itself.
#
# Perhaps the RNG should belong to the Universe object
# so that procedural generation of events throughout
# the game can be replicated.
#
# Perhaps all these methods could be folded into the
# Universe object.
class WorldGenerator:
    def __init__(self,seed=None):
        self.system_generated = False
        self.rng = Random()
        if seed:
            self.rng.seed(seed)

    def generate_development(self):
        # don't call this before we're done generating
        # a system or the seed won't make the same world
        assert(self.system_generated)
        result = None
        if self.rng.random() <= 0.01:
            result = self.rng.randint(1,1000000)
        return result
        
    def generate_system(self):
        u = Universe(self)
        sun = Body("The Sun", pow(10, 29+self.rng.random()*2),
                   pow(10, 11.9+self.rng.random()*0.2), universe=u)
        u.sun = sun
        for i in range(1 + self.rng.randint(0,4) + self.rng.randint(0,4)):
            self.add_gas_giant(sun)
        for i in range(1 + self.rng.randint(0,4) + self.rng.randint(0,4)):
            self.add_rocky_planet(sun)
        u.bodies.sort(key=lambda obj:obj.distance(sun))
        self.system_generated = True
        return u

    def add_gas_giant(self,parent):
        mass_range = (86,91)
        density_range = (39,41)
        sma_range = (29,32.5)
        ecc_range = (-6.5,-2)
        theta_range = (-6,-5.5)
        color = (255,255,0)
        self.add_object(parent,"GG",mass_range,density_range,sma_range,ecc_range,theta_range,color)
        idx = len(parent.universe.bodies)-1
        for i in range(self.rng.randint(1,6)):
            self.add_moon(parent.universe.bodies[idx])
        
    def add_rocky_planet(self,parent):
        mass_range = (78,83)
        density_range = (42.5,43.4)
        sma_range = (26,29)
        ecc_range = (-6.5,-2)
        theta_range = (-7,-5)
        color = (255,0,0)
        self.add_object(parent,"RP",mass_range,density_range,sma_range,ecc_range,theta_range,color)
        idx = len(parent.universe.bodies)-1
        for i in range(self.rng.randint(0,1)):
            self.add_moon(parent.universe.bodies[idx])

    #def add_dwarf_planet(self,parent):
        
    def add_moon(self,parent):
        mass_range = (65,76)
        density_range = (42.4,42.9)
        sma_range = (18,19)
        ecc_range = (-6.5,-2)
        theta_range = (-7,-5)
        color = (255,255,255)
        self.add_object(parent,"MN",mass_range,density_range,sma_range,ecc_range,theta_range,color)

    def exprange(self,r):
        a,b = r
        return pow(2,self.rng.uniform(a,b))

    def add_object(self,parent,prefix,mass_range,density_range,sma_range,ecc_range,theta_range,color,reverse_odds=0.002):
        mass = self.exprange(mass_range)
        density = self.exprange(density_range)
        sma = self.exprange(sma_range)
        ecc = self.exprange(ecc_range)
        prog = self.rng.random()*tau
        theta = self.exprange(theta_range)*tau
        phi = self.rng.random()*tau
        incl_angle = self.rng.random()*tau
        reverse_orbit = (self.rng.random() < reverse_odds)
        index = list(map(lambda b: b.name[:2], parent.universe.bodies)).count(prefix)+1
        parent.add_satellite("%s%d"%(prefix,index),mass,density,color,sma,ecc,prog,theta,phi,incl_angle,reverse_orbit)
        
