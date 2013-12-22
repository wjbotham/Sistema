from physics_snapshot import PhysicsSnapshot

class PhysicsCache:
    def __init__(self):
        self._snapshots = {}
        self._snapshots[0] = PhysicsSnapshot()
        self._snapshots[0].ready = True
        self._latest = 0
        self._count = 1

    def acquire(self, turn):
        if turn not in self._snapshots:
            self._snapshots[turn] = PhysicsSnapshot()
        self._snapshots[turn].acquire()

    '''
    tracks the highest turn for which PhysicsSnapshot.ready is true
    '''
    def get_latest(self):
        return self._latest
    latest = property(get_latest)

    '''
    tracks the number of turns for which PhysicsSnapshot.ready is true
    '''
    def get_count(self):
        return self._count
    count = property(get_count)

    def has(self, turn):
        return turn in self._snapshots and self._snapshots[turn].ready

    def record(self, turn, body, position, velocity, sat_accel=0):
        self._snapshots[turn].record(body, position, velocity, sat_accel)

    def release(self, turn):
        was_ready = self._snapshots[turn].ready
        self._snapshots[turn].release()
        if not was_ready:
            self._count += 1
            if turn > self._latest:
                self._latest = turn

    def game_loop_finish(self, turn):
        if turn in self._snapshots:
            self._snapshots[turn].game_loop_finish()
            self.verify_and_delete(turn)
            self.game_loop_finish(turn-1)

    def graphics_loop_finish(self, turn):
        if turn in self._snapshots:
            self._snapshots[turn].graphics_loop_finish()
            self.verify_and_delete(turn)
            self.graphics_loop_finish(turn-1)

    def verify_and_delete(self, turn):
        if turn in self._snapshots and turn < self.latest:
            snapshot = self._snapshots[turn]
            snapshot.acquire()
            if snapshot.okay_to_delete and not snapshot.being_deleted:
                snapshot.being_deleted = True
                snapshot.release()
                del self._snapshots[turn]
                self._count -= 1
            else:
                snapshot.release()

    def fetch_velocity(self, body, turn):
        return self._snapshots[turn].kinematics[body].velocity

    def fetch_position(self, body, turn):
        return self._snapshots[turn].kinematics[body].position

    def init_body(self, body, position, velocity):
        self._snapshots[0].record(body, position, velocity)
