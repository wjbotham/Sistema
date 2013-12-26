from math import ceil,sqrt
from interface import Interface
from threading import Thread
from vector import Vector
from physics_cache import PhysicsCache
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
        self._paused = paused
        self.generator = generator
        self.sun = None
        self.physics_cache = PhysicsCache(self)
        self.next_turn = clock() + 360
        self._seconds_per_turn = 360
        self.running = False

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
        return max(0, self.next_turn - clock()) / self.seconds_per_turn
    turn_left = property(get_turn_left)

    def get_paused(self):
        return self._paused
    def set_paused(self, paused):
        # if unpausing
        if self.paused and not paused:
            self.next_turn = clock() + (self._turn_left * self.seconds_per_turn)
            # self._turn_left only has meaning while paused
            del self._turn_left
        # else if pausing
        elif not self.paused and paused:
            self._turn_left = self.turn_left
        self._paused = paused
    paused = property(get_paused, set_paused)

    def get_center_of_mass(self):
        total_mass = sum(body.mass for body in self.bodies)
        if total_mass == 0:
            return Vector(0,0,0)
        return sum((body.get_position(self.time) * body.mass) for body in self.bodies)/total_mass
    center_of_mass = property(get_center_of_mass)

    def calculate_physics(self, turn):
        self.physics_cache.acquire(turn)
        if not self.physics_cache.has(turn):
            for body in self.bodies:
                gravity_sum = 0
                satellite_gravity_sum = 0
                for other in self.bodies:
                    # if the other is body's primary, use other's mass and body's system_mass
                    if body.primary == other:
                        component = body.attraction(other, turn-1, True, False)
                        gravity_sum += component
                        satellite_gravity_sum += component
                    # if the other is body's satellite, use other's system_mass and body's mass
                    elif body == other.primary:
                        gravity_sum += body.attraction(other, turn-1, False, True)
                    # if we are satellites of the same primary, use system_mass of each
                    elif body.primary == other.primary:
                        component = body.attraction(other, turn-1, True, True)
                        gravity_sum += component
                        satellite_gravity_sum += component
                    # otherwise, do not calculate an interaction
                position = body.get_position(turn-1) + body.get_velocity(turn-1)
                velocity = body.get_velocity(turn-1) + (gravity_sum * self.G)
                sat_accel = satellite_gravity_sum * self.G
                self.physics_cache.record(turn, body, position, velocity, sat_accel)
        self.physics_cache.release(turn)

    def pass_turn(self):
        self.time += 1
        dev = self.generator.generate_development()
        if dev:
            print("Development: %d at t=%d" % (dev,self.time))
        # give the goahead from our side to delete this record
        self.physics_cache.game_loop_finish(self.time - 1)

    def travel_time(self,b1,b2,accel):
        velocity_diff = (b1.velocity - b2.velocity).magnitude
        distance = (b1.position - b2.position).magnitude
        return ceil((velocity_diff/accel)+(distance/sqrt(accel*distance/4)))

    def ui_loop(self):
        self.view = Interface(self)
        self.view.ui_loop()

    def physics_cache_loop(self):
        start_time = clock()
        while self.view:
            self.calculate_physics(self.physics_cache.latest + 1)
            if self.time_per_snapshot < self.seconds_per_turn or self.paused:
                self.physics_cache.garbage_collect(2)
            self.time_per_snapshot = (clock() - start_time + self.time_per_snapshot*9) / 10
            start_time = clock()

    def describe_system(self):
        plural = "s"
        if self.time == 1:
            plural = ""
        print("time = "+str(self.time)+" turn"+plural)
        sun = self.bodies[0]
        print(sun.name+": mass="+('%.2E' % sun.mass))
        for i in range(1,len(self.bodies)):
            bodyi = self.bodies[i]
            dist = (self.bodies[0].position - bodyi.position).magnitude
            orbit_speed = (self.bodies[0].velocity - bodyi.velocity).magnitude
            print(bodyi.name+": dist=("+('%.2E' % dist)+"), orbit speed=("+('%.2E' % orbit_speed)+"), mass="+('%.2E' % bodyi.mass))
        print()

    def make_system_tree(self, turn=None):
        sorted_bodies = sorted(self.bodies, key=lambda b: b.mass)
        for i in range(0,len(sorted_bodies)-1):
            bodyi = sorted_bodies[i]
            highest_influence = 0
            primary = None
            for j in range(i+1,len(sorted_bodies)):
                bodyj = sorted_bodies[j]
                dist = bodyi.distance(bodyj, turn)
                influence = bodyj.mass / dist / dist
                if influence > highest_influence:
                    highest_influence = influence
                    primary = bodyj
            bodyi.primary = primary

    def run(self):
        self.start_time = clock()
        ui_t = Thread(target=self.ui_loop)
        ui_t.start()
        while not self.view:
            pass
        phys_t = Thread(target=self.physics_cache.loop)
        phys_t.start()
        self.next_turn = clock() + self.seconds_per_turn
        self.running = True
        while self.view:
            while (self.paused or clock() < self.next_turn) and self.view:
                pass
            if (self.physics_cache.latest <= self.time):
                self.paused = True
            else:
                self.pass_turn()
                self.next_turn += self.seconds_per_turn

    def stop(self):
        self.running = False
        self.physics_cache.running = False
        self.view = None
