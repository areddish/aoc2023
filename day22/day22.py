from collections import defaultdict
###
#   Submission helper, print the answer and copy it to the clipboard
#   to reduce the amount of times I have the answer and mistype it :).
###
#import pyperclip
from copy import deepcopy
answer_part = 1
def answer(v):
    global answer_part
    #pyperclip.copy(v)
    print("Part 1 =" if answer_part == 1 else "Part 2 =", v)
    answer_part = 2

part1 = 0
part2 = 0

def is_in_cube(v, brick):
    v1,v2 = brick
    x,y,z = v

    # this point is above
    if z > max(v1[2],v2[2]):
        return False
    
    # colinear
    if v == v1 or v == v2:
        return True

    # point is inside this brick    
    if (v1[0] <= x < v1[0] and v1[1] <= y < v1[1] and v1[2] <= z < v1[2]) or (v2[0] <= x < v2[0] and v2[1] <= y < v2[1] and v2[2] <= z < v2[2]):
        return True
    
    return False

def collide(bricks, brick, index, ignore_brick_index):
    v1,v2 = brick
    for i in range(0, index-1):
        if i == ignore_brick_index:
            continue

        if AABB_intersection(brick, bricks[i]):
            return True
        
    return False

def AABB_intersection(a,b):
    ax1,ay1,az1 = a[0]
    ax2,ay2,az2 = a[1]

    bx1,by1,bz1 = b[0]
    bx2,by2,bz2 = b[1]
    return (min(ax1,ax2) <= max(bx1,bx2) and max(ax1,ax2) >= min(bx1,bx2)) and (min(ay1,ay2) <= max(by1,by2) and max(ay1,ay2) >= min(by1,by2)) and (min(az1,az2) <= max(bz1,bz2) and max(az1,az2) >= min(bz1,bz2))
    

def settle_bricks(bricks, ignore_brick_index, do_move):
    num_moved = 0
    # sort by z
    z_sorted_bricks = sorted(bricks,key=lambda b: min(b[0][2], b[1][2]))

    index = ignore_brick_index + 1 if ignore_brick_index else 0
    while index < len(z_sorted_bricks):
        # if index == ignore_brick_index:
        #     index += 1
        #     continue

        brick = z_sorted_bricks[index]
        dz = -1
        # try to move this down as far as it can go.
        nv1,nv2 = brick
        _, _, z1 = nv1
        _, _, z2 = nv2
        while min(z1, z2) != 1 and not collide(z_sorted_bricks, ((nv1[0],nv1[1],z1+dz), (nv2[0],nv2[1],z2+dz)), index + 1, ignore_brick_index):
            z1 += dz
            z2 += dz

        moved_brick = ((nv1[0],nv1[1],z1), (nv2[0],nv2[1],z2))
        num_moved += 1 if moved_brick != brick else 0
        if do_move:            
            z_sorted_bricks[index] = moved_brick

        index += 1

    print(f"Moved {num_moved} bricks")
    return z_sorted_bricks, num_moved

bricks = []
with open("test.txt") as file:
#with open("day22.txt") as file:
    for y,line in enumerate(file.readlines()): 
        v1,v2 = line.strip().split("~")
        bricks.append(([int(x) for x in v1.split(",")],[int(x) for x in v2.split(",")]))

bricks, num_moved = settle_bricks(bricks, None, do_move=True)
print(bricks)
for i in range(len(bricks)):
    print("Testing brick",i)
    _, num_moved = settle_bricks(bricks, ignore_brick_index=i, do_move=False)    
    if num_moved == 0:
        part1 += 1

answer(part1)
#answer(part2)