from collections import defaultdict
import heapq
import numpy as np
###
#   Submission helper, print the answer and copy it to the clipboard
#   to reduce the amount of times I have the answer and mistype it :).
###
#import pyperclip
answer_part = 1
def answer(v):
    global answer_part
    #pyperclip.copy(v)
    print("Part 1 =" if answer_part == 1 else "Part 2 =", v)
    answer_part = 2

part1 = 0
part2 = 0

stones = []
#with open("test.txt") as file:
with open("day24.txt") as file:
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        pos, vel = line.split(" @")
        pos = tuple([int (x) for x in pos.split(",")])
        vel = [int (x) for x in vel.split(",")]
        print(pos,vel)
        assert pos not in stones
        stones.append((pos, vel))

def ray_ray_intersection(p1,v1,p2,v2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    det = v2[0] * v1[1] - v2[1] * v1[0]
    if det == 0:
        return -1,-1
    u = (dy * v2[0] - dx * v2[1]) / det
    v = (dy * v1[0] - dx * v1[1]) / det
    if u < 0 or v < 0:
        return -1, -1
    return p1[0] + u * v1[0], p1[1] + u * v1[1]

# ignore z
min_xy = 200000000000000
max_xy = 400000000000000

for i in range(len(stones)):
    for j in range(i + 1, len(stones)):
        p1 = stones[i][0]
        p2 = stones[j][0]
        v1 = stones[i][1]
        v2 = stones[j][1]

        x_interset, y_intersect = ray_ray_intersection(p1,v1,p2,v2)

        if min_xy <= x_interset <= max_xy and min_xy <= y_intersect <= max_xy:
            #print("Collide", p1, p2, x_interset, y_intersect)
            part1 += 1

answer(part1)
