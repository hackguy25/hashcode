
files = [("inputs/"+i+".txt", "outputs/"+i+".txt") for i in "abcdef"]
print(files)

for fn_in, fn_out in files:
    print()
    f_in = open(fn_in, "r")
    f_out = open(fn_out, "w")
    print("file: " + fn_in)

    D, I, S, V, F = f_in.readline().split()
    streets = []
    street_occupancies = dict()
    for i in range(int(S)):
        street = f_in.readline().split()
        streets.append(street)
        street_occupancies[street[2]] = 0
    print("streets: " + S)

    cars = []
    for i in range(int(V)):
        cars.append(f_in.readline())
    print("cars: " + V)

    for car in cars:
        car_streets = car.split()[1:]
        for street in car_streets:
            street_occupancies[street] += 1

    intersection_inputs = [[] for _ in range(int(I))]
    for i in streets:
        intersection = int(i[1])
        intersection_inputs[intersection].append(i[2])

    # f_out.write(f"{sum([len(i)>0 for i in intersection_inputs])}\n")
    printed_intersections = 0
    total_out = ""
    for idx, int_streets in enumerate(intersection_inputs):
        if (len(int_streets) > 0):
            out_str = ""
            # f_out.write(f"{idx}\n")
            # f_out.write(f"{len(int_streets)}\n")
            greens = 0
            for i in range(len(int_streets)):
                if (street_occupancies[int_streets[i]] > 0):
                    out_str += f"{int_streets[i]} 1\n"
                    greens += 1
            if greens > 0:
                printed_intersections += 1
                total_out += f"{idx}\n"
                total_out += f"{greens}\n"
                total_out += out_str
    f_out.write(f"{printed_intersections}\n")
    f_out.write(total_out)
