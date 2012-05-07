from universe import Universe
from world_gen import generate_system

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''
 
def main():
    u = generate_system()

    distances = []
    u.describe_system()
    for i in range(10):
        u.pass_hour()
        u.describe_system()

if __name__ == "__main__":
    main()
