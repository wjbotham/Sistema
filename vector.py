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

    def rotate(self,rx,ry,rz):
        # rotation around z
        ax = cos(rz)*self.x - sin(rz)*self.y
        ay = sin(rz)*self.x + cos(rz)*self.y
        az = self.z
        # rotation around y
        bx = cos(ry)*ax - sin(ry)*az
        by = ay
        bz = sin(ry)*ax + cos(ry)*az
        # rotation around x
        cx = bx
        cy = cos(rx)*by - sin(rx)*bz
        cz = sin(rx)*by + cos(rx)*bz
        return Vector(cx,cy,cz)

    def __repr__(self):
        return "Vector(%s,%s,%s)" % (self.x,self.y,self.z)
