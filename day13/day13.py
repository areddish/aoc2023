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

def horiz_differences(board,y1,y2):
    diff = 0
    for x in range(len(board[0])):
        if board[y1][x] != board[y2][x]:
            #diff.append((x,y1,board[y1][x],x,y2,board[y2][x]))
            diff += 1
    return diff

def vert_differences(board,x1,x2):
    diff = 0
    for y in range(len(board)):
        if board[y][x1] != board[y][x2]:
            #diff.append((x1,y,board[y][x1],x2,y,board[y][x2]))
            diff += 1
    return diff

def check_horiz(board, x, differences_allowed):
    x1,x2 = x, x+1
    total_differences = 0
    while x1 >= 0 and x2 < len(board):
        total_differences += horiz_differences(board,x1,x2)
        if total_differences > differences_allowed:
            return 0
        x1 -= 1
        x2 += 1
    return 100*(x+1)

def check_vert(board, y, differences_allowed):
    y1,y2 = y, y+1
    total_differences = 0
    while y1 >= 0 and y2 < len(board[0]):
        #slice1 = [board[i][y1] for i in range(len(board))]
        #slice2 = [board[i][y2] for i in range(len(board))]
        total_differences += vert_differences(board,y1,y2)
        if total_differences > differences_allowed: #slice1 != slice2:
            return 0
        y1 -= 1
        y2 += 1
    return y + 1

def find_reflection(board, differences_allowed, previous=None):
    y = 0
    ans = 0
    while y < len(board)-1:
        if (0,y) != previous:
            if horiz_differences(board,y,y+1)<=differences_allowed:
                ans = check_horiz(board, y, differences_allowed)
                if ans:
                    return (ans, 0, y)
        y+=1

    x = 0
    ans = 0
    while x < len(board[0])-1:
        if (x,0) != previous:
            if vert_differences(board,x,x+1)<=differences_allowed:
                ans = check_vert(board, x, differences_allowed)
                if ans:
                    return (ans, x, 0)
        x+=1

    assert False, "No reflection found!"

part1 = 0
part2 = 0

board = []
#with open("test.txt") as file:
with open("day13.txt") as file:
    for line in file.readlines():
        line = line.strip()        
        if not line:
            # print(board)
            a,x,y = find_reflection(board,0)
            part1 += a
            a,x,y = find_reflection(board, 1, (x,y))
            part2 += a
            board = []
        else:
            board.append(line)
    # print(board)
    a,x,y = find_reflection(board,0)
    part1 += a
    a,x,y = find_reflection(board, 1, (x,y))
    part2 += a  
answer(part1)
answer(part2)