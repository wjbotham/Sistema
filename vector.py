from math import sqrt,cos,sin

class Vector:
    def __init__(self,x=0,y=0,z=0):
        self.x,self.y,self.z = x,y,z

    def magnitude(self):
        return sqrt(self.dot_product())

    def dot_product(self,other=None):
        if other == None:
            other = self
        return (self.x*other.x) + (self.y*other.y) + (self.z*other.z)

    def add(self,other):
        return Vector(self.x+other.x,self.y+other.y,self.z+other.z)

    def subtract(self,other):
        return self.add(other.neg())

    def multiply(self,scalar):
        return Vector(self.x*scalar,self.y*scalar,self.z*scalar)

    def divide(self,scalar):
        return Vector(self.x/scalar,self.y/scalar,self.z/scalar)
    
    def neg(self):
        return Vector(-self.x,-self.y,-self.z)

    def normalize(self):
        return self.divide(self.magnitude())

    # http://upload.wikimedia.org/wikipedia/commons/4/4f/3D_Spherical.svg
    def rotate(self,theta,phi):
        x,y,z = self.x,self.y,self.z
        # rotation about y-axis (azimuthal)
        x,y,z = sin(theta)*z + cos(theta)*x, y, cos(theta)*z - sin(theta)*x
        # rotation around z-axis
        x,y,z = cos(phi)*x - sin(phi)*y, sin(phi)*x + cos(phi)*y, z
        return Vector(x,y,z)

    def __repr__(self):
        return "Vector(%s,%s,%s)" % (self.x,self.y,self.z)
