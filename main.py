from universe import Universe
from world_gen import generate_system
from view import View

''' mass is in kilograms '''
''' distance is in kilometers '''
''' velocity is in kilometers per minute '''
 
def main():
    u = generate_system()
    v = View(u)
    
    distances = []
    #u.describe_system()
    for i in range(10000):
        u.pass_hour(1)
        v.update()
        #u.describe_system()
    v.close()

if __name__ == "__main__":
    main()
