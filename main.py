from universe import Universe
from world_gen import generate_system
from time import clock

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''

def main():
    u = generate_system()
    u.generate_view_thread()

    while not u.view:
        None
    next_tick = clock()+1
    while u.view:
        while clock() < next_tick:
            None
        u.pass_hour(1)
        next_tick += 1

if __name__ == "__main__":
    main()
