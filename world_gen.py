from universe import Universe
from body import Body
from random import Random
from math import pi,log
tau = 2*pi

# TODO
# Perhaps there should be a class that instantiates
# the RNG itself.
rng = Random()
def generate_system(seed=None):
    if seed:
        rng.seed(seed)
    u = Universe()
    sun = Body("The Sun",pow(10,29+rng.random()*2))
    u.add_body(sun)
    for i in range(1 + rng.randint(0,3) + rng.randint(0,3)):
        add_gas_giant(sun)
    for i in range(1 + rng.randint(0,3) + rng.randint(0,3)):
        add_rocky_planet(sun)
    u.bodies.sort(key=lambda obj:obj.distance(sun))
    return u

def add_gas_giant(parent):
    mass_range = (86,91)
    sma_range = (29,32.5)
    ecc_range = (-6.5,-2)
    theta_range = (-6,-5.5)
    color = (255,255,0)
    add_object(parent,"GG",mass_range,sma_range,ecc_range,theta_range,color)
    idx = len(parent.universe.bodies)-1
    for i in range(randint(1,6)):
        add_moon(parent.universe.bodies[idx])
    
def add_rocky_planet(parent):
    mass_range = (78,83)
    sma_range = (26,29)
    ecc_range = (-6.5,-2)
    theta_range = (-7,-5)
    color = (255,0,0)
    add_object(parent,"RP",mass_range,sma_range,ecc_range,theta_range,color)
    idx = len(parent.universe.bodies)-1
    for i in range(randint(0,1)):
        add_moon(parent.universe.bodies[idx])

#def add_dwarf_planet(parent):
    
def add_moon(parent):
    mass_range = (65,76)
    sma_range = (18,19)
    ecc_range = (-6.5,-2)
    theta_range = (-7,-5)
    color = (255,255,255)
    add_object(parent,"MN",mass_range,sma_range,ecc_range,theta_range,color)

def exprange(r):
    a,b = r
    return pow(2,rng.uniform(a,b))

def add_object(parent,prefix,mass_range,sma_range,ecc_range,theta_range,color,reverse_odds=0.002):
    mass = exprange(mass_range)
    sma = exprange(sma_range)
    ecc = exprange(ecc_range)
    prog = rng.random()*tau
    theta = exprange(theta_range)*tau
    phi = rng.random()*tau
    incl_angle = rng.random()*tau
    reverse_orbit = (rng.random() < reverse_odds)
    index = list(map(lambda b: b.name[:2], parent.universe.bodies)).count(prefix)+1
    parent.add_satellite("%s%d"%(prefix,index),mass,color,sma,ecc,prog,theta,phi,incl_angle,reverse_orbit)
    
