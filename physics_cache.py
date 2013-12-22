from physics_snapshot import PhysicsSnapshot
from threading import Thread
from time import clock

class PhysicsCache:
    def __init__(self):
        self._snapshots = {}
        self._snapshots[0] = PhysicsSnapshot()
        self._snapshots[0].ready = True
        self._latest = 0
        self._oldest = 0
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
        _turn = turn
        while _turn in self._snapshots:
            self._snapshots[_turn].game_loop_finish()
            _turn -= 1

    def graphics_loop_finish(self, turn):
        _turn = turn
        while _turn in self._snapshots:
            self._snapshots[_turn].graphics_loop_finish()
            _turn -= 1

    def garbage_collect(self, limit=1):
        _limit = limit
        while self._oldest != self._latest and _limit > 0:
            if self._snapshots[self._oldest].okay_to_delete:
                del self._snapshots[self._oldest]
                self._count -= 1
                i = self._oldest
                while i not in self._snapshots:
                    i += 1
                self._oldest = i
                _limit -= 1
            else:
                _limit = 0

    def fetch_velocity(self, body, turn):
        return self._snapshots[turn].kinematics[body].velocity

    def fetch_position(self, body, turn):
        return self._snapshots[turn].kinematics[body].position

    def init_body(self, body, position, velocity):
        self._snapshots[0].record(body, position, velocity)
