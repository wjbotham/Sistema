import unittest
from physics.cache import PhysicsCache
from time import sleep

class TestPhysicsCache(unittest.TestCase):
    def test_latest(self):
        pc = PhysicsCache()
        self.assertEqual(pc.latest, 0)
        pc.acquire(3)
        pc.release(3)
        pc.acquire(2)
        pc.release(2)
        self.assertEqual(pc.latest, 3)
    
    def test_count(self):
        pc = PhysicsCache()
        count = len([i for i in pc._snapshots if pc._snapshots[i].ready])
        self.assertEqual(count, 1)
        self.assertEqual(pc.count, count)
        pc.acquire(3)
        pc.release(3)
        pc.acquire(2)
        count = len([i for i in pc._snapshots if pc._snapshots[i].ready])
        self.assertEqual(count, 2)
        self.assertEqual(pc.count, count)
        pc.release(2)
        count = len([i for i in pc._snapshots if pc._snapshots[i].ready])
        self.assertEqual(count, 3)
        self.assertEqual(pc.count, count)

    def test_has(self):
        pc = PhysicsCache()
        self.assertTrue(pc.has(0))
        self.assertTrue(not pc.has(3))
        pc.acquire(3)
        self.assertTrue(not pc.has(3))
        pc.release(3)
        self.assertTrue(pc.has(3))

    def test_garbage_collection_precondition(self):
        pc = PhysicsCache()
        pc.acquire(1)
        pc.release(1)
        pc.acquire(2)
        pc.release(2)

        # verify that game_loop_finish does not permit collection by itself,
        # but does in conjunction with graphics_loop_finish
        pc.game_loop_finish(0)
        pc._garbage_collect()
        self.assertEqual(pc.count, 3)
        self.assertEqual(pc.latest, 2)
        self.assertTrue(pc.has(0))
        pc.graphics_loop_finish(0)
        pc._garbage_collect()
        self.assertEqual(pc.count, 2)
        self.assertEqual(pc.latest, 2)
        self.assertTrue(not pc.has(0))

        # verify that graphics_loop_finish does not permit collection by
        # itself, but does in conjunction with game_loop_finish
        pc.graphics_loop_finish(1)
        pc._garbage_collect()
        self.assertEqual(pc.count, 2)
        self.assertEqual(pc.latest, 2)
        self.assertTrue(pc.has(1))
        pc.game_loop_finish(1)
        pc._garbage_collect()
        self.assertEqual(pc.count, 1)
        self.assertEqual(pc.latest, 2)
        self.assertTrue(not pc.has(1))

    def test_garbage_collection_cascade(self):
        pc = PhysicsCache()
        pc.acquire(1)
        pc.release(1)
        pc.acquire(2)
        pc.release(2)

        # verify that a snapshot that's okay_to_delete also causes earlier
        # snapshots to be okay_to_delete
        pc.graphics_loop_finish(1)
        pc.game_loop_finish(1)
        pc._garbage_collect(2)
        self.assertEqual(pc.count, 1)
        self.assertEqual(pc.latest, 2)
        self.assertTrue(not pc.has(0))
        self.assertTrue(not pc.has(1))
        self.assertTrue(pc.has(2))

    def test_garbage_collection_protects_latest(self):
        pc = PhysicsCache()
        pc.acquire(1)
        pc.release(1)

        # verify that the latest snapshot will not permit itself to be deleted
        pc.graphics_loop_finish(1)
        pc.game_loop_finish(1)
        pc._garbage_collect(2)
        self.assertTrue(pc.has(1))
