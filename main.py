import sys
sys.path.append("C:\\Users\\wajib\\Desktop\\Solar\\")
from vector import Vector
from universe import Universe
from body import Body
from random import random
import math
tau = 2*math.pi

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''

def add_random_planet(parent):
    mass = 1E+23 + random()*1E+25
    # sma = semi-major axis
    sma = 5E+7 + min([random() for i in range(5)])*5E+8
    # ecc = eccentricity
    ecc = min([random() for i in range(40)])
    # prog = progression
    prog = random()*tau
    theta = min([random()/4 for i in range(50)])*tau
    phi = random()*tau
    reverse_orbit = (random() < 0.001)
    parent.add_satellite("Test "+str(len(parent.universe.bodies)),mass,sma,ecc,prog,theta,phi,reverse_orbit)
    
def main():
    u = Universe()
    sol = Body("Sol",5E29+random()*5E30)
    u.add_body(sol)

    for i in range(3):
        add_random_planet(sol)

    '''
    mass = 4.8685E24
    semimajor_axis = 108942109
    eccentricity = 0.0068
    u.bodies[0].add_satellite("Venus",
                              mass,
                              semimajor_axis,
                              eccentricity,
                              2*tau/3,3*tau/8,3*tau/8,True)
    
    sol = Body("Sol",1.9891E30)
    jupiter = Body("Jupiter",1.8986E27,Vector(778547200,0,0),Vector(0,13.07*3600,0),sol)
    earth = Body("Earth",5.9736E24,Vector(149598261,0,0),Vector(0,29.78*3600,0),sol)
    #luna = Body("Luna",7.3477E22,Vector(384399,0,0),Vector(0,0,1.022*60*60),earth)
    mars = Body("Mars",6.4185E23,Vector(227939100,0,0),Vector(0,24.077*3600,0),sol)
    venus = Body("Venus",4.8685E24,Vector(108208930,0,0),Vector(0,35.02*3600,0),sol)
    io = Body("Io",8.9319E22,Vector(421700,0,0),Vector(0,17.334*3600,0),jupiter)
    europa = Body("Europa",4.8E22,Vector(670900,0,0),Vector(0,13.74*3600,0),jupiter)
    ganymede = Body("Ganymede",1.4819E23,Vector(1070400,0,0),Vector(0,10.88*3600,0),jupiter)
    callisto = Body("Callisto",1.075938E23,Vector(1882700,0,0),Vector(0,8.204*3600,0),jupiter)
    system = [sol,jupiter,earth,mars,venus,io,europa,ganymede,callisto]
    for body in system:
        u.add_body(body)'''
    distances = []
    u.report()
    for i in range(10000):
        u.pass_hour()
        if i%1000 == 999:
            u.report()

if __name__ == "__main__":
    main()
