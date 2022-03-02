
files = [("inputs/"+i+".txt", "outputs/"+i+".txt") for i in "abcdef"]
print(files)

for fn_in, fn_out in files:
    print()
    f_in = open(fn_in, "r")
    f_out = open(fn_out, "w")
    print("file: " + fn_in)

    D, I, S, V, F = f_in.readline().split()
    streets = {}
    street_occupancies = dict()
    for i in range(int(S)):
        street = f_in.readline().split()
        streets[street[2]] = street
        street_occupancies[street[2]] = 0
    print("streets: " + S)

    cars = []
    for i in range(int(V)):
        cars.append(f_in.readline())
    print("cars: " + V)

    car_times = []
    cars_to_remove = []
    for i, car in enumerate(cars):
        car_streets = car.split()[1:]
        time = 0
        for street in car_streets:
            time += int(streets[street][3])
        if time - int(streets[car_streets[0]][3]) <= int(D):
            car_times.append(time)
            for street in car_streets:
                street_occupancies[street] += 1
        else:
            cars_to_remove.append(i)
    for c in cars_to_remove:
        cars.pop(c)

    car_times, cars = zip(*sorted(zip(car_times, cars)))

    intersection_inputs = [[] for _ in range(int(I))] #bomo dodajali ulice :D
    """for i in streets:
        intersection = int(streets[i][1])
        intersection_inputs[intersection][] = (0, 0)"""

    for car in cars:
        time_to_street = 0
        for street in car.split()[1:]:
            starting_intersection = intersection_inputs[int(streets[street][1])]
            if len(starting_intersection) == 0:
                starting_intersection.append({'street': street, 'time': time_to_street})
            else:
                if street not in [x['street'] for x in starting_intersection]:
                    starting_intersection.append({'street': street, 'time': time_to_street})
            time_to_street += int(streets[street][3])
    
    new_intersection_inputs = [[] for _ in range(int(I))]
    for i, intersection in enumerate(intersection_inputs):
        if len(intersection) <= 1:
            new_intersection = intersection
        else:
            #print([x['time'] for x in intersection])
            #print([x['street'] for x in intersection])
            times, streets2 = zip(*sorted(zip([x['time'] for x in intersection], [x['street'] for x in intersection])))
            new_times = [min(max(y-x, 1), int(D)) for x, y in zip(times, times[1:])] 
            new_times.append(1)
            new_intersection = []
            for j, street in enumerate(streets2):
                new_intersection.append({'street': street, 'time': new_times[j]})
        new_intersection_inputs[i] = new_intersection
    
    intersection_inputs = new_intersection_inputs

    # f_out.write(f"{sum([len(i)>0 for i in intersection_inputs])}\n")
    printed_intersections = 0
    total_out = ""
    for idx, streets2 in enumerate(intersection_inputs):
        if (len(streets2) > 0):
            out_str = ""
            # f_out.write(f"{idx}\n")
            # f_out.write(f"{len(streets)}\n")
            greens = 0
            for i in range(len(streets2)):
                if (street_occupancies[streets2[i]['street']] > 0):
                    out_str += f"{streets2[i]['street']} {1 + street_occupancies[streets2[i]['street']] // 11}\n"
                    greens += 1
            if greens > 0:
                printed_intersections += 1
                total_out += f"{idx}\n"
                total_out += f"{greens}\n"
                total_out += out_str
    f_out.write(f"{printed_intersections}\n")
    f_out.write(total_out)
