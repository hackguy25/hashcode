
files = [("inputs/"+i+".txt", "outputs/"+i+".txt") for i in "abcdef"]
print(files)

for fn_in, fn_out in files:
    print()
    f_in = open(fn_in, "r")
    f_out = open(fn_out, "w")
    print("file: " + fn_in)

    D, I, S, V, F = f_in.readline().split()
    streets = []
    for i in range(int(S)):
        streets.append(f_in.readline())
    print("streets: " + S)

    cars = []
    for i in range(int(V)):
        cars.append(f_in.readline())
    print("cars: " + V)

    intersection_inputs = [[] for _ in range(int(I))]
    for i in streets:
        ii = i.split()
        intersection = int(ii[1])
        intersection_inputs[intersection].append(ii[2])

    f_out.write(f"{sum([len(i)>0 for i in intersection_inputs])}\n")
    for idx, streets in enumerate(intersection_inputs):
        if (len(streets) > 0):
            f_out.write(f"{idx}\n")
            f_out.write(f"{len(streets)}\n")
            for i in range(len(streets)):
                f_out.write(f"{streets[i]} 1\n")


