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
    def rotate(self,theta,phi,spin):
        # rotation around x-axis
        ax = self.x
        ay = cos(spin)*self.y - sin(spin)*self.z
        az = sin(spin)*self.y + cos(spin)*self.z
        # rotation about y-axis (azimuthal)
        bx = sin(theta)*az + cos(theta)*ax
        by = ay
        bz = cos(theta)*az - sin(theta)*ax
        # rotation around z-axis
        cx = cos(phi)*bx - sin(phi)*by
        cy = sin(phi)*bx + cos(phi)*by
        cz = bz
        return Vector(cx,cy,cz)

    def __repr__(self):
        return "Vector(%s,%s,%s)" % (self.x,self.y,self.z)
