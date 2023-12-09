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

part1 = 0
part2 = 0

#with open("test.txt") as file:
with open("day9.txt") as file:
    for line in file.readlines():        
        parts = line.strip().split(" ")
        history = [int(x) for x in parts]
        #print(history)
        differences = [history]
        i = 1
        while not all([n == 0 for n in differences[i-1]]):       
            differences.append([])
            for n in range(len(differences[i-1])-1):
                differences[i].append(differences[i-1][n+1] - differences[i-1][n])
            #print(differences[c])                            
            i += 1

        differences[-1].append(0)
        differences[-1].insert(0, 0)        
        for i in range(len(differences)-2,-1,-1):
            #print(i, differences[i])
            differences[i].append(differences[i][-1] + differences[i+1][-1])
            differences[i].insert(0, differences[i][0] - differences[i+1][0])
        part1 += differences[0][-1]
        part2 += differences[0][0]

answer(part1)
answer(part2)