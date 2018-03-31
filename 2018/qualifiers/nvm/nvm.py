filename = "e_high_bonus"
input_file = open("input/"+filename+".in", "r")

R, C, F, N, B, T = input_file.readline().split()

import copy
from operator import attrgetter

def get_rides(vehicle):
    c_rides = []
    for ride in av_rides:
        ride.tget_travel(vehicle)
        c_rides.append(ride)
    rides = sorted(c_rides, key=attrgetter('tg_travel'))
    return rides

class Vehicle():
    def __init__(self, vehicle_id):
        self.id = vehicle_id
        self.location = [0, 0]

        # steps taken should not be more than the maximum
        # number of steps available in the simulation
        self.steps_taken = 0
        self.rides_taken = []
    
    def take_ride(self, ride):
        # in taking a ride, the vehicle travels first to 
        # the ride's starting location, computes and follows
        # the ride's waiting time and moves the ride to its
        # finish location
        self.location = ride.start_location
        self.steps_taken += ride.travel_time(self)
        self.location = ride.finish_location
        self.rides_taken.append(ride.id)
        return
    
    def __repr__(self):
        return f"Id: {self.id}; Steps: {self.steps_taken}; Location: {self.location}"

class Ride():
    def __init__(self, id,  a, b, x, y, s, f):
        self.id = id
        self.start_location = [int(a), int(b)]
        self.finish_location = [int(x), int(y)]
        self.earliest_start = int(s)
        self.latest_finish = int(f)

        self.tg_travel = 0

    def movement(self, origin, destination):
        # get the time it takes to travel from one
        # location to another
        a, b = origin
        x, y = destination
        steps = abs((a - x) + (b- y))
        return steps
    
    def tget_travel(self, vehicle):
        self.tg_travel = self.travel_time(vehicle)
    
    def travel_time(self, vehicle):
        # time to start location
        vehicle_location = vehicle.location
        ttsl = self.movement(vehicle_location, self.start_location)

        # wait time
        steps_taken = vehicle.steps_taken
        if steps_taken >= self.earliest_start:
            wait_time = 0
        else:
            wait_time = self.earliest_start - steps_taken
        
        # time to finish location
        ttfl = self.movement(self.start_location, self.finish_location)

        total_time = ttsl + wait_time + ttfl
        return total_time
    
    def __repr__(self):
        return f"Ride Id: {self.id}"

vehicles = [Vehicle(i) for i in range(int(F))]
rides = []
count = 0

# make a list of rides from provided data
for line in input_file.readlines():
    a, b, x, y, s, f = line.split()
    rides.append(Ride(count, a, b, x, y, s, f))
    count += 1

# dependent variables
av_rides = copy.copy(rides)
vehicle_queue = copy.copy(vehicles)

# how about calculating the thing
# lets try zipping

while av_rides:
    cut = av_rides[:len(vehicle_queue)]
    sim = zip(vehicle_queue, av_rides)

    for v, r in sim:
        v.take_ride(r)
    
    av_rides = av_rides[len(vehicle_queue):]

# to submit..
output_file = open("output/" + filename + ".out", "w")
for vehicle in vehicle_queue:
    n = str(len(vehicle.rides_taken))
    r = [str(i) for i in vehicle.rides_taken]
    r = " ".join(r)

    output_file.write(n + " " + r + "\n")
