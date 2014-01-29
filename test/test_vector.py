import unittest
from core.vector import Vector
from math import sqrt

class TestVector(unittest.TestCase):
    def setUp(self):
        self.zero_vector = Vector(0,0,0)
        self.test_vector = Vector(1,2,3)
        self.unit_vector = Vector(1/sqrt(3),1/sqrt(3),1/sqrt(3))
        self.sum_vector = Vector(1+1/sqrt(3), 2+1/sqrt(3), 3+1/sqrt(3))

    def test_magnitude(self):
        self.assertEqual(self.zero_vector.magnitude, 0)
        self.assertEqual(self.test_vector.magnitude, sqrt(14))
        self.assertEqual(self.unit_vector.magnitude, 1)

    def test_arithmetic(self):
        self.assertEqual(self.zero_vector + self.test_vector, self.test_vector)
        self.assertEqual(self.test_vector - self.test_vector, self.zero_vector)
        temp = self.test_vector
        temp += self.unit_vector
        self.assertEqual(temp, self.sum_vector)
        temp = self.test_vector
        temp *= 3
        self.assertEqual(temp, Vector(3,6,9))
        self.assertEqual(self.test_vector + self.test_vector, self.test_vector * 2)
        self.assertEqual(self.test_vector / 2, Vector(1/2, 1, 3/2))
        self.assertEqual(self.test_vector + self.unit_vector, self.sum_vector)
        self.assertEqual(-self.test_vector, self.test_vector * -1)

    def test_dot_product(self):
        left_hand = round(self.test_vector * self.unit_vector, 13)
        right_hand = round(2*sqrt(3), 13)
        self.assertEqual(left_hand, right_hand)
        self.assertEqual(self.test_vector * self.zero_vector, 0)

if __name__ == '__main__':
    unittest.main()
