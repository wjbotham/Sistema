from universe import Universe
from body import Body
from random import random,uniform,randint
from math import pi,log
tau = 2*pi

def generate_system():
    u = Universe()
    sun = Body("The Sun",pow(10,29+random()*2))
    u.add_body(sun)
    for i in range(1 + randint(0,3) + randint(0,3)):
        add_gas_giant(sun)
    for i in range(1 + randint(0,3) + randint(0,3)):
        add_rocky_planet(sun)
    u.bodies.sort(key=lambda obj:obj.distance(sun))
    return u

def add_gas_giant(parent):
    mass_range = (86,91)
    sma_range = (29,32.5)
    ecc_range = (-6.5,-2)
    theta_range = (-6,-5.5)
    add_object(parent,"GG",mass_range,sma_range,ecc_range,theta_range)
    idx = len(parent.universe.bodies)-1
    for i in range(randint(1,6)):
        add_moon(parent.universe.bodies[idx])
    
def add_rocky_planet(parent):
    mass_range = (78,83)
    sma_range = (26,29)
    ecc_range = (-6.5,-2)
    theta_range = (-7,-5)
    add_object(parent,"RP",mass_range,sma_range,ecc_range,theta_range)
    idx = len(parent.universe.bodies)-1
    for i in range(randint(0,1)):
        add_moon(parent.universe.bodies[idx])

#def add_dwarf_planet(parent):
    
def add_moon(parent):
    mass_range = (65,76)
    sma_range = (18,19)
    ecc_range = (-6.5,-2)
    theta_range = (-7,-5)
    add_object(parent,"MN",mass_range,sma_range,ecc_range,theta_range)

def exprange(r):
    a,b = r
    return pow(2,uniform(a,b))

def add_object(parent,prefix,mass_range,sma_range,ecc_range,theta_range,reverse_odds=0.002):
    mass = exprange(mass_range)
    sma = exprange(sma_range)
    ecc = exprange(ecc_range)
    prog = random()*tau
    theta = exprange(theta_range)*tau
    phi = random()*tau
    incl_angle = random()*tau
    reverse_orbit = (random() < reverse_odds)
    index = list(map(lambda b: b.name[:2], parent.universe.bodies)).count(prefix)+1
    parent.add_satellite("%s%d"%(prefix,index),mass,sma,ecc,prog,theta,phi,incl_angle,reverse_orbit)
    
