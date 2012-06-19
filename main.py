from world_gen import WorldGenerator

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''

def main():
    wg = WorldGenerator("Here is my sample system")
    u = wg.generate_system()
    u.run()

if __name__ == "__main__":
    main()
