from core.world_gen import WorldGenerator

''' mass is in kilograms '''
''' distance is in kilometers '''
''' time is in turns, and 1 turn = 6 minutes '''

def main():
    wg = WorldGenerator("Here is my sample system")
    u = wg.generate_system()
    u.run()

if __name__ == "__main__":
    main()
