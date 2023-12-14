from collections import defaultdict
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

def p(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            print(board[y][x], end="")
        print()
    
def slide(board, x, y, dir):
    dx,dy = dir
    if dy != 0:
        while 0 <= y < len(board):
            y += dy
            if y < len(board) and board[y][x] != ".":
                y -= dy
                break
        if y < 0:
            y = 0
        if y == len(board):
            y = len(board) - 1
    if dx != 0:
        while 0 <= x < len(board[0]):
            x += dx
            if x < len(board[0]) and board[y][x] != ".":
                x -= dx
                break
        if x < 0:
            x = 0
        if x == len(board[0]):
            x = len(board[0]) - 1

    return (x,y)

def tilt(board, yrange, xrange, offset=(0,-1)):
#    ans = sum([1 if ch == 'O' else 0 for ch in board[0]]) * (len(board))
    for y in yrange:
        for x in xrange:
            if board[y][x] == "O":
                nx,ny = slide(board,x,y,offset)
                board[y][x] = "."
                board[ny][nx] = "O"
                # if (x,y) != (nx,ny):
                #     val = len(board) - ny
                #     #print(f"{len(board)} {ny} {x},{y} -> {nx},{ny}  {val}")
                #     ans += val
                # else:
                #     val = len(board) - y
                #     ans += val

def compute_load(board):
    ans = 0
    H = len(board)
    for y in range(H):
        for x in range(len(board[0])):
            if board[y][x] == "O":
                ans += H - y
    return ans

board = []

#with open("test.txt") as file:
with open("day14.txt") as file:
    index = 1
    for y,line in enumerate(file.readlines()): 
        line = line.strip()
        board.append(list(line))

    part1_done = False
    #p(board)
    answers = defaultdict(list)
    # This number found by testing
    #  1000 -> no answer
    #  5000 -> 3 answers (99862, 99861, 99875)
    #  8000 -> 2 answers (99861, 99875)
    #  10000 -> 1 answer.. and it's common with other's
    for i in range(1,10000+1):#000000+1):
        tilt(board, range(0,len(board)), range(0,len(board[0])), (0,-1))
        if not part1_done:
            answer(compute_load(board))
            part1_done = True
        tilt(board, range(0,len(board)), range(0,len(board[0])), (-1,0))
        tilt(board, range(len(board)-1,-1,-1), range(0,len(board[0])), (0,1))
        tilt(board, range(0,len(board)), range(len(board[0])-1, -1, -1), (1,0))
        load = compute_load(board)
        answers[load].append(i)
        if i % 1000 == 0:
            print(f"{i}: {load}")

    for k in answers:
        # need enough samples
        if len(answers[k]) < 100:
            continue
        # find the first occurence and the cycle
        index = min(answers[k])
        cycle = answers[k][-1] - answers[k][-2]
        #print(k, index, cycle)
        # if we could reach that in 1000000000, it's our answer.
        # could there by more than one?
        if (1000000000 - index) % cycle == 0:
            answer(k)            