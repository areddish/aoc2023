import math

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

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

move_graph = {}
directions = None

#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day8.txt") as file:
    for line in file.readlines():        
        if not line.strip():
            continue
        if not directions:
            directions = line.strip()
            continue
        parts = line.strip().split(" = ")
        src = parts[0]
        l,r = parts[1].replace("(","").replace(")","").split(", ")
        move_graph[src] = { "L": l, "R": r}

def traverse(move_graph, directions, start, end_condition):
    cur = start
    steps = 0
    stop = False
    while not stop:
        for dx in list(directions):
            cur = move_graph[cur][dx]
            steps += 1
            if end_condition(cur):
                return steps

# part 1
answer(traverse(move_graph, directions, "AAA", lambda loc: loc == "ZZZ"))

# part 2
starting_locations = []
steps_to_end = []
for src in move_graph:
    if src[-1] == "A":
        starting_locations.append(src)
#print(starting_locations)
for i in range(len(starting_locations)):
    steps_to_end.append(traverse(move_graph, directions, starting_locations[i], lambda loc: loc[-1] == "Z"))
#print(steps_to_end)
part2 = steps_to_end[0]
for step_count in steps_to_end[1:]:
    part2 = lcm(part2, step_count)
answer(part2)