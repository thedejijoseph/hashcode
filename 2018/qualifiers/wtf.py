# first of, read the file in
filename = 'e_high_bonus'
content = open("input/"+filename+".in", 'r')

R, C,F,N,B,T = content.readline().split()

ride_times = []
count = 0
for ride_d in content.readlines():
    a, b, x, y, s, f = ride_d.split()
    time_to_origin = abs((0 - int(a) + (0 - int(b))))
    if int(s) > time_to_origin:
        waiting_time = int(s) - time_to_origin
    else:
        waiting_time = 0
    
    time_to_start = time_to_origin + waiting_time

    time_to_drop = abs((int(a) - int(x)) + (int(b) - int(y)))
    total_time = time_to_start + time_to_drop
    ride_times.append([count, total_time])
    count += 1

no_of_vehicles = int(F)
solution = {}
limit = int(T)

import copy
k = lambda r: r[1]
pride = sorted(ride_times, key=k)

for vehicle in range(1, no_of_vehicles+1):
    vehicle_no = vehicle
    capacity, vehicle_contains = 0, []
    
    while True:
        if pride != []:
            ride_no, ride_time = pride.pop(0)
        else:
            break
        capacity += ride_time
        if capacity <= limit:
            vehicle_contains.append(ride_no)
            #print(vehicle_no, ride_no, vehicle_contains)
            continue
        elif capacity > limit:
            pride.insert(0, [ride_no, ride_time])
            break
    solution[vehicle_no] = vehicle_contains

with open("output/"+filename+".out", "w") as submit:
	for vehicle, t_rides in solution.items():
		rides = " ".join([str(r) for r in t_rides])
		vehicle = str(vehicle)
		no_of_rides = str(len(t_rides))
		
		line = str(no_of_rides + " " + rides + "\n")
		submit.write(line)