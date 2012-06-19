from world_gen import WorldGenerator
from agent import Agent

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''

def main():
    wg = WorldGenerator("Here is my sample system")
    u = wg.generate_system()
    a = Agent("UNSK5672",u.bodies[0])
    b = Agent("SDBJ3178",u.bodies[0])
    u.run()

if __name__ == "__main__":
    main()
