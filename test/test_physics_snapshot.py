import unittest
from threading import Thread,ThreadError
from physics.snapshot import PhysicsSnapshot
import time

class TestPhysicsSnapshot(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        ps = PhysicsSnapshot()
        self.assertTrue(not ps.ready)
        self.assertTrue(not ps.okay_to_delete)

    def test_release(self):
        ps = PhysicsSnapshot()
        with self.assertRaises(ThreadError):
            ps.release()

    def test_record(self):
        ps = PhysicsSnapshot()
        self.assertEqual(ps.kinematics, {})
        ps.record("TEST_BODY", (0,1,2), (3,2,1))
        k = ps.kinematics["TEST_BODY"]
        self.assertEqual(k.position, (0,1,2))
        self.assertEqual(k.velocity, (3,2,1))

    def test_okay_to_delete(self):
        ps = PhysicsSnapshot()
        ps.game_loop_finish()
        self.assertTrue(not ps.okay_to_delete)
        ps.graphics_loop_finish()
        self.assertTrue(ps.okay_to_delete)
        del ps

        ps = PhysicsSnapshot()
        ps.graphics_loop_finish()
        self.assertTrue(not ps.okay_to_delete)
        ps.game_loop_finish()
        self.assertTrue(ps.okay_to_delete)
        del ps

    '''
    this test makes sure that PhysicsSnapshot blocks correctly when other
    methods call PhysicsSnapshot.acquire()
    '''
    def test_blocking(self):
        self.threadSwitch = False
        mainSwitch = False
        ps = PhysicsSnapshot()

        def grabSnapshot():
            ps.acquire()
            self.threadSwitch = True
            # wait long enough that the main thread acquires the snapshot
            time.sleep(0.05)
            # verify the main thread was blocked from flipping mainSwitch
            self.assertTrue(not mainSwitch)
            self.threadSwitch = False
            ps.release()
            time.sleep(0.1)
            # verify the main thread has taken over again and flipped
            # mainSwitch
            self.assertTrue(mainSwitch)
        thread = Thread(target=grabSnapshot)
        thread.start()

        # wait long enough that the side thread flips threadSwitch
        time.sleep(0.01)
        # verify that the side thread has flipped threadSwitch
        self.assertTrue(self.threadSwitch)
        ps.acquire()
        # verify that the side thread has flipped it back
        self.assertTrue(not self.threadSwitch)
        mainSwitch = True

        del self.threadSwitch
