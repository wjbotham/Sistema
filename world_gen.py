from universe import Universe
from body import Body
from random import random,randint
from math import pi
tau = 2*pi

def generate_system():
    u = Universe()
    sun = Body("The Sun",pow(10,29+random()*2))
    u.add_body(sun)
    for i in range(5 + randint(0,4) + randint(0,4)):
        add_object(sun)
    u.bodies.sort(key=lambda obj:obj.get_distance(sun))
    return u

def add_object(parent):
    r1 = random()*2
    mass = pow(10,16 + (r1+random())/3*11.5)
    sma = 7*pow(10,5 + (r1+random())/3*4)
    ecc = min([random() for i in range(40)])
    prog = random()*tau
    theta = min([random()/4 for i in range(50)])*tau
    phi = random()*tau
    reverse_orbit = (random() < 0.001)
    parent.add_satellite("SB"+str(len(parent.universe.bodies)),mass,sma,ecc,prog,theta,phi,reverse_orbit)

#def add_gas_giant(parent):
#def add_moon(parent):
