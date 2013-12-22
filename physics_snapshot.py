from threading import Lock
from kinematic import Kinematic

class PhysicsSnapshot:
    def __init__(self):
        self.kinematics = {}
        self.lock = Lock()
        self.ready = False
        self.game_loop_done = False
        self.graphics_loop_done = False

    def acquire(self):
        self.lock.acquire()

    def record(self, body, position, velocity, sat_accel = 0):
        assert(body not in self.kinematics)
        self.kinematics[body] = Kinematic(position, velocity, sat_accel = 0)

    def release(self):
        if (not self.ready):
            # apply satellite acceleration before we mark this as done
            def applySatAccel(sat, accel):
                self.kinematics[sat].accelerate(accel)
                for subsat in sat.satellites:
                    applySatAccel(subsat, accel)
            
            for body in self.kinematics.keys():
                for sat in body.satellites:
                    applySatAccel(sat, self.kinematics[body].sat_accel)
        
        self.ready = True
        self.lock.release()

    def game_loop_finish(self):
        self.game_loop_done = True

    def graphics_loop_finish(self):
        self.graphics_loop_done = True

    def get_okay_to_delete(self):
        return self.game_loop_done and self.graphics_loop_done
    okay_to_delete = property(get_okay_to_delete)
