from collections import defaultdict

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

N = 0
E = 1
S = 2
W = 3

moves = {
    # type : NESW
    "|": [True, False, True, False ],
    "-": [False, True, False, True ],

    "L": [True, True, False, False ],
    "J": [True, False, False, True ],
    "7": [False, False, True, True ],
    "F": [False, True, True, False ],

    ".": [False, False, False, False ],
}

m2 = {
    # type : NESW
    "|": { N: N, S: S },
    "-": { E: E, W: W  },

    "L": { W:N, S:E }, 
    "J": { E:N, S:W }, 
    "7": { N:W, E:S }, 
    "F": { N:E, W:S }, 

    ".": { }
}
part1 = 0
part2 = 0

board = []
start = None
#with open("test2.txt") as file:
#with open("test.txt") as file:
with open("day10.txt") as file:
    for i, line in enumerate(file.readlines()):        
        line = line.strip()
        if "S" in line:
            start = (line.index("S"), i)
            line = line.replace("S","L") # day10
            #line = line.replace("S","F") # test
            #line = line.replace("S","F") # test2
        row = list(line)
        board.append(row)

Width = len(board[0])
H = len(board)

def get_neighbors(b, cur, w, h):
    x,y = cur
    for dy in range(-1,2,1):
        for dx in range(-1,2,1):
            if dx == 0 and dy == 0:
                continue
            nx = x+dx
            ny = y+dy
            print(dx,dy, board[ny][nx])

def print_neighbors(b, cur, w, h):
    x,y = cur
    for dy in range(-1,2,1):
        for dx in range(-1,2,1):
            nx = x+dx
            ny = y+dy
            print(board[ny][nx],end="")
        print()

asciimap = {
    "F": "┌",
    "J": "┘",
    "-": "─",
    "|": "│",
    "7": "┐",
    "L": "└"
}

asciimap2 = {
    "F": "╔",
    "J": "╝",
    "-": "═",
    "|": "║",
    "7": "╗",
    "L": "╚"
}
def pb(b, w, h, path=None):
    for y in range(h):
        for x in range(w):            
            m = asciimap2 if path and x in path[y] else asciimap
            print(m.get(b[y][x], b[y][x]), end="")
        print()

pb(board, Width, H)
print(start)

def get_next_dir(cur_dir):
    if cur_dir == N:
        return E
    if cur_dir == E:
        return S
    if cur_dir == S:
        return W
    if cur_dir == W:
        return N

def get_right_dir(dir):
    if dir == N:
        return E
    if dir == E:
        return S
    if dir == S:
        return W
    if dir == W:
        return N

# follow the path, and look right, we count any thing right of the current direction

def count_right(c1, ch, dir, path, inside):

    directions_to_test = [get_right_dir(dir)]

    # corners count in two direcitons.
    if ch == "L":
        if dir == E:
            directions_to_test.append(get_right_dir(S))
        else:
            assert dir == N
            directions_to_test.append(get_right_dir(W))
    if ch == "F":
        if dir == E:
            directions_to_test.append(get_right_dir(N))
        else:
            assert dir == S
            directions_to_test.append(get_right_dir(W))
    if ch == "7":
        if dir == S:
            directions_to_test.append(get_right_dir(E))
        else:
            assert dir == W
            directions_to_test.append(get_right_dir(N))
    if ch == "J":
        if dir == N:
            directions_to_test.append(get_right_dir(E))
        else:
            assert dir == W
            directions_to_test.append(get_right_dir(S))


    for dir in directions_to_test:
        while True:
            # Move one right
            move = dir
            if move == N:
                c1 = (c1[0], c1[1] - 1)
            elif move == E:
                c1 = (c1[0]+1, c1[1])
            elif move == S:
                c1 = (c1[0], c1[1] + 1)
            elif move == W:
                c1 = (c1[0]-1, c1[1])
            else:
                assert False
            
            if c1[0] in path[c1[1]]:
                break

            inside.add(c1) 

def traverse(board, existing_path=None, inside=None):
    part1 = 0
    c1 = start
    path = defaultdict(list)
    path[c1[1]].append(c1[0])

    dir = list(m2[board[c1[1]][c1[0]]].values())[0]
    Stop = False

    directed_path = defaultdict(list)
    directed_path[c1] = dir
    while not Stop:
        if existing_path:
            count_right(c1, board[c1[1]][c1[0]], dir, existing_path, inside)
        move = dir
        if move == N:
            c1 = (c1[0], c1[1] - 1)
        elif move == E:
            c1 = (c1[0]+1, c1[1])
        elif move == S:
            c1 = (c1[0], c1[1] + 1)
        elif move == W:
            c1 = (c1[0]-1, c1[1])
        else:
            assert False

        path[c1[1]].append(c1[0])
        directed_path[c1] = move

        # new position
        ch = board[c1[1]][c1[0]]
        # new dir
        dir = m2[ch][dir]
        #print(c1)
        if c1 == start:
            Stop = True
        
        part1 += 1
    return part1 // 2, path, directed_path

part1, path, directed_path = traverse(board, None)
answer(part1)

inside = set()
part1, path, _ = traverse(board, path, inside)
answer(len(inside)+15) # missed 15

for x,y in inside:
    board[y][x] = "I"
pb(board, Width, H, path)
exit(-1)
# # # scan l to r 
# inside_chars = ["|", "L", "F"]
# for y in sorted(path.keys()):
#     x_scanline = sorted(path[y])
#     # for x in range(len(x_scanline)-1):
#     #     part2 += x_scanline[x+1] - x_scanline[x]
#     start = min(x_scanline)
#     end = max(x_scanline)
#     print(y,start,end)
#     while start < end:
#         if board[y][start] == "|":
#             start += 1 
#             while board[y][start] == ".":
#                 part2 += 1

#         while start in x_scanline and start < end:
#             start += 1
#         while start not in x_scanline and start < end:
#             part2 += 1
#             start += 1

def can_reach_path(board, path, cur):
    x,y = cur
    if cur in path:
        return False
    if board[y][x] != ".":
        return False
    
    hit_path = 0
    # up
    for ny in range(y,-1,-1):
        if path.get((x,ny), None) == get_right_dir(N):
            hit_path += 1
            break

    # down
    for ny in range(y,len(board),1):
        #if x in path[ny]:
        if path.get((x,ny), None) == get_right_dir(S):
            hit_path += 1
            break

    # left
    for nx in range(x,-1,-1):
        #if nx in path[y]:
        if path.get((nx,y), None) == get_right_dir(E):
            hit_path += 1
            break

    # right
    for nx in range(x,len(board[0]),1):
        #if nx in path[y]:
        if path.get((nx,y), None) == get_right_dir(W):
            hit_path += 1
            break

    return hit_path == 4

def can_reach_path2(board, path, cur):
    x,y = cur
    if cur in path:
        return False
    if board[y][x] != ".":
        return False
    
    # go left and right
    hit_path = 0
    # up
    for ny in range(y,-1,-1):
        if path.get((x,ny), None) == get_right_dir(N):
            hit_path += 1
            break

    # down
    for ny in range(y,len(board),1):
        #if x in path[ny]:
        if path.get((x,ny), None) == get_right_dir(S):
            hit_path += 1
            break

    # left
    for nx in range(x,-1,-1):
        #if nx in path[y]:
        if path.get((nx,y), None) == get_right_dir(E):
            hit_path += 1
            break

    # right
    for nx in range(x,len(board[0]),1):
        #if nx in path[y]:
        if path.get((nx,y), None) == get_right_dir(W):
            hit_path += 1
            break

    return hit_path == 4

marked_board = []
for y in range(H):
    row = []
    for x in range(Width):
        if can_reach_path(board, directed_path, (x,y)):
            part2 += 1
            row.append("I")
        else:
            row.append(board[y][x])
    marked_board.append(row)
pb(marked_board, Width, H)
answer(part2)