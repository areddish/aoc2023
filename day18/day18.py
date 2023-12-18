import sys
sys.setrecursionlimit(10**6)
from collections import defaultdict
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

dir_map = {
    "R" : (1,0),
    "U" : (0,-1),
    "D" : (0,1),
    "L" : (-1,0)
}

hex_digit_to_dir_map = {
    "0": dir_map["R"],
    "1": dir_map["D"],
    "2": dir_map["L"],
    "3": dir_map["U"]
}

xbounds = (0,0)
ybounds = (0,0)
board = {}
start = (0,0)


def floodfill(board, x, y, xbounds, ybounds):
    visited = set()
    q = [(x,y)]
    while q:
        cur = q.pop()
        visited.add(cur)

        for dx,dy in [(-1,0),(1,0),(0,1),(0,-1)]:
            nx = cur[0] + dx
            ny = cur[1] + dy
            if xbounds[0] <= nx <= xbounds[1] and ybounds[0] <= ny <= ybounds[1] and (nx,ny) not in board and (nx,ny) not in visited:
                q.append((nx,ny))  
    return len(visited)

# adapted from various stack overflow, updated dtype as it would overflow otherwise
def shoelace(coords):
    coords = np.array(coords, dtype='int64')
    coords = coords.reshape(-1,2)

    x = coords[:,0]
    y = coords[:,1]

    sum1 = np.sum(x*np.roll(y,-1))
    sum2 = np.sum(y*np.roll(x,-1))

    return int(np.absolute(sum1 - sum2)/2)

def show_map(board, xbounds, ybounds):
    for y in range(ybounds[0], ybounds[1]+1):
        for x in range(xbounds[0], xbounds[1]+1):
            ch = "."
            if (x,y) in board:
                ch = "#"
            print(ch,end="")
        print()


edge_count = 0
part2_edge_count = 0

vertices = [(0,0)]
part2_vertices = [(0,0)]

cursor = (0,0)
part2_cursor = (0,0)

#with open("test.txt") as file:
with open("day18.txt") as file:
    for y,line in enumerate(file.readlines()):
        parts = line.strip().split()
        direction, count, hex = parts

        count = int(count)
        edge_count += count
        cursor = (cursor[0] + (count*dir_map[direction][0]), cursor[1] + (count*dir_map[direction][1]))
        vertices.append(cursor)

        hex = hex[1:-1]
        part2_direction = hex_digit_to_dir_map[hex[-1]]
        part2_count = int(hex[1:-1], 16)        
        part2_edge_count += part2_count
        part2_cursor = (part2_cursor[0] + (part2_count*part2_direction[0]), part2_cursor[1] + (part2_count*part2_direction[1]))
        part2_vertices.append(part2_cursor)

        # original floodfill solution
        # for _ in range(count):            
        #     board[start] = hex
        #     start = (start[0] + dir_map[direction][0], start[1] + dir_map[direction][1])
        #     xbounds = (min(xbounds[0], start[0]),max(xbounds[1], start[0]))
        #     ybounds = (min(ybounds[0], start[1]),max(ybounds[1], start[1]))
        # show_map(board, xbounds, ybounds)

# part 1 - original way answer was obtained
# f = floodfill(board, xbounds[0] + 2, ybounds[0] + (754-664), xbounds, ybounds)
# answer(f+len(board))

# Updated to use shoelace algo and pick's theorem. Although I added +1 as I was off by one.. so some luck
answer(shoelace(vertices) + edge_count //2 + 1)
answer(shoelace(part2_vertices) + part2_edge_count //2 + 1)


