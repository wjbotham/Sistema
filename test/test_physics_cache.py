import unittest
from physics_cache import PhysicsCache

class TestPhysicsCacheFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        pc = PhysicsCache()
        self.assertEqual(pc.latest(), 0)
        self.assertEqual(pc.count(), 1)
        self.assertTrue(pc.has(0))
