from universe import Universe
from world_gen import generate_system

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''
 
def main():
    u = generate_system()
    u.generate_view_thread()

    for i in range(10000):
        u.pass_hour(24)

if __name__ == "__main__":
    main()
