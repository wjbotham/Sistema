from universe import Universe
from world_gen import generate_system

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''
 
def main():
    u = generate_system()

    distances = []
    u.report()
    #for i in range(1000):
    #    u.pass_hour()
    #    if i%100 == 99:
    #        u.report()

if __name__ == "__main__":
    main()
