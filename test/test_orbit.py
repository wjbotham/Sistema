import unittest
from threading import Thread
from universe import Universe
from body import Body

class TestOrbit(unittest.TestCase):
    def test_solitary(self):
        u = Universe()
        u.sun = Body("The Sun", pow(10, 30),
                   pow(10, 12), universe=u)
        starting_position = u.sun.position
        t = Thread(target=u.run, args=[False])
        t.start()
        five_days = 10*24*5
        while (u.physics_cache.latest < five_days):
            pass
        u.paused = False
        while (u.time < five_days):
            pass
        u.paused = True
        self.assertEqual(u.sun.position, starting_position)
        u.stop()
    
    def test_moon(self):
        u = Universe()
        u.sun = Body("The Sun", pow(10, 30),
                   pow(10, 12), universe=u)
        u.sun.add_satellite("Satellite",
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
        starting_distance = u.bodies[0].distance(u.bodies[1])
        t = Thread(target=u.run, args=[False])
        t.start()
        one_day = 10*24
        for i in range(1,10+1):
            while (u.physics_cache.latest < one_day*i):
                pass
            u.paused = False
            while (u.time < one_day*i):
                pass
            u.paused = True
            new_distance = u.bodies[0].distance(u.bodies[1])
            self.assertTrue(starting_distance*0.99999 <= new_distance <= starting_distance*1.00001)
        u.stop()
