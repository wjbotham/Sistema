from math import sqrt,cos,sin

class Vector:
    def __init__(self,x=0,y=0,z=0):
        self.x,self.y,self.z = x,y,z

    def get_magnitude(self):
        return sqrt(self * self)
    magnitude = property(get_magnitude)

    def __eq__(self,other):
        if other.__class__ is Vector:
            return self.coord() == other.coord()
        else:
            return False

    def __add__(self,other):
        if other == 0:
            # makes it possible to sum(vectors) with default init=0
            return self
        return Vector(self.x+other.x,self.y+other.y,self.z+other.z)
    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y,self.z-other.z)

    def __mul__(self,other):
        c = other.__class__
        if c == Vector:
            # dot product
            return (self.x*other.x) + (self.y*other.y) + (self.z*other.z)
        else:
            # scalar
            return Vector(self.x*other,self.y*other,self.z*other)
    def __rmul__(self,other):
        return self.__mul__(other)

    def __truediv__(self,scalar):
        return Vector(self.x/scalar,self.y/scalar,self.z/scalar)
    
    def __neg__(self):
        return Vector(-self.x,-self.y,-self.z)

    def get_normalized(self):
        return self / self.magnitude
    normalized = property(get_normalized)

    def coord(self):
        return self.x,self.y,self.z

    # http://upload.wikimedia.org/wikipedia/commons/4/4f/3D_Spherical.svg
    def rotated(self,theta,phi):
        x,y,z = self.x,self.y,self.z
        # rotation about y-axis (azimuthal)
        x,y,z = sin(theta)*z + cos(theta)*x, y, cos(theta)*z - sin(theta)*x
        # rotation around z-axis
        x,y,z = cos(phi)*x - sin(phi)*y, sin(phi)*x + cos(phi)*y, z
        return Vector(x,y,z)

    def __repr__(self):
        return "Vector(%s,%s,%s)" % (self.x,self.y,self.z)
