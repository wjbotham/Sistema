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

    def rotate(self,theta,phi):
        ax = cos(theta)*self.x - sin(theta)*self.y
        ay = sin(theta)*self.x + cos(theta)*self.y
        az = self.z
        bx = cos(phi)*ax - sin(phi)*az
        by = ay
        bz = sin(phi)*ax + cos(phi)*az
        return Vector(bx,by,bz)
