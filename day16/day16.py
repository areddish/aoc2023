import sys
sys.setrecursionlimit(10**6)

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

def show_map(board):
    for y in range(len(board)):
        print("".join(board[y]))

def show_path(board, path):
    PATH_CHARS = {
        (1,0): ">",
        (-1,0): "<",
        (0,1): "V",
        (0,-1): "^"
    }
    temp = deepcopy(board)
    for l,d in path:
        ch = temp[l[1]][l[0]]
        temp[l[1]][l[0]] = PATH_CHARS[d] if ch == "." else ch

    show_map(temp)

def follow_light(board, start, dir):
    beams = [(start, dir)]
    marked = set()
    while beams:
        cur = beams.pop()
        while cur not in marked:
            x,y = cur[0]
            if x < 0 or y < 0 or x >= len(board[0]) or y >= len(board):
                break
            dx,dy = cur[1]
            ch = board[y][x]
            marked.add(cur)
            if ch == ".":
                cur = ((x+dx, y+dy), (dx,dy))
            elif ch == "|":
                if (dx,dy) == (0,1) or (dx,dy) == (0,-1):
                    cur = ((x+dx, y+dy), (dx,dy))
                else:
                    beams.append(((x,y+1), (0, 1)))
                    marked.add(((x,y), (0,-1)))
                    cur = ((x,y-1), (0,-1))
            elif ch == "-":
                if (dx,dy) == (1,0) or (dx,dy) == (-1,0):
                    cur = ((x+dx, y+dy), (dx,dy))
                else:
                    beams.append(((x-1,y), (-1,0)))
                    marked.add(((x,y), (1,0)))
                    cur = ((x+1,y), (1,0))
            elif ch == "\\":
                if (dx,dy) == (0,1):
                    new_dir = (1,0)
                elif (dx,dy) == (-1,0):
                    new_dir = (0,-1)                    
                elif (dx,dy) == (1, 0):
                    new_dir = (0,1)
                else:
                    new_dir = (-1,0)
                cur = ((x+new_dir[0],y+new_dir[1]), new_dir)

            elif ch == "/":   
                if (dx,dy) == (0,-1):
                    new_dir = (1,0)
                elif (dx,dy) == (0,1):
                    new_dir = (-1,0)
                elif (dx,dy) == (-1,0):
                    new_dir = (0,1)
                else:
                    new_dir = (0,-1)
                cur = ((x+new_dir[0],y+new_dir[1]), new_dir)
            if cur in marked:
                pass
    #show_path(board, marked)
    marked_locations = set()
    for l,d in marked:
        marked_locations.add(l)
    return len(marked_locations)

part1 = 0
part2 = 0

start = (0,0)
dir = (1,0)

board = []
from copy import copy, deepcopy
#with open("test.txt") as file:
with open("day16.txt") as file:
    for y,line in enumerate(file.readlines()):
        line = line.strip()
        board.append(list(line.strip()))

    # part1 
    part1 = follow_light(board, (0,0), (1,0))

    # part 2
    starting_loc_and_dir = [((x,0),(0,1)) for x in range(len(board[0]))]
    starting_loc_and_dir += [((x,len(board)-1),(0,-1)) for x in range(len(board[0]))]
    for y in range(len(board)):
        starting_loc_and_dir.append(((0,y),(1,0)))
        starting_loc_and_dir.append(((len(board[0])-1,y),(-1,0)))

    ls = []
    for cur_loc_and_dir in starting_loc_and_dir:
        ls.append(follow_light(board, *cur_loc_and_dir))
    part2 = max(ls)
answer(part1)
answer(part2)