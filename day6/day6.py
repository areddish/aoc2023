###
#   Submission helper, print the answer and copy it to the clipboard
#   to reduce the amount of times I have the answer and mistype it :).
###
import pyperclip
answer_part = 1
def answer(v):
    global answer_part
    pyperclip.copy(v)
    print("Part 1 =" if answer_part == 1 else "Part 2 =", v)
    answer_part = 2


def sim_race(time, distance_goal):
    count = 0
    for hold in range(time-1):
        #race for time - holding time
        race_time = time - hold
        distance_covered = race_time * hold
        if distance_covered > distance_goal:
            count += 1
    return count

part1 = 1
times = []
dists = []
#with open("test.txt") as file:
with open("day6.txt") as file:
        lines = file.readlines()
        line = lines[0].strip()
        for num in line.split(":")[1].strip().split(" "):
            if num:
                times.append(int(num))

        line = lines[1].strip()
        for num in line.split(":")[1].strip().split(" "):
            if num:
                dists.append(int(num))

        for i in range(len(times)):
            part1 *= sim_race(times[i], dists[i])
answer(part1)

time = int("".join([str(x) for x in times]))
distance = int("".join([str(x) for x in dists]))
answer(sim_race(time, distance))
