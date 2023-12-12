from itertools import permutations
from copy import copy
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


def count_groupings(str):
    groups = []
    in_hash=False
    cur = 0
    for ch in str:
        if ch == "." or ch == "?":
            in_hash = False
            if cur > 0:
                groups.append(cur)
                cur = 0
        if ch == "#":
            in_hash = True
            cur += 1
    if cur > 0:
        groups.append(cur)
    return groups

def generate_pattern(p_length):
    g = set()
    for i in range(p_length):
        for p in permutations(list("#" * i + "?" * (p_length-i)), p_length):
            p = "".join(p)
            g.add(p)
            g.add("."+p+".")
            g.add("?"+p+".")
            g.add("."+p+"?")
        for p in permutations(list("?" * (p_length-i) + "#" * i), p_length):
            p = "".join(p)
            g.add(p)
            g.add("."+p+".")
            g.add("?"+p+".")
            g.add("."+p+"?")
    return g

def grouping_combinations(springs, grouping, patterns):
    # find groupings that are met
    # grouping = sorted(grouping, reverse=True)
    # possible_groupings = {}
    # for ch in springs:
    #     if ch == ".":
    #         continue
    #     continguous_question = 0
    #     while ch == "?":
    #         continguous_question += 1

    #     continguous_hash = 0
    #     while ch == "#":
    #         continguous_hash += 1
    if count_groupings(springs) == grouping and "?" not in springs:
        return 1
    
    matching = []
    for g in grouping:
        sub = []
        for p in patterns[g]:
            if p in springs:
                sub.append(p)
        matching.append(sub)
    
    print(matching)
    # for i in range(len(springs)):
    #     if springs[i] == "?":
    #         if count_groupings(springs[:i]+"#")
    return 1

# patterns = {}
# for i in range(1,15):
#     patterns[i] = generate_pattern(i)

memo = {}
def rtry(springs_str, groupings):
    global memo
    if springs_str in memo:
        return memo[springs_str]
    
    temp_groupings = count_groupings(springs_str)
    # we matched exactly
    if temp_groupings == groupings:
        memo[springs_str] = 1
        return 1
    
    # not enough to match
    if len(springs_str) < sum(groupings)+len(groupings)-1:
        memo[springs_str] = 0
        return 0
    
    for i in range(len(springs_str)):
        if springs_str[i] == "?":
            ans = rtry(springs_str[:i]+"#"+springs_str[i+1:], groupings) + rtry(springs_str[:i]+"."+springs_str[i+1:], groupings)
            memo[springs_str] = ans
            return ans
    #if str.find("?") != -1:

    memo[springs_str] = 0
    return 0

#with open("test.txt") as file:
with open("day12.txt") as file:
    for y,line in enumerate(file.readlines()): 
        print("Processing #",y)
        line = line.strip()
        springs, grouping = line.split()
        grouping = [int(x) for x in grouping.split(",")]

        memo = {}
        res1 = rtry(springs, grouping)
        part1 += res1
        # res2 = rtry("?"+springs, grouping)
        # res3 = rtry(springs+"?", grouping)
        # print(res1,res2,res3)
        # if res1 == 1:
        #     print(1)
        #     part2 += 1
        # else:
        #     if res2 > res3:
        #         print(res2*res2*res2*res2*res3)
        #         part2 += res2*res2*res2*res2*res3
        #     else:
        #         print(res3*res3*res3*res3*res2)
        #         part2 += res3*res3*res3*res3*res2

        res2 = rtry(springs+"?"+springs, grouping+grouping)
        part2 += res1*(res2/res1)*(res2/res1)*(res2/res1)*(res2/res1)
        # esprings = springs
        # egroups = copy(grouping)
        # for i in range(4):
        #     esprings += "?" + springs
        #     egroups += grouping
        # print(esprings, egroups)
        #print(springs+"?", grouping, rtry(springs+"?", grouping))

        #part2 += rtry(springs+"?", grouping)
        #print (springs, grouping, count_groupings(springs))
        #part1 += grouping_combinations(springs, grouping, patterns)



answer(part1)
answer(part2)