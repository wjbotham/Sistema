from math import ceil,sqrt
from interface import Interface
from threading import Thread, Lock
from vector import Vector
from time import clock

class Universe:
    def __init__(self,generator,paused=True,G = 8.648208e-15):
        self.bodies = []
        self.time = 0
        # gravitational constant is in kilometers cubed per kilogram per turn squared
        # 1 turn = 6 minutes
        self.G = G
        self.view = None
        self._turn_left = 1
        self.paused = paused
        self.generator = generator
        self.sun = None
        self.physics_locks = {}
        self.next_turn = clock() + 360
        self._seconds_per_turn = 360

    def get_last_cached_turn(self):
        return min(max(body.physics_cache.keys()) for body in self.bodies)
    last_cached_turn = property(get_last_cached_turn)

    def get_seconds_per_turn(self):
        return self._seconds_per_turn
    def set_seconds_per_turn(self, seconds_per_turn):
        turn_left = (self.next_turn - clock()) / self._seconds_per_turn
        self._seconds_per_turn = seconds_per_turn
        self.next_turn = clock() + (turn_left * self._seconds_per_turn)
    seconds_per_turn = property(get_seconds_per_turn, set_seconds_per_turn)

    def get_turn_left(self):
        if self.paused:
            return self._turn_left
        return (self.next_turn - clock()) / self.seconds_per_turn
    turn_left = property(get_turn_left)

    def get_paused(self):
        return self._paused
    def set_paused(self, paused):
        self._paused = paused
        self._turn_left = self.turn_left
    paused = property(get_paused, set_paused)

    def calculate_physics(self, turn):
        if turn not in self.physics_locks:
            self.physics_locks[turn] = Lock()
        self.physics_locks[turn].acquire()
        if self.last_cached_turn < turn-1:
            # if we don't have the previous turn's state, calculate it now
            self.calculate_physics(turn-1)
        for body in [i for i in self.bodies if turn not in i.physics_cache]:
                gravity_sum = sum(body.attraction(other, turn-1) for other in self.bodies if other != body)
                body.physics_cache[turn] = {
                    "position": body.get_position(turn-1) + body.get_velocity(turn-1),
                    "velocity": body.get_velocity(turn-1) + (gravity_sum / body.mass)
                }
        self.physics_locks[turn].release()
        # TODO make this update call conditional on our displaying cached turns
        if self.view:
            self.view.update()

    def pass_turn(self):
        self.time += 1
        dev = self.generator.generate_development()
        if dev:
            print("Development: %d at t=%d" % (dev,self.time))
        if self.view:
            self.view.update()

    def center_of_mass(self):
        total_mass = sum(body.mass for body in self.bodies)
        if total_mass == 0:
            return Vector(0,0,0)
        return sum((body.get_position(self.time) * body.mass) for body in self.bodies)/total_mass

    def travel_time(self,b1,b2,accel):
        velocity_diff = (b1.velocity - b2.velocity).magnitude()
        distance = (b1.position - b2.position).magnitude()
        return ceil((velocity_diff/accel)+(distance/sqrt(accel*distance/4)))

    def ui_loop(self):
        self.view = Interface(self)
        self.view.ui_loop()

    def physics_cache_loop(self):
        while not self.view:
            pass
        while self.view:
            while self.last_cached_turn > (2 * self.time) + 10:
                pass
            self.calculate_physics(self.last_cached_turn + 1)

    def describe_system(self):
        plural = "s"
        if self.time == 1:
            plural = ""
        print("time = "+str(self.time)+" turn"+plural)
        sun = self.bodies[0]
        print(sun.name+": mass="+('%.2E' % sun.mass))
        for i in range(1,len(self.bodies)):
            bodyi = self.bodies[i]
            dist = (self.bodies[0].position - bodyi.position).magnitude()
            orbit_speed = (self.bodies[0].velocity - bodyi.velocity).magnitude()
            print(bodyi.name+": dist=("+('%.2E' % dist)+"), orbit speed=("+('%.2E' % orbit_speed)+"), mass="+('%.2E' % bodyi.mass))
        print()

    def run(self):
        self.start_time = clock()
        ui_t = Thread(target=self.ui_loop)
        ui_t.start()
        phys_t = Thread(target=self.physics_cache_loop)
        phys_t.start()
        while not self.view:
            pass
        self.next_turn = clock() + self.seconds_per_turn
        while self.view:
            while clock() < self.next_turn:
                if self.paused:
                    turn_left = self.turn_left
                    while self.paused and self.view:
                        pass
                    self.next_turn = clock() + (turn_left * self.seconds_per_turn)
                pass
            self.pass_turn()
            self.next_turn += self.seconds_per_turn
