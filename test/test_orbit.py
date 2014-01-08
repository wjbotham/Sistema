import unittest
from threading import Thread
from universe import Universe
from body import Body

class TestOrbit(unittest.TestCase):
    def setUp(self):
        self.u = Universe()
        self.u.sun = Body("The Sun", pow(10, 30),
                   pow(10, 12), universe=self.u)
        self.t = Thread(target=self.u.run, args=[False])

    def tearDown(self):
        self.u.stop()

    def test_solitary(self):
        starting_position = self.u.sun.position
        five_days = 10*24*5

        self.t.start()
        while (self.u.physics_cache.latest < five_days):
            pass
        self.u.paused = False
        while (self.u.time < five_days):
            pass
        self.u.paused = True
        self.assertEqual(self.u.sun.position, starting_position)
    
    def test_moon(self):
        self.u.sun.add_satellite("Satellite",
                                 pow(2, 70),
                                 pow(2, 42.5),
                                 (255,255,255),
                                 pow(2,27),
                                 0,
                                 0,
                                 pow(2,-6),
                                 0,
                                 0,
                                 False)
        starting_distance = self.u.bodies[0].distance(self.u.bodies[1])
        one_day = 10*24

        self.t.start()
        for i in range(1,10+1):
            while (self.u.physics_cache.latest < one_day*i):
                pass
            self.u.paused = False
            while (self.u.time < one_day*i):
                pass
            self.u.paused = True
            new_distance = self.u.bodies[0].distance(self.u.bodies[1])
            self.assertTrue(starting_distance*0.99999 <= new_distance <= starting_distance*1.00001)
