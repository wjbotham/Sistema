from physics_snapshot import PhysicsSnapshot

class PhysicsCache:
    def __init__(self):
        self._snapshots = {}
        self._snapshots[0] = PhysicsSnapshot()
        self._snapshots[0].ready = True

    def acquire(self, turn):
        if turn not in self._snapshots:
            self._snapshots[turn] = PhysicsSnapshot()
        self._snapshots[turn].acquire()

    def latest(self):
        return max(self._snapshots)

    def count(self):
        return len(self._snapshots)

    def has(self, turn):
        return turn in self._snapshots and self._snapshots[turn].ready

    def record(self, turn, body, position, velocity, sat_accel):
        self._snapshots[turn].record(body, position, velocity, sat_accel)

    def release(self, turn):
        self._snapshots[turn].release()

    def game_loop_finish(self, turn):
        if turn in self._snapshots:
            self._snapshots[turn].game_loop_finish()
            if self._snapshots[turn].okay_to_delete:
                del self._snapshots[turn]

    def graphics_loop_finish(self, turn):
        if turn in self._snapshots:
            self._snapshots[turn].graphics_loop_finish()
            if self._snapshots[turn].okay_to_delete:
                del self._snapshots[turn]

    def fetch_velocity(self, body, turn):
        return self._snapshots[turn].kinematics[body].velocity

    def fetch_position(self, body, turn):
        return self._snapshots[turn].kinematics[body].position

    def init_body(self, body, position, velocity):
        self._snapshots[0].record(body, position, velocity)
