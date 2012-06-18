from universe import Universe
from world_gen import generate_system
from agent import Agent

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''

def main():
    u = generate_system("Here is my sample system")
    a = Agent("UNSK5672",u.bodies[0])
    b = Agent("SDBJ3178",u.bodies[0])
    u.run()

if __name__ == "__main__":
    main()
