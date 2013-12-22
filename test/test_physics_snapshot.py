import unittest
from threading import Thread
from physics_snapshot import PhysicsSnapshot
import time

class TestPhysicsSnapshotFunctions(unittest.TestCase):
    def setUp(self):
        pass

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
            time.sleep(0.02)
            # verify the main thread was blocked from flipping mainSwitch
            self.assertTrue(not mainSwitch)
            self.threadSwitch = False
            ps.release()
            time.sleep(0.01)
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
