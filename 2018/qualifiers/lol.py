filename = "e_high_bonus"
input_file = open("input/"+filename+".in", "r")

R, C, F, N, B, T = input_file.readline().split()

import copy
from operator import attrgetter


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
    	return f"{self.id}; {self.steps_taken}; {self.location}"

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

def get_rides(vehicle):
    c_rides = []
    for ride in av_rides:
        ride.tget_travel(vehicle)
        c_rides.append(ride)
    rides = sorted(c_rides, key=attrgetter('tg_travel'))
    return rides


vehicles = [Vehicle(i) for i in range(int(F))]
rides = []
count = 0

for line in input_file.readlines():
    a, b, x, y, s, f = line.split()
    rides.append(Ride(count, a, b, x, y, s, f))
    count += 1


av_rides = copy.copy(rides)
vehicle_queue = copy.copy(vehicles)


while av_rides:
	# select a vehicle
	vehicle = vehicle_queue.pop(0)
	
	# get rides for this vehicle
	closest_rides = get_rides(vehicle)
	
	# select the closest
	ride = closest_rides.pop(0)
	
	# match vehicle and ride
	vehicle.take_ride(ride)
	
	# update available rides
	av_rides.remove(ride)
	
	# rides has been made, add vehicle back to the queue
	vehicle_queue.append(vehicle)

# unsolved but submitting
output_file = open("output/"+filename+".out", "w")
for vehicle in vehicle_queue:
	n = str(len(vehicle.rides_taken))
	rides = [str(i) for i in vehicle.rides_taken]
	rs = " ".join(rides)
	output_file.write(n + " " + rs + "\n")

output_file.close()