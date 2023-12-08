from collections import defaultdict, Counter
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
        print(parts, src, r, l)
        move_graph[src] = { "L": l, "R": r}

    cur = "AAA"
    steps = 0
    stop = False
    while not stop:
        for dx in list(directions):
            cur = move_graph[cur][dx]
            steps += 1
            if cur == "ZZZ":
                answer(steps)
                stop = True
                break

    cur = []
    cycles = []
    for src in move_graph:
        if src[-1] == "A":
            cur.append(src)
            cycles.append(None)
    print(cur)
    steps = 0
    stop = False
    
    while not stop:
        for dx in list(directions):
            for i in range(len(cur)):
                cur[i] = move_graph[cur[i]][dx]
            steps += 1
            done = False
            # if steps % 1000:
            #     print(cur)
            for i in range(len(cur)):
                if cur[i][-1] == "Z" and cycles[i] == None:
                    cycles[i] = steps
                    print("CYCLES:", cycles)
            if all(cycles):
                stop = True
                part2 = cycles[0]
                for i in range(1,len(cycles)):
                    part2 = lcm(part2, cycles[i])
                answer(part2)
                break