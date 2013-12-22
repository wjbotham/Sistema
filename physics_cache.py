from physics_snapshot import PhysicsSnapshot
from threading import Thread
from time import clock

class PhysicsCache:
    def __init__(self):
        self._snapshots = {}
        self._snapshots[0] = PhysicsSnapshot()
        self._snapshots[0].ready = True
        self._latest = 0
        self._count = 1
        self.garbage_collector = None
        self.start_garbage_collection()

    def start_garbage_collection(self):
        assert(not self.garbage_collector)
        self.garbage_collector = Thread(target = self.collector_loop)
        self.garbage_collector.start()

    def acquire(self, turn):
        if turn not in self._snapshots:
            if not self.garbage_collector:
                self.start_garbage_collection()
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

    def graphics_loop_finish(self, turn):
        if turn in self._snapshots:
            self._snapshots[turn].graphics_loop_finish()

    def collector_loop(self):
        lowest = 0
        lookingForNewLowest = False
        time_of_last_snapshot = clock()
        old_latest = self.latest
        while clock() < time_of_last_snapshot + 1:
            for turn in range(lowest, self.latest):
                if turn == lowest and turn not in self._snapshots:
                    lookingForNewLowest = True
                elif turn in self._snapshots:
                    if lookingForNewLowest:
                        lowest = turn
                        lookingForNewLowest = False
                    if self._snapshots[turn].okay_to_delete:
                        for delete_turn in range(lowest, turn+1):
                            if delete_turn in self._snapshots:
                                del self._snapshots[delete_turn]
                                self._count -= 1
            if old_latest != self.latest:
                time_of_last_snapshot = clock()
            old_latest = self.latest
        self.garbage_collector = None

    def fetch_velocity(self, body, turn):
        return self._snapshots[turn].kinematics[body].velocity

    def fetch_position(self, body, turn):
        return self._snapshots[turn].kinematics[body].position

    def init_body(self, body, position, velocity):
        self._snapshots[0].record(body, position, velocity)
