from math import sqrt,cos,sin
from decimal import Decimal

class Vector:
    def __init__(self,x=0,y=0,z=0):
        self.x,self.y,self.z = Decimal(x),Decimal(y),Decimal(z)

    def magnitude(self):
        return self.dot_product().sqrt()

    def dot_product(self,other=None):
        if other == None:
            other = self
        return (self.x*other.x) + (self.y*other.y) + (self.z*other.z)

    def add(self,other):
        return Vector(self.x+other.x,self.y+other.y,self.z+other.z)

    def subtract(self,other):
        return self.add(other.neg())

    def multiply(self,scalar):
        scalar = Decimal(scalar)
        return Vector(self.x*scalar,self.y*scalar,self.z*scalar)

    def divide(self,scalar):
        scalar = Decimal(scalar)
        return Vector(self.x/scalar,self.y/scalar,self.z/scalar)
    
    def neg(self):
        return Vector(-self.x,-self.y,-self.z)

    def normalize(self):
        return self.divide(self.magnitude())

    def rotate(self,theta,phi):
        ax = Decimal(cos(theta))*self.x - Decimal(sin(theta))*self.y
        ay = Decimal(sin(theta))*self.x + Decimal(cos(theta))*self.y
        az = self.z
        bx = Decimal(cos(phi))*ax - Decimal(sin(phi))*az
        by = ay
        bz = Decimal(sin(phi))*ax + Decimal(cos(phi))*az
        return Vector(bx,by,bz)
