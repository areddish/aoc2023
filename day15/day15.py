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

def hash(s):
    cur = 0
    for ch in s:
        cur = ((cur + ord(ch)) * 17) % 256
    return cur

from collections import defaultdict

boxes = defaultdict(list)
#with open("test.txt") as file:
with open("day15.txt") as file:
    lines = file.readlines()
    assert len(lines) == 1
    for x in lines[0].strip().split(","):
            part1 += hash(x)
            if "-" in x:
                # dash case
                label = x[:-1]
                box_number = hash(label)
                lenses = []
                removed = False
                for l in boxes[box_number]:
                    b,n = l
                    if not removed and b == label:
                        continue
                    lenses.append((b,n))
                boxes[box_number] = lenses
            else:
                label, num = x.split("=")
                box_number = hash(label)
                replaced = False
                for i,l in enumerate(boxes[box_number]):
                    b,n = l
                    if b == label:
                        replaced = True
                        boxes[box_number][i] = (label, num)
                        break
                        # found, replace

                if not replaced:
                    boxes[box_number].append((label, num))    

for i in range(256):
    for slot, lens in enumerate(boxes.get(i, [])):
        part2 += (i+1) * (slot+1) * int(lens[1])
    
answer(part1)
answer(part2)