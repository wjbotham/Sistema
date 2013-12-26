from physics_snapshot import PhysicsSnapshot
from threading import Thread
from time import clock

class PhysicsCache:
    # TODO maybe we can remove `universe` as an argument someday
    def __init__(self, universe=None):
        self._snapshots = {}
        self._snapshots[0] = PhysicsSnapshot()
        self._snapshots[0].ready = True
        self._latest = 0
        self._oldest = 0
        self._count = 1
        self.running = False
        self.universe = universe
        self.time_per_snapshot = None

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
        self.loop_finish(turn, lambda x: x.game_loop_finish())
        if self.universe and not self.universe.view:
            self.graphics_loop_finish(turn)

    def graphics_loop_finish(self, turn):
        self.loop_finish(turn, lambda x: x.graphics_loop_finish())

    '''
    helper function for game_loop_finish and graphics_loop_finish
    '''
    def loop_finish(self, turn, action):
        try:
            while turn in self._snapshots and not self._snapshots[turn].okay_to_delete:
                action(self._snapshots[turn])
                turn -= 1
        except KeyError as e:
            # this happens if the snapshot gets garbage collected at exactly the wrong time
            if str(e) != str(turn):
                raise

    def _garbage_collect(self, limit=1):
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

    def fetch_center_of_mass(self, body, turn):
        return self._snapshots[turn].kinematics[body].center_of_mass

    def set_center_of_mass(self, body, turn, center_of_mass):
        snapshot = self._snapshots[turn].kinematics[body]
        assert(snapshot.center_of_mass == None)
        snapshot.center_of_mass = center_of_mass

    def init_body(self, body, position, velocity):
        self._snapshots[0].record(body, position, velocity)

    def loop(self):
        self.running = True
        start_time = clock()
        while self.running:
            self.universe.calculate_physics(self.latest+1)
            self._garbage_collect()
            if self.time_per_snapshot == None:
                self.time_per_snapshot = clock() - start_time
            else:
                self.time_per_snapshot = (clock() - start_time + self.time_per_snapshot*19) / 20
            start_time = clock()
            
