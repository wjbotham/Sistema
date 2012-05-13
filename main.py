from universe import Universe
from world_gen import generate_system

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''
 
def main():
    u = generate_system()
    u.generate_view_thread()

    while not u.view:
        None
    while u.view:
        u.pass_hour(1)

if __name__ == "__main__":
    main()
