from blaz import save_result, input_filenames, output_filenames

def read_file(fname):
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

for filei in range(1, 6):
    print(input_filenames[filei])
    people, projects = read_file(input_filenames[filei])

    sorted_projects = sorted(projects, key=lambda x: x[1])

    assigned_projects = []
    # pari (clovek, kaj dela, koliko je bilo zahtevano, kdaj je fraj, na katerem projektu je)
    used_people = []
    current_time = 0
    poskusi = 0
    while sorted_projects is not None and poskusi <= 100:
        sorted_projects = sorted(sorted_projects, key=lambda x: x[3]-current_time)
        for project in [x for x in sorted_projects if x[0] not in [y[0] for y in assigned_projects]]:
            #print(project)
            found_roles = True
            assigned_projects.append((project[0], []))
            temp_list = []
            for role in project[4]:
                peeps_with_skill = [(p, people[p]) for p in people if \
                     role[0] in people[p] and \
                          people[p][role[0]] >= role[1] and \
                              p not in [x[0][0] for x in used_people] and \
                                  p not in assigned_projects[-1][1]]
                #print(peeps_with_skill)
                #print(people)
                if not peeps_with_skill:
                    found_roles = False
                    break
                sorted_peeps = sorted(peeps_with_skill, key=lambda x: x[1][role[0]])
                assigned_projects[-1][1].append(sorted_peeps[0][0])
                #print("TUKAJ")
                #print(assigned_projects)
                temp_list.append((sorted_peeps[0], role[0], role[1], project[1]+current_time, project))
                #print(used_people)
            #print(assigned_projects[-1])
            already_assigned_roles = [x[1] for x in temp_list]
            #print(already_assigned_roles)
            if already_assigned_roles is not None and len(already_assigned_roles) != 0:
                #print(already_assigned_roles)
                missing_roles = [x for x in project[4] if x[0] not in already_assigned_roles]
                #print(missing_roles)
               # print(missing_roles)
                for role in missing_roles:
                    for possible_mentor in assigned_projects[-1][1]:
                        # can mentor?
                        #print(possible_mentor)
                        mentor_person = (possible_mentor, people[possible_mentor])
                        #print(mentor_person)
                        if role[0] in mentor_person[1] and mentor_person[1][role[0]] >= role[1]:

                            if role[1] == 1:
                                peeps_with_skill = [(p, people[p]) for p in people if \
                                    role[0] in people[p] and \
                                    p not in [x[0][0] for x in used_people] and \
                                        p not in assigned_projects[-1][1]]
                                peeps_with_skill = sorted(peeps_with_skill, key=lambda x: len(x[1]))
                            else:
                                peeps_with_skill = [(p, people[p]) for p in people if \
                                role[0] in people[p] and \
                                    people[p][role[0]] >= role[1] - 1 and \
                                        p not in [x[0][0] for x in used_people] and \
                                            p not in assigned_projects[-1][1]]
                            #print(people)
                            #print(peeps_with_skill)
                            if not peeps_with_skill:
                                found_roles = False
                                break
                        
                            assigned_projects[-1][1].append(peeps_with_skill[0][0])
                            temp_list.append((peeps_with_skill[0], role[0], role[1], project[1]+current_time, project))

            #print(found_roles)
            if not found_roles:
                assigned_projects = assigned_projects[:-1]
                continue
            used_people.extend(temp_list)
            #print(assigned_projects)
            #print(used_people)
            #print(current_time)
            for pname in assigned_projects[-1][1]:
                person = None
                for pppp in used_people:
                    if pname == pppp[0][0]:
                        person = pppp
                        break
                level_cloveka = person[0][1][person[1]]
                level_na_projektu = person[2]
                #print("clovek {}".format(level_cloveka))
                #print("projekt {}".format(level_na_projektu))
                if level_na_projektu >= level_cloveka:
                    people[person[0][0]][person[1]] += 1

        poskusi += 1
        # povecat current time
        # zbrisat used people

        #print("SMO NA KONC ENGA FORA")
        
        if used_people is None or len(used_people) == 0:
            break
        #print(used_people)
        min_fraj = min(used_people, key=lambda x: x[3])[3]
        #print(min_fraj)
        #people_to_delete = []
        for peep in used_people:
            if peep[3] == min_fraj:
                if peep[4] in sorted_projects:
                    sorted_projects.remove(peep[4])
        used_people = [x for x in used_people if x[3] != min_fraj]

        #used_people.remove(people_to_delete)

        current_time = min_fraj
        #print(used_people)
        #print(current_time)
        #print(assigned_projects)


    #print(assigned_projects)

    save_result(assigned_projects, output_filenames[filei])
    #break

        
    