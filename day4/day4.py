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

part1 = 0
part2 = 0

copies = {}
#with open("test.txt") as file:
with open("day4.txt") as file:
    for card, line in enumerate(file.readlines()):
        line = line.strip()
        parts = line.split("|")
        # single digits have a leading whitespace, remove it before splitting.
        my_numbers = parts[1].strip().replace("  "," ").split(" ")
        winning_numbers = parts[0].strip().split(":")[1].strip().replace("  "," ").split(" ")

        winning_number_count = 0
        card_points = 0
        for number in my_numbers:
            if number in winning_numbers:
                winning_number_count += 1
                # First match gets a point, subsequent ones double the 
                # points
                if winning_number_count == 1:
                    card_points = 1
                else:
                    card_points *= 2
        if winning_number_count > 0:
            # This copies cards based on wining number count and propagates them
            # forward. We never have to actually manage the cards in memory, instead
            # we can just keep track of how many copies we would create.
            for i in range(card+1,card+1+winning_number_count):
                copies[i] = copies.get(card, 0)+1 + copies.get(i, 0)
        part1 += card_points
        #print(winning, my_nums, points)
        part2 += 1
answer(part1)

for winning_number_count in copies:
    part2 += copies[winning_number_count]
answer(part2)