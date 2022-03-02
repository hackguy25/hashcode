import json

# vrne (people: list, projects: list)
#     person: (ime: str, skills: dict(str -> int))
#     project: (ime: str, duration: int, score: int, best_before: int, roles: list)
#         role: (skill: str, level: int)

def read_file(fname):
    people = []
    projects = []
    with open(fname) as f_in:
        nums = f_in.readline().split()
        num_people = int(nums[0])
        num_projects = int(nums[1])

        for i in range(num_people):
            peep = f_in.readline().split()
            poop = dict()
            for j in range(int(peep[1])):
                skill = f_in.readline().split()
                poop[skill[0]] = int(skill[1])
            people.append((peep[0], poop))

        for i in range(num_projects):
            proj = f_in.readline().split()
            poop = []
            for i in range(int(proj[4])):
                role = f_in.readline().split()
                poop.append((role[0], int(role[1])))
            projects.append((
                proj[0],
                int(proj[1]),
                int(proj[2]),
                int(proj[3]),
                poop
            ))
    return (people, projects)

def erika_read(fname):
    people = {}
    projects = []
    with open(fname) as f_in:
        nums = f_in.readline().split()
        num_people = int(nums[0])
        num_projects = int(nums[1])

        for i in range(num_people):
            peep = f_in.readline().split()
            poop = dict()
            for j in range(int(peep[1])):
                skill = f_in.readline().split()
                poop[skill[0]] = int(skill[1])
            people[peep[0]] = poop

        for i in range(num_projects):
            proj = f_in.readline().split()
            poop = []
            for i in range(int(proj[4])):
                role = f_in.readline().split()
                poop.append((role[0], int(role[1])))
            projects.append((
                proj[0],
                int(proj[1]),
                int(proj[2]),
                int(proj[3]),
                poop
            ))
    return (people, projects)

def pad_skills(people):
    skills = [list(people[k].keys()) for k in people]
    skills = list({item for sublist in skills for item in sublist})
    for peep in people:
        for skill in skills:
            if skill not in people[peep]:
                people[peep][skill] = 0
    return people


# vzame projects: list, fname: string
#    project: (name: str, participants: list of str)
def save_result(projects, fname):
    with open(fname, "w") as f_out:
        f_out.write(f"{len(projects)}\n")
        for project in projects:
            f_out.write(f"{project[0]}\n")
            f_out.write(f"{' '.join(project[1])}\n")

def sort_by_latest_starting_day(projects):
    return sorted(projects, key=lambda project: project[3] - project[1])

def find_acceptable(roles):
    ret = dict()
    to_remove = None
    while len(roles) > 0:
        # print(f"  {roles}")
        # print(f"    {to_remove}")
        # print(f"    {ret}")
        if to_remove != None:
            roles.pop(to_remove[0])
            for (name, candidates) in roles:
                if to_remove[1] in candidates:
                    candidates.remove(to_remove[1])
            to_remove = None
        for (i, (name, candidates)) in enumerate(roles):
            if len(candidates) == 0:
                return None
            if len(candidates) == 1:
                to_remove = (i, candidates[0])
                ret[name] = to_remove[1]
                break
        if len(roles) > 0 and to_remove == None:
            to_remove = (0, roles[0][1][0])
            ret[roles[0][0]] = to_remove[1]
    return ret



def naive_noupdate(people, projects):
    # max_day = max(i[2] + i[3] for i in projects) + 1
    # print(max_day)
    projects = sort_by_latest_starting_day(projects)
    current_day = 0
    ret = []
    # print(people)

    for project in projects:
        #print(f"day {current_day}")
        #print(project)
        if current_day + project[1] - project[2] // 2 > project[3]:
            print(f"expired by {current_day + project[1] - project[3]} days")
            continue
        roles = []
        for role in project[4]:
            candidates = []
            for (i, person) in enumerate(people):
                #print(person)
                if role[0] in person[1] and person[1][role[0]] >= role[1]:
                    candidates.append(i)
            roles.append((role[0], candidates))
        # print(roles)
        nabor = find_acceptable(roles)
        # print(nabor)
        if nabor == None:
            # print("-----")
            continue
        # print(project[4])
        # print([people[nabor[i[0]]][0] for i in project[4]])
        ret.append((project[0], [people[nabor[i[0]]][0] for i in project[4]]))
        current_day += project[1]

    print(ret)
    print()
    return ret

input_filenames = [
    "input/a_an_example.in.txt",
    "input/b_better_start_small.in.txt",
    "input/c_collaboration.in.txt",
    "input/d_dense_schedule.in.txt",
    "input/e_exceptional_skills.in.txt",
    "input/f_find_great_mentors.in.txt"
]

output_filenames = [
    "output/a.txt",
    "output/b.txt",
    "output/c.txt",
    "output/d.txt",
    "output/e.txt",
    "output/f.txt"
]


if __name__ == "__main__":
    # print(json.dumps(read_file("input/a_an_example.in.txt"), indent=4))

    # for i in range(0, 6):
    #     save_result(naive_noupdate(*read_file(input_filenames[i])), output_filenames[i])

    # naive_noupdate(*read_file(input_filenames[1]))
    (people, projects) = erika_read(input_filenames[0])
    print(people)
    pad_skills(people)
    print(people)